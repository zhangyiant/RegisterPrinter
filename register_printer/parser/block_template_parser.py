import re
import logging
from xlrd import open_workbook


from .register_parser import parse_register
from .parse_context import ExcelParseContext
from .parse_exception import ExcelParseException


LOGGER = logging.getLogger(__name__)


def is_empty_row(row):
    if row[0].value.strip() == "" and row[1].value.strip() == "":
        return True
    return False

def is_register_table_flag_row(row):
    if row[0].value.strip().upper() == "register description".upper():
        return True
    return False

def is_register_table_title_row(row):
    if row[0].value.strip().upper() == "Offset".upper():
        return True
    return False

def parse_register_table_title(row):
    column_count = len(row)
    result = {}
    for i in range(column_count):
        if row[i].value.strip().upper() == "offset".upper():
            result["offset"] = i
        elif row[i].value.strip().upper() == "name".upper():
            result["name"] = i
        elif row[i].value.strip().upper() == "msb".upper():
            result["msb"] = i
        elif row[i].value.strip().upper() == "lsb".upper():
            result["lsb"] = i
        elif row[i].value.strip().upper() == "field name".upper():
            result["field name"] = i
        elif row[i].value.strip().upper() == "access".upper():
            result["access"] = i
        elif row[i].value.strip().upper() == "default".upper():
            result["default"] = i
        elif row[i].value.strip().upper() == "description".upper():
            result["description"] = i
    LOGGER.debug("Register table column mapping: %s", result)
    return result

def is_array_table_flag_row(row):
    if row[0].value.strip().upper() == "register array".upper():
        return True
    return False

def is_array_table_title_row(row):
    if row[1].value.strip().upper() == "array_name".upper():
        return True
    return False

def parse_array_table_title(row):
    column_count = len(row)
    result = {}
    for i in range(column_count):
        if row[i].value.strip().upper() == "array_name".upper():
            result["array_name"] = i
        elif row[i].value.strip().upper() == "array_len".upper():
            result["array_len"] = i
        elif row[i].value.strip().upper() == "array_offset".upper():
            result["array_offset"] = i
        elif row[i].value.strip().upper() == "start_addr".upper():
            result["start_addr"] = i
        elif row[i].value.strip().upper() == "end_addr".upper():
            result["end_addr"] = i
    LOGGER.debug("Array table column mapping: %s", result)
    return result

def is_table_title_row(row):
    if is_register_table_title_row(row) or \
        is_array_table_title_row(row):
        return True
    return False

def is_table_flag_row(row):
    if is_array_table_flag_row(row) or \
        is_register_table_flag_row(row):
        return True
    return False

# Todo： validate field in Block.
def validate_field_block(field, block):
    msb = field.msb
    if msb not in range(block.data_width):
        raise Exception("Invalid msb %d" % msb)
    return


def find_register_table_title_row(sheet, previous_context):
    context = previous_context.copy()
    rowx = 1
    context.row = rowx
    found = False
    while rowx < sheet.nrows:
        row = sheet.row(rowx)
        if is_register_table_flag_row(row):
            LOGGER.debug("Register table flag row is found. Row: %s", rowx + 1)
            rowx += 1
            context.row = rowx
            if rowx < sheet.nrows:
                row = sheet.row(rowx)
                if is_register_table_title_row(row):
                    LOGGER.debug("Register table title row is found. Row: %s", rowx + 1)
                    found = True
                    break
                else:
                    msg = "No Register table title row found after Register table flag."
                    raise ExcelParseException(msg, context)
            else:
                msg = "Unexpected end of sheet after finding Register table flag."
                raise ExcelParseException(msg, context)
        else:
            rowx += 1
            context.row = rowx
    if not found:
        msg = "Register table title row not found"
        raise ExcelParseException(msg, context)
    return rowx

