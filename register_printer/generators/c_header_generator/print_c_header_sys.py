import logging
import os

from register_printer.template_loader import get_template

LOGGER = logging.getLogger(__name__)


def print_c_header_sys(top_sys, out_path):
    LOGGER.debug("Print top sys C header...")

    file_name = os.path.join(
        out_path,
        "regs_" + top_sys.name.lower() + ".h")

    if os.path.exists(file_name):
        os.remove(file_name)

    include_macro_name = "REGS_" + top_sys.name.upper() + "_H"
    include_filenames = []
    for block in top_sys.blocks:
        include_filename = "regs_" + block.block_type.lower() + ".h"
        include_filenames.append(include_filename)

    block_instances_data = []
    for block_instance in top_sys.block_instances:
        block_instances_data.append(
            {
                "name": block_instance.name.upper(),
                "base_address": block_instance.base_address,
                "type": block_instance.block_type
            }
        )

    template = get_template("c_header_sys.h")

    content = template.render(
        {
            "include_macro_name": include_macro_name,
            "include_filenames": include_filenames,
            "block_instances": block_instances_data
        }
    )

    with open(file_name, "w") as sfh:
        sfh.write(content)

    return