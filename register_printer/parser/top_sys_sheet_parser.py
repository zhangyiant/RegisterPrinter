import logging
from xlrd import open_workbook
from .parse_exception import ExcelParseException
from .parse_context import ExcelParseContext


LOGGER = logging.getLogger(__name__)


def parse_top_sys_meta_data(sheet, previous_context):
    context = previous_context.copy()
    context.row = 0
    context.column = 1
    name = sheet.cell(0, 1).value.strip()
    try:
        context.row = 1
        context.column = 1
        addr_size = int(sheet.cell(1, 1).value)
    except Exception as e:
        msg = "Parse address size error: {}.".format(e)
        raise ExcelParseException(msg, context)

    try:
        context.row = 2
        context.column = 1
        data_size = int(sheet.cell(2, 1).value)
    except Exception as e:
        msg = "Parse data size error: {}.".format(e)
        raise ExcelParseException(msg, context)

    author = sheet.cell(3, 1).value.strip()
    version = sheet.cell(4, 1).value
    result = {
        "name": name,
        "author": author,
        "version": version,
        "addressWidth": addr_size,
        "dataWidth": data_size
    }
    return result


def parse_block_instance_row(row, previous_context):
    context = previous_context.copy()
    block_instance_name = row[0].value.strip()
    block_type = row[1].value.strip()

    context.column = 2
    try:
        block_base_address = int(row[2].value.strip(), 16)
    except Exception as exc:
        msg = "Parse block base address error: {}.".format(exc)
        raise ExcelParseException(msg, context)

    context.column = 3
    try:
        block_size = int(row[3].value.strip(), 16)
    except Exception as exc:
        msg = "Parse block size error: {}.".format(exc)
        raise ExcelParseException(msg, context)

    context.column = 4
    addr_width = None
    value = row[4].value
    if value != "":
        try:
            addr_width = int(value)
        except Exception as exc:
            msg = "Parse address width error: {}.".format(exc)
            raise ExcelParseException(msg, context)

    context.column = 5
    data_width = None
    value = row[5].value
    if value != "":
        try:
            data_width = int(value)
        except Exception as exc:
            msg = "Parse data width error: {}.".format(exc)
            raise ExcelParseException(msg, context)

    result = {
        "name": block_instance_name,
        "blockType": block_type,
        "baseAddress": block_base_address,
        "blockSize": block_size,
        "addressWidth": addr_width,
        "dataWidth": data_width
    }
    return result


def parse_top_sys_sheet(sheet, previous_context):
    """
    Parse top sys excel sheet.
    :type sheet: xlrd.sheet
    """
    context = previous_context.copy()
    context.sheet_name = sheet.name
    top_dict = parse_top_sys_meta_data(sheet, context)

    top_dict["blockInstances"] = []
    for rowx in range(7, sheet.nrows):
        row = sheet.row(rowx)
        context.row = rowx
        block_inst_dict = parse_block_instance_row(row, context)
        top_dict["blockInstances"].append(block_inst_dict)
    return top_dict


def parse_top_sys_file(filename):
    LOGGER.debug("Parsing top config file: %s", filename)
    context = ExcelParseContext(filename=filename)
    workbook = open_workbook(filename)

    found = False
    top_dict = None
    for sheet in workbook.sheets():
        if sheet.name == "Top":
            found = True
            top_dict = parse_top_sys_sheet(sheet, context)
            LOGGER.debug("Parse top dict %s", top_dict)

    if not found:
        raise ExcelParseException(
            "No Sheet named \"Top\" in config file!",
            context=context
        )
    return top_dict