def find_array_table_title_row(sheet, previous_context):
    context = previous_context.copy()
    rowx = 1
    context.row = rowx
    found = False
    while rowx < sheet.nrows:
        row = sheet.row(rowx)
        if is_array_table_flag_row(row):
            LOGGER.debug("Array flag row is found. Row: %s", rowx)
            rowx += 1
            context.row = rowx
            if rowx < sheet.nrows:
                row = sheet.row(rowx)
                if is_array_table_title_row(row):
                    LOGGER.debug("Array table title row is found. Row: %s", rowx)
                    found = True
                    break
                else:
                    msg = "No Array table title row found after Array table flag."
                    raise ExcelParseException(msg, context)
            else:
                msg = "Unexpected end of sheet after finding Array table flag."
                raise ExcelParseException(msg, context)
        else:
            rowx += 1
            context.row = rowx
    if found:
        return rowx
    return None

def parse_array_row(row, array_table_column_mapping, previous_context):
    """
        row: xlrd row object. You can obtain it by sheet.row()
                 a sequence of cells.
    """
    context = previous_context.copy()

    context.column = array_table_column_mapping["array_name"]
    array_name = row[context.column].value

    context.column = array_table_column_mapping["array_len"]
    try:
        array_length = int(row[context.column].value)
    except Exception as exc:
        msg = "Parse array length error: {}.".format(exc)
        raise ExcelParseException(msg, context)

    context.column = array_table_column_mapping["array_offset"]
    try:
        array_offset = int(row[context.column].value, 16)
    except Exception as exc:
        msg = "Parse array offset error: {}.".format(exc)
        raise ExcelParseException(msg, context)

    context.column = array_table_column_mapping["start_addr"]
    try:
        start_address = int(row[context.column].value, 16)
    except Exception as exc:
        msg = "Parse start address error: {}.".format(exc)
        raise ExcelParseException(msg, context)

    context.column = array_table_column_mapping["end_addr"]
    try:
        end_address = int(row[context.column].value, 16)
    except Exception as exc:
        msg = "Parse end address error: {}.".format(exc)
        raise ExcelParseException(msg, context)

    result = {
        "name": array_name,
        "length": array_length,
        "offset": array_offset,
        "startAddress": start_address,
        "endAddress": end_address,
        "description": ""
    }
    return result

def parse_array_table(sheet, start_rowx, previous_context):
    context = previous_context.copy()
    rowx = start_rowx
    context.row = rowx

    row = sheet.row(rowx)
    array_table_column_mapping = parse_array_table_title(row)

    rowx += 1
    array_dict_list = []
    while rowx < sheet.nrows:
        row = sheet.row(rowx)
        context.row = rowx
        if is_table_title_row(row):
            break
        if is_table_flag_row(row):
            break
        if is_empty_row(row):
            rowx += 1
        else:
            array_dict = parse_array_row(row, array_table_column_mapping, context)
            array_dict_list.append(array_dict)
            rowx += 1
    return array_dict_list

def parse_register_table(sheet, start_rowx, previous_context):
    context = previous_context.copy()
    rowx = start_rowx
    context.row = rowx

    row = sheet.row(rowx)
    register_table_column_mapping = parse_register_table_title(row)

    rowx += 1
    context.row = rowx
    register_dict_list = []
    while rowx < sheet.nrows:
        row = sheet.row(rowx)
        context.row = rowx
        if is_table_title_row(row):
            break
        if is_table_flag_row(row):
            break
        if is_empty_row(row):
            rowx += 1
        elif is_register_row(row):
            (register_dict, rowx) = parse_register(sheet, rowx, register_table_column_mapping, context)
            register_dict_list.append(register_dict)
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
    return register_dict_list

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
    if sheet.cell(0, 0).value.upper() != "Module description".upper():
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


    block_template_dict = {
        "blockType": sheet.name,
        "registers": [],
        "arrays": []
    }

    register_table_title_rowx = find_register_table_title_row(
        sheet,
        context
    )
    rowx = register_table_title_rowx
    context.row = rowx
    block_template_dict["registers"] = parse_register_table(
        sheet,
        rowx,
        context
    )

    array_table_title_rowx = find_array_table_title_row(
        sheet,
        context
    )
    if array_table_title_rowx is not None:
        rowx = array_table_title_rowx
        context.row = rowx
        array_dict_list = parse_array_table(
            sheet,
            rowx,
            context
        )
        block_template_dict["arrays"] = array_dict_list

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
