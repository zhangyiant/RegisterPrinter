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


def update_top_sys_block_template(block_template_list, top_sys):
    for block_template in block_template_list:
        block_type = block_template.block_type
        block = top_sys.find_block_by_type(block_type)
        if block is not None:
            block.block_template = block_template
    return


def parse_excels(top_sys, work_path, top_sys_dict):

    LOGGER.debug("Parsing with excel files in %s.", work_path)

    filenames = os.listdir(work_path)
    for filename in filenames:
        if re.match(r'~', filename):
            continue
        elif re.search(".xlsx", filename) is not None:
            full_filename = os.path.join(work_path, filename)
            LOGGER.info("Parsing excels file: %s", full_filename)
            block_types = get_block_types(top_sys_dict)
            LOGGER.debug("Block types need to be checked: %s.", block_types)
            block_template_list = parse_block_template_file(full_filename, block_types)
            update_top_sys_block_template(block_template_list, top_sys)

    for blk in top_sys.blocks:
        if len(blk.registers) == 0:
            LOGGER.error(
                "No register definition for block %s",
                blk.name)
            raise Exception("No register definition for block.")

    return top_sys
