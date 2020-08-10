import json
import logging
from .data_model import (
    TopSys, BlockTemplate
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


def parse_top_sys(config_file, excel_path):

    top_sys_dict = parse_top_sys_file(config_file)

    block_types = get_block_types(top_sys_dict)
    LOGGER.debug("Block types need to be checked: %s.", block_types)

    block_template_dict_list = parse_excels(excel_path, block_types)

    block_template_list = []
    for block_template_dict in block_template_dict_list:
        block_template = BlockTemplate.from_dict(block_template_dict)
        block_template_list.append(block_template)

    top_sys = TopSys.generate_top_sys(top_sys_dict, block_template_list)

    return top_sys


def parse_top_sys_from_json(json_file):
    rp_doc_dict = None
    with open(json_file,"r") as json_file_handler:
        rp_doc_dict = json.load(json_file_handler)
    top_sys = TopSys.from_dict(rp_doc_dict)
    return top_sys
