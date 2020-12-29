import re
import logging
from xlrd import open_workbook


from .register_parser import parse_register
from .parse_context import ExcelParseContext
from .parse_exception import ExcelParseException


LOGGER = logging.getLogger(__name__)


def is_empty_row(row):
    if row[0].value == "":
        return True
    return False


# Todo： validate field in Block.
def validate_field_block(field, block):
    msb = field.msb
    if msb not in range(block.data_width):
        raise Exception("Invalid msb %d" % msb)
    return


def validate_sheet(sheet, previous_context):
    context = previous_context.copy()
    if sheet.ncols < 8:
        LOGGER.error(
            "sheet %s error: column number is wrong, must be greater than 8",
            sheet.name)
        msg = "Sheet column number must be greater than 8."
        raise ExcelParseException(msg, context)

    context.row = 0
    context.column = 0
    if sheet.cell(0, 0).value != "Module description:":
        LOGGER.debug(
            "sheet %s error: find no \"Module description:\" in cell(0,0)",
            sheet.name)
        msg = "No \"Module description:\" in cell(0,0)."
        raise ExcelParseException(msg, context)
    return


def is_register_row(row):
    """
        :type row: a sequence of the xlrd.sheet.cell objects
    """
    if re.match(r'0x', str(row[0].value)):
        return True
    return False


def generate_block_template_from_sheet(sheet, previous_context):

    context = previous_context.copy()
    context.sheet_name = sheet.name

    LOGGER.debug(
        "Processing sheet %s row=%d col=%d",
        sheet.name,
        sheet.nrows,
        sheet.ncols)

    validate_sheet(sheet, context)

    rowx = 3
    block_template_dict = {
        "blockType": sheet.name,
        "registers": []
    }
    while rowx < sheet.nrows:
        row = sheet.row(rowx)
        context.row = rowx
        if is_empty_row(row):
            rowx += 1
        elif is_register_row(row):
            (register_dict, rowx) = parse_register(sheet, rowx, context)
            block_template_dict["registers"].append(register_dict)
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
            msg = "Unknown row."
            raise ExcelParseException(msg, context)
    LOGGER.debug(
        "Processing sheet %s done",
        sheet.name)

    return block_template_dict


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


def parse_block_template_file(filename, block_types=None):
    context = ExcelParseContext(filename=filename)
    workbook = open_workbook(filename)

    sheet_list = get_sheet_list(workbook, block_types)

    block_template_dict_list = []
    for sheet in sheet_list:
        block_template_dict = generate_block_template_from_sheet(
            sheet,
            context
        )
        block_template_dict_list.append(block_template_dict)

    return block_template_dict_list
