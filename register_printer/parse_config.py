import json
import logging
from .data_model import (
    TopSys
)
from .parse_excels import parse_excels
from .parser import parse_top_sys_file

LOGGER = logging.getLogger(__name__)


def get_block_types(top_sys_dict):
    block_types = []
    block_instances = top_sys_dict["block_instances"]
    for block_instance in block_instances:
        block_types.append(block_instance['type'])
    return block_types


def update_top_sys_block_template(block_template_list, top_sys):
    for block_template in block_template_list:
        block_type = block_template.block_type
        block = top_sys.find_block_by_type(block_type)
        if block is not None:
            block.block_template = block_template
    return


def generate_top_sys(top_sys_dict, block_template_list):
    top_sys = TopSys.from_top_sys_dict(top_sys_dict)
    update_top_sys_block_template(block_template_list, top_sys)

    for blk in top_sys.blocks:
        if len(blk.registers) == 0:
            LOGGER.error(
                "No register definition for block %s",
                blk.name)
            raise Exception("No register definition for block.")
    return top_sys


def parse_top_sys(config_file, excel_path):

    top_sys_dict = parse_top_sys_file(config_file)

    block_types = get_block_types(top_sys_dict)
    LOGGER.debug("Block types need to be checked: %s.", block_types)
    block_template_list = parse_excels(excel_path, block_types)

    top_sys = generate_top_sys(top_sys_dict, block_template_list)

    return top_sys


def parse_top_sys_from_json(json_file):
    rp_doc_dict = None
    with open(json_file,"r") as json_file_handler:
        rp_doc_dict = json.load(json_file_handler)
    top_sys = TopSys.from_dict(rp_doc_dict)
    return top_sys
