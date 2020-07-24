import json
import logging
from .data_model import (
    TopSys,
    BlockTemplate,
    Block,
    BlockInstance
)
from .parse_excels import parse_excels
from .parser import parse_top_sys_file

LOGGER = logging.getLogger(__name__)


def top_sys_dict_to_top_sys(top_dict):
    top_sys = TopSys(
        top_dict["name"],
        top_dict["default_addr_width"],
        top_dict["default_data_width"]
    )
    top_sys.author = top_dict["author"]
    top_sys.version = top_dict["version"]
    for block_inst_dict in top_dict["block_instances"]:

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


def parse_top_sys(config_file, excel_path):
    top_sys_dict = parse_top_sys_file(config_file)
    top_sys = top_sys_dict_to_top_sys(top_sys_dict)
    top_sys = parse_excels(top_sys, excel_path)
    return top_sys


def parse_top_sys_from_json(json_file):
    rp_doc_dict = None
    with open(json_file,"r") as json_file_handler:
        rp_doc_dict = json.load(json_file_handler)
    top_sys = TopSys.from_dict(rp_doc_dict)
    return top_sys
