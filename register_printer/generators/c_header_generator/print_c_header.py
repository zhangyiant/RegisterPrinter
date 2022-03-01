import os
import os.path
import logging
from register_printer.template_loader import get_template
from .print_c_header_block import print_c_header_block
from .print_c_test import print_c_test


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
    for block_instance in top_sys.block_instances:
        include_filename = "regs_" + block_instance.block_type.lower() + ".h"
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


def print_c_header(top_sys, output_path="."):
    LOGGER.debug("Generating C header files...")

    out_dir = os.path.join(
        output_path,
        "regheaders")
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    for block in top_sys.blocks:
        print_c_header_block(block, out_dir)

    print_c_header_sys(top_sys, out_dir)
    print_c_test(top_sys, out_dir)
    LOGGER.debug("C header files generated in directory %s", out_dir)
    return
