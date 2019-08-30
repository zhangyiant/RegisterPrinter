import os
import os.path
import re
import logging
from .block import *
from .register import Register
from .field import Field, RW_TYPES
from xlrd import *


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

def is_register_row(sheet, row):
    if re.match(r'0x', str(sheet.cell(row, 0).value)):
        return True
    return False

def is_field_row(sheet, row):
    if sheet.cell(row, 2).value != "":
        return True
    return False

def is_empty_row(sheet, row):
    if sheet.cell(row, 0).value == "":
        return True
    return False

def validate_register_row_empty_field(sheet, row):
    field_map = [
        (2, "msb"),
        (3, "lsb"),
        (4, "field"),
        (5, "access"),
        (6, "default")
    ]
    for (col, field_name) in field_map:
        if sheet.cell(row, col).value != "":
            LOGGER.error(
                "sheet %s row %d error: %s not empty in register define row",
                sheet.name,
                row + 1,
                field_name)
            raise Exception("%s must be emtpy." % field_name)
    return

def parse_register_row(sheet, row):

    validate_register_row_empty_field(sheet, row)

    offset = int(sheet.cell(row, 0).value, 16)
    name = sheet.cell(row, 1).value
    description = "%s" % (sheet.cell(row, 7).value)
    register = Register(name, offset, description)

    return register

def validate_field(field, block, previous_lsb):
    msb = field.msb
    lsb = field.lsb
    name = field.name
    access = field.access
    default = field.default
    if msb not in range(block.data_len):
        raise Exception("Invalid msb %d" % msb)
    if lsb not in range(block.data_len):
        raise Exceptioin("Invalid lsb %d" % lsb)
    if lsb > msb:
        raise Exception("lsb %d > msb %d" % (lsb, msb))
    if previous_lsb >= msb:
        raise Exception("previous lsb %d > msb %d" % (previous_lsb, msb))
    if name == "":
        raise Exception("no Field Name")
    if access not in RW_TYPES:
        raise Exception("Invalid access type.")
    if default >= (1 << (msb-lsb + 1)):
        raise Exception("Default value is out of range.")
    return

def parse_field_row(sheet, row):
    msb = int(sheet.cell(row, 2).value)
    lsb = int(sheet.cell(row, 3).value)
    field_name = sheet.cell(row, 4).value
    access = sheet.cell(row, 5).value.upper()
    default = sheet.cell(row, 6).value
    description = "%s" % (sheet.cell(row, 7).value)
    if re.match(r"0x", str(default)):
        default = int(default, 16)
    else:
        try:
            default = int(default)
        except:
            raise Exception("Invalid default value")
    field = Field(field_name, msb, lsb, default, access, description)
    return field

def parse_register(sheet, block, start_row):
    row = start_row
    register = parse_register_row(sheet, row)

    row = row + 1
    lsb_pre = -1
    while is_field_row(sheet, row):
        field = parse_field_row(sheet, row)
        try:
            validate_field(field, block, lsb_pre)
        except Exception as exc:
            LOGGER.error(
                "sheet %s row %d error: %s",
                sheet.name,
                row,
                str(exc)
            )
            raise Exception(
                "sheet %s row %d error: %s" % (sheet.name, row, str(exc)))
        register.add_field(field)
        lsb_pre = field.lsb
        if row < sheet.nrows - 1:
            row = row + 1
        else:
            break

    if is_empty_row(sheet, row):
        row += 1
    else:
        LOGGER.debug(
            "sheet %s row %d error: no blank row between registers",
            sheet.name,
            row + 1)
        raise Exception("No blank row between registers")
    return (register, row)

def process_sheet(sheet, block):
    LOGGER.debug(
        "Processing sheet %s row=%d col=%d",
        sheet.name,
        sheet.nrows,
        sheet.ncols)

    validate_sheet(sheet)

    row = 3
    while row < sheet.nrows:
        if is_empty_row(sheet, row):
            row += 1
        elif is_register_row(sheet, row):
            (register, row) = parse_register(sheet, block, row)
            if register.offset > block.size:
                LOGGER.error(
                    "sheet %s row %d error: offset %x > block size %x",
                    sheet.name,
                    row,
                    offset,
                    block.size)
                raise Exception("offset > block size")
            block.add_register(register)
        else:
            LOGGER.error(
                "sheet %s row %d error: unknown row.",
                sheet.name,
                row)
            LOGGER.error(" %s", sheet.cell(row, 0).value)
            raise Exception("Unknown row")
    block.sort_register_by_offset()
    LOGGER.debug(
        "Processing sheet %s done",
        sheet.name)
    return

def parse_excel_file(filename, top_sys):
    workbook = open_workbook(filename)
    for sheet in workbook.sheets():
        if sheet.name == "Top":
            continue
        block = top_sys.find_block_by_name(sheet.name)
        if block is not None:
            process_sheet(sheet, block)
    return


def parse_excels(top_sys, work_path):

    LOGGER.debug("Parsing with excel files in %s.", work_path)

    filenames = os.listdir(work_path)
    for filename in filenames:
        if  re.match(r'~', filename):
            continue
        elif re.search(".xlsx", filename) is not None:
            full_filename = os.path.join(work_path, filename)
            parse_excel_file(full_filename, top_sys)

    for blk in top_sys.blocks:
        if len(blk.registers) == 0:
            LOGGER.error(
                "No register definition for block %s",
                blk.name)
            raise Exception("No register definition for block.")

    return top_sys