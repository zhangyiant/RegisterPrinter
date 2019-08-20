import os
import os.path
import re
import sys
import logging
from .block import *
from .register import *
from .field import *
from jinja2 import Environment, PackageLoader


LOGGER = logging.getLogger(__name__)


def print_c_header_block(block, out_path):
    LOGGER.debug("Print block %s C header...", block.name)

    file_name = os.path.join(
        out_path,
        "regs_" + block.name.lower() + ".h")
    if os.path.exists(file_name):
        os.remove(file_name)


    struct_fields = []
    prev_offset = -4
    curr_offset = -4
    byte_len = int(block.data_len / 8)
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
            sruct_fields.append(struct_field)
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

    env = Environment(
        loader=PackageLoader("register_printer", "templates"),
        trim_blocks=True
    )
    template = env.get_template("c_header_block.h")

    content = template.render(
        {
            "block_name": block.name,
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
    for block in top_sys.blocks:
        include_filename = "regs_" + block.name.lower() + ".h"
        include_filenames.append(include_filename)
    block_instances = []
    for addr_entry in top_sys.addr_map:
        block_instances.append(
            {
                "name": addr_entry['block_instance'].upper(),
                "base_address": addr_entry["base_address"],
                "type": addr_entry["block_type"]
            }
        )

    env = Environment(
        loader=PackageLoader("register_printer", "templates"),
        trim_blocks=True
    )
    template = env.get_template("c_header_sys.h")

    content = template.render(
        {
            "include_macro_name": include_macro_name,
            "include_filenames": include_filenames,
            "block_instances": block_instances
        }
    )

    with open(file_name, "w") as sfh:
        sfh.write(content)

    return

def print_c_header(top_sys):
    LOGGER.debug("Generating C header files...")

    out_dir = "regheaders"
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    for block in top_sys.blocks:
        print_c_header_block(block, out_dir)
    print_c_header_sys(top_sys, out_dir)
    LOGGER.debug("C header files generated in directory %s", out_dir)
    return
