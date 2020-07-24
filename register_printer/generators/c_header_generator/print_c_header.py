import os
import os.path
import re
import sys
import logging
from register_printer.template_loader import get_template


LOGGER = logging.getLogger(__name__)


def print_c_test(top_sys, out_path):
    LOGGER.debug("Print top sys C test...")

    file_name = os.path.join(
        out_path,
        "test.c")

    if os.path.exists(file_name):
        os.remove(file_name)

    template = get_template("c_test.c")

    content = template.render(
        {
            "top_sys": top_sys
        }
    )

    with open(file_name, "w") as sfh:
        sfh.write(content)

    return


def print_c_header_block(block, out_path):

    LOGGER.debug("Print block %s C header...", block.block_type)

    file_name = os.path.join(
        out_path,
        "regs_" + block.block_type.lower() + ".h")
    if os.path.exists(file_name):
        os.remove(file_name)

    struct_fields = []
    prev_offset = -4
    curr_offset = -4
    byte_len = int(block.data_width / 8)
    rsvd_idx = 0
    for reg in block.registers:
        prev_offset = curr_offset
        curr_offset = reg.offset
        nrsvd = (curr_offset - prev_offset) / byte_len - 1
        mat = "    {:24}\t{:24}\t;\n"
        if nrsvd > 0:
            struct_field = {
                "type": "volatile const int",
                "name": "RSVD%d[%d]" % (rsvd_idx, nrsvd)
            }
            struct_fields.append(struct_field)
            rsvd_idx = rsvd_idx + 1
        struct_field = {
            "type": "volatile int",
            "name": reg.name.upper()
        }
        struct_fields.append(struct_field)

    pos_mask_macros = []
    for reg in block.registers:
        for fld in reg.fields:
            if fld.name != "-":
                prefix = reg.name.upper() + "_" + fld.name.upper()
                pos_value = fld.lsb
                mask_value = (1 << (fld.msb - fld.lsb + 1)) - 1
                pos_mask_macros.append({
                    "prefix": prefix,
                    "pos_value": pos_value,
                    "mask_value": mask_value
                })

    template = get_template("c_header_block.h")

    content = template.render(
        {
            "block_type": block.block_type,
            "struct_fields": struct_fields,
            "pos_mask_macros": pos_mask_macros
        }
    )

    with open(file_name, "w") as bfh:
        bfh.write(content)

    return


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
        include_filename = "regs_" + block_instance.block.block_type.lower() + ".h"
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
