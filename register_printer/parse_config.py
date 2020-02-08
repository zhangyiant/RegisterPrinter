import re
import os
import sys
import logging
from xlrd import *
from .top_sys import *
from .parse_excels import parse_excels
from .block import Block


LOGGER = logging.getLogger(__name__)

def parse_sheet(sheet):
    top_sys = None
    name = sheet.cell(0, 1).value.strip()
    addr_size = int(sheet.cell(1, 1).value)
    data_size = int(sheet.cell(2, 1).value)
    author = sheet.cell(3, 1).value.strip()
    version = sheet.cell(4, 1).value

    top_sys = TopSys(name, addr_size, data_size)
    top_sys.author = author
    top_sys.version = version

    for row in range(7, sheet.nrows):
        block_instance = sheet.cell(row, 0).value.strip()
        block_type = sheet.cell(row, 1).value.strip()
        block_address = int(sheet.cell(row, 2).value.strip(), 16)
        block_size = int(sheet.cell(row, 3).value.strip(), 16)
        val = sheet.cell(row, 4).value
        if val == "":
            block_address_size = addr_size
        else:
            block_address_size = int(val)
        val = sheet.cell(row, 5).value
        if val == "":
            block_data_size = data_size
        else:
            block_data_size = int(val)
        if top_sys.find_block_by_type(block_type) is None:
            block = Block(
                block_type,
                block_size,
                block_address_size,
                block_data_size)
            top_sys.add_block(block)
        top_sys.add_block_to_address_map(
            block_type,
            block_instance,
            block_address,
            block_size)
    return top_sys


def parse_config(cfg_name):
    LOGGER.debug("Parsing top config file: %s", cfg_name)
    workbook = open_workbook(cfg_name)

    found = False
    top_sys = None
    for sheet in workbook.sheets():
        if sheet.name == "Top":
            found = True
            top_sys = parse_sheet(sheet)

    if not found:
        LOGGER.error("Error: No Sheet named \"Top\" in config file!")
    return top_sys

def parse_top_sys(config_file, excel_path):
    top_sys = parse_config(config_file)
    top_sys = parse_excels(top_sys, excel_path)
    return top_sys

def parse_top_sys_from_json(json_file):
    print("Todo: not implemented yet.")
    return None
