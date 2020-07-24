import os
import os.path
import re
import logging

from register_printer.parser import parse_block_template_file

LOGGER = logging.getLogger(__name__)


def get_block_types(top_sys_dict):
    block_types = []
    block_instances = top_sys_dict["block_instances"]
    for block_instance in block_instances:
        block_types.append(block_instance['type'])
    return block_types


def parse_excels(top_sys, work_path, top_sys_dict):

    LOGGER.debug("Parsing with excel files in %s.", work_path)

    filenames = os.listdir(work_path)
    block_template_list = []
    for filename in filenames:
        if re.match(r'~', filename):
            continue
        elif re.search(".xlsx", filename) is not None:
            full_filename = os.path.join(work_path, filename)
            LOGGER.info("Parsing excels file: %s", full_filename)
            block_types = get_block_types(top_sys_dict)
            LOGGER.debug("Block types need to be checked: %s.", block_types)
            temp_block_template_list = parse_block_template_file(full_filename, block_types)
            block_template_list.extend(temp_block_template_list)
    return block_template_list

