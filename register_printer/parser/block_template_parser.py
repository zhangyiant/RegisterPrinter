import re
import logging
from xlrd import open_workbook
from register_printer.data_model import (
    Register,
    Field,
    BlockTemplate
)


LOGGER = logging.getLogger(__name__)


# Todo： validate field in Block.
def validate_field_block(field, block):
    msb = field.msb
    if msb not in range(block.data_width):
        raise Exception("Invalid msb %d" % msb)
    return


def validate_sheet(sheet):
    if sheet.ncols < 8:
        LOGGER.error(
            "sheet %s error: column number is wrong, must be greater than 8",
            sheet.name)
        raise Exception("Sheet column number must be geater than 8")

    if sheet.cell(0, 0).value != "Module description:":
        LOGGER.debug(
            "sheet %s error: find no \"Module description:\" in cell(0,0)",
            sheet.name)
        raise Exception("No \"Module description:\" in cell(0,0)")
    return


def is_empty_row(row):
    if row[0].value == "":
        return True
    return False


def is_field_row(row):
    '''
        row: xlrd row object.
    '''
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
    description = "%s" % (row[7].value)

    result = {
        "offset": offset,
        "name": name,
        "description": description
    }

    return result


def parse_register(sheet, start_row):
    rowx = start_row

    register = None
    row = sheet.row(rowx)
    try:
        register_dict = parse_register_row(row)
        register = Register(
            register_dict["name"],
            register_dict["offset"],
            register_dict["description"]
        )
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
    while is_field_row(row):
        field = None
        try:
            field = Field.parse_excel_row(row)
            register.add_field(field)
        except Exception as exc:
            LOGGER.error(
                "sheet %s row %d error, Register %s: %s",
                sheet.name,
                rowx + 1,
                register.name,
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
    return register, rowx


def is_register_row(row):
    '''
        :type row: a sequence of the xlrd.sheet.cell objects
    '''
    if re.match(r'0x', str(row[0].value)):
        return True
    return False


def generate_block_template_from_sheet(sheet):

    LOGGER.debug(
        "Processing sheet %s row=%d col=%d",
        sheet.name,
        sheet.nrows,
        sheet.ncols)

    validate_sheet(sheet)

    block_template = BlockTemplate(
        sheet.name
    )
    rowx = 3
    while rowx < sheet.nrows:
        row = sheet.row(rowx)
        if is_empty_row(row):
            rowx += 1
        elif is_register_row(row):
            (register, rowx) = parse_register(sheet, rowx)
            block_template.add_register(register)
            # Todo: Add offset, size validation
            # if register.offset > block.size:
            #     LOGGER.error(
            #         "sheet %s row %d error: offset %x > block size %x",
            #         sheet.name,
            #         rowx,
            #         register.offset,
            #         block.size)
            #     raise Exception("offset > block size")
        else:
            LOGGER.error(
                "sheet %s row %d error: unknown row.",
                sheet.name,
                rowx)
            LOGGER.error(" %s", sheet.cell(rowx, 0).value)
            raise Exception("Unknown row")
    LOGGER.debug(
        "Processing sheet %s done",
        sheet.name)
    return block_template


def is_sheet_parse_needed(sheet_name, block_types=None):
    if sheet_name == "Top":
        LOGGER.debug("Skip Top sheet")
        return False
    if block_types is None:
        # All sheet needs to be parsed.
        return True
    result = False
    for block_type in block_types:
        if sheet_name.upper() == block_type.upper():
            result = True
            break
    return result


def get_sheet_list(workbook, block_types=None):
    sheet_list = []
    for sheet in workbook.sheets():
        LOGGER.debug("Process sheet: \"%s\"", sheet.name)
        if is_sheet_parse_needed(sheet.name, block_types):
            sheet_list.append(sheet)
        else:
            LOGGER.debug(
                'Skip sheet "%s", not defined in Top config or '
                'sheet name is "Top"',
                sheet.name)
    return sheet_list


def parse_excel_file(filename, block_types=None):

    workbook = open_workbook(filename)

    sheet_list = get_sheet_list(workbook, block_types)

    block_template_list = []
    for sheet in sheet_list:
        block_template = generate_block_template_from_sheet(
            sheet
        )
        block_template_list.append(block_template)

    return block_template_list
