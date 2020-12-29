import logging

from .field_parser import parse_field_row
from .parse_exception import ExcelParseException


LOGGER = logging.getLogger(__name__)


def is_empty_row(row):
    if row[0].value == "":
        return True
    return False


def is_field_row(row):
    """
        row: xlrd row object.
    """
    if row[2].value != "":
        return True
    return False


def validate_register_row_empty_field(row, previous_context):
    """
        row can be obtained by xlrd sheet.row() method.
        It's a sequence of cell objects.
    """
    context = previous_context.copy()
    field_map = [
        (2, "msb"),
        (3, "lsb"),
        (4, "field"),
        (5, "access"),
        (6, "default")
    ]
    for (col, field_name) in field_map:
        context.column = col
        if row[col].value != "":
            msg = "Field '%s' must be emtpy." % field_name
            raise ExcelParseException(msg, context)
    return


def parse_register_row(row, previous_context):
    """
        row: xlrd row object. You can obtain it by sheet.row()
                 a sequence of cells.
    """
    context = previous_context.copy()
    validate_register_row_empty_field(row, context)

    context.column = 0
    try:
        offset = int(row[0].value, 16)
    except Exception as exc:
        msg = "Parse offset error: {}.".format(exc)
        raise ExcelParseException(msg, context)

    name = row[1].value
    description = "%s" % row[7].value

    result = {
        "offset": offset,
        "name": name,
        "description": description
    }

    return result


def parse_register(sheet, start_row, previous_context):
    context = previous_context.copy()
    rowx = start_row

    row = sheet.row(rowx)
    context.row = rowx

    register_dict = parse_register_row(row, context)

    rowx = rowx + 1
    row = sheet.row(rowx)
    context.row = rowx
    field_dict_list = []
    while is_field_row(row):
        field_dict = parse_field_row(row, context)
        field_dict_list.append(field_dict)

        if rowx < sheet.nrows - 1:
            rowx = rowx + 1
            row = sheet.row(rowx)
            context.row = rowx
        else:
            break

    if is_empty_row(row):
        rowx += 1
    else:
        err_msg = \
            "sheet {0} row {1} error: no blank row between registers".format(
                sheet.name,
                rowx + 1)
        LOGGER.debug(err_msg)
        raise Exception(err_msg)

    register_dict["fields"] = field_dict_list

    return register_dict, rowx
