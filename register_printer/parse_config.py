import json
import logging
from .data_model import (
    TopSys
)
from .parse_excels import parse_excels
from .parser import parse_top_sys_file

LOGGER = logging.getLogger(__name__)


def parse_top_sys(config_file, excel_path):
    top_sys_dict = parse_top_sys_file(config_file)
    top_sys = TopSys.from_top_sys_dict(top_sys_dict)
    top_sys = parse_excels(top_sys, excel_path, top_sys_dict)

    for blk in top_sys.blocks:
        if len(blk.registers) == 0:
            LOGGER.error(
                "No register definition for block %s",
                blk.name)
            raise Exception("No register definition for block.")
    return top_sys


def parse_top_sys_from_json(json_file):
    rp_doc_dict = None
    with open(json_file,"r") as json_file_handler:
        rp_doc_dict = json.load(json_file_handler)
    top_sys = TopSys.from_dict(rp_doc_dict)
    return top_sys
