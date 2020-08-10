import os
import os.path
import re
import logging

from register_printer.parser import parse_block_template_file


LOGGER = logging.getLogger(__name__)


def parse_excels(work_path, block_types=None):

    LOGGER.debug("Parsing with excel files in %s.", work_path)

    filenames = os.listdir(work_path)
    block_template_dict_list = []
    for filename in filenames:
        if re.match(r'~', filename):
            continue
        elif re.search(".xlsx", filename) is not None:
            full_filename = os.path.join(work_path, filename)
            LOGGER.info("Parsing excels file: %s", full_filename)
            temp_block_template_dict_list = parse_block_template_file(
                full_filename,
                block_types)
            LOGGER.debug(
                "Parsed block template dict: %s",
                temp_block_template_dict_list
            )
            block_template_dict_list.extend(temp_block_template_dict_list)

    return block_template_dict_list

