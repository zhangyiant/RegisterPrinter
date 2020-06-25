import os
import os.path
import re
import logging
from .data_model import (
    Register,
    Field,
    BlockTemplate
)
from xlrd import open_workbook


LOGGER = logging.getLogger(__name__)


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


# Todo： validate field in Block.
def validate_field_block(field, block):
    msb = field.msb
    if msb not in range(block.data_width):
        raise Exception("Invalid msb %d" % msb)
    return


def parse_register(sheet, start_row):
    rowx = start_row

    register = None
    row = sheet.row(rowx)
    try:
        register = Register.parse_register_row(row)
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
    while Field.is_field_row(row):
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
    return (register, rowx)


def parse_block_template_sheet(sheet):

    result = {}

    result["name"] = sheet.name

    return result


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


def parse_excel_file(filename, top_sys):
    workbook = open_workbook(filename)
    for sheet in workbook.sheets():
        LOGGER.debug("Process sheet: \"%s\"", sheet.name)
        if sheet.name == "Top":
            LOGGER.debug("Skip Top sheet")
            continue
        block = top_sys.find_block_by_type(sheet.name)
        if block is not None:
            block_template = generate_block_template_from_sheet(
                sheet
            )
            block.block_template = block_template
        else:
            LOGGER.debug(
                "Skip sheet \"%s\", not defined in Top config.",
                sheet.name)
    return


def parse_excels(top_sys, work_path):

    LOGGER.debug("Parsing with excel files in %s.", work_path)

    filenames = os.listdir(work_path)
    for filename in filenames:
        if re.match(r'~', filename):
            continue
        elif re.search(".xlsx", filename) is not None:
            full_filename = os.path.join(work_path, filename)
            LOGGER.info("Parsing excels file: %s", full_filename)
            parse_excel_file(full_filename, top_sys)

    for blk in top_sys.blocks:
        if len(blk.registers) == 0:
            LOGGER.error(
                "No register definition for block %s",
                blk.name)
            raise Exception("No register definition for block.")

    return top_sys
