import logging

from .field_parser import parse_field_row


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


def validate_register_row_empty_field(row):
    """
        row can be obtained by xlrd sheet.row() method.
        It's a sequence of cell objects.
    """
    field_map = [
        (2, "msb"),
        (3, "lsb"),
        (4, "field"),
        (5, "access"),
        (6, "default")
    ]
    for (col, field_name) in field_map:
        if row[col].value != "":
            raise Exception("%s must be emtpy." % field_name)
    return


def parse_register_row(row):
    """
        row: xlrd row object. You can obtain it by sheet.row()
                 a sequence of cells.
    """

    validate_register_row_empty_field(row)

    offset = int(row[0].value, 16)
    name = row[1].value
    description = "%s" % row[7].value

    result = {
        "offset": offset,
        "name": name,
        "description": description
    }

    return result


def parse_register(sheet, start_row):
    rowx = start_row

    row = sheet.row(rowx)
    try:
        register_dict = parse_register_row(row)
    except Exception as exc:
        LOGGER.error(
            "sheet %s row %d error: %s",
            sheet.name,
            rowx + 1,
            str(exc)
        )
        raise

    rowx = rowx + 1
    row = sheet.row(rowx)
    field_dict_list = []
    while is_field_row(row):
        try:
            field_dict = parse_field_row(row)
            field_dict_list.append(field_dict)
        except Exception as exc:
            LOGGER.error(
                "sheet %s row %d error, Register %s: %s",
                sheet.name,
                rowx + 1,
                register_dict["name"],
                str(exc)
            )
            raise

        if rowx < sheet.nrows - 1:
            rowx = rowx + 1
            row = sheet.row(rowx)
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