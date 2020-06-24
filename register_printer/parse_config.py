import re
import os
import sys
import json
import logging
from xlrd import *
from .data_model import (
    TopSys,
    BlockTemplate,
    Block,
    BlockInstance
)
from .parse_excels import parse_excels


LOGGER = logging.getLogger(__name__)


def parse_block_instance_row(row):
    block_instance_name = row[0].value.strip()
    block_type = row[1].value.strip()
    block_base_address = int(row[2].value.strip(), 16)
    block_size = int(row[3].value.strip(), 16)
    addr_width = None
    value = row[4].value
    if value != "":
        addr_width = int(value)
    data_width = None
    value = row[5].value
    if value != "":
        data_width = int(value)
    result = {
        "name": block_instance_name,
        "type": block_type,
        "base_address": block_base_address,
        "size": block_size,
        "addr_width": addr_width,
        "data_width": data_width
    }
    return result


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
        sheet_row = sheet.row(row)
        block_inst_dict = parse_block_instance_row(sheet_row)

        block = top_sys.find_block_by_type(
            block_inst_dict["type"])
        if block is None:
            block_template = BlockTemplate(
                block_inst_dict["type"]
            )
            block = Block(
                top_sys,
                block_template,
                addr_width=block_inst_dict["addr_width"],
                data_width=block_inst_dict["data_width"],
                size=block_inst_dict["size"]
            )
            top_sys.add_block(block)

        new_block_instance = BlockInstance(
            top_sys,
            block_inst_dict["name"],
            block,
            block_inst_dict["base_address"],
            block_inst_dict["size"]
        )
        top_sys.add_block_to_address_map(
            block_inst_dict["type"],
            block_inst_dict["name"],
            block_inst_dict["base_address"],
            block_inst_dict["size"])
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
    rp_doc_dict = None
    with open(json_file,"r") as json_file_handler:
        rp_doc_dict = json.load(json_file_handler)
    top_sys = TopSys.from_dict(rp_doc_dict)
    return top_sys
