import re
import os
import os.path
import logging
from jinja2 import Environment, PackageLoader


LOGGER = logging.getLogger(__name__)


def print_uvm_block(block, out_path):
    uvm_block_name = block.name.lower() + "_reg_model"
    file_name = os.path.join(
        out_path,
        uvm_block_name + ".sv")

    if os.path.exists(file_name):
        os.remove(file_name)

    env = Environment(
        loader=PackageLoader("register_printer", "templates"),
        trim_blocks=True,
        lstrip_blocks=True
    )
    template = env.get_template("reg_model.sv")

    content = template.render(
        {
            "block": block
        }
    )

    with open(file_name, "w") as bfh:
        bfh.write(content)

    return


def print_uvm_sys(top_sys, out_path):
    uvm_sys_name = top_sys.name.lower() + "_reg_model"
    file_name = os.path.join(
        out_path,
        uvm_sys_name + ".sv")

    if os.path.exists(file_name):
        os.remove(file_name)

    env = Environment(
        loader=PackageLoader("register_printer", "templates"),
        trim_blocks=True,
        lstrip_blocks=True
    )
    template = env.get_template("sys_model.sv")

    content = template.render(
        {
            "top_sys": top_sys
        }
    )

    with open(file_name, "w") as bfh:
        bfh.write(content)

    return

def print_sv_defines(top_sys, out_path):

    sv_def_name = top_sys.name.lower() + "_register_defines"
    file_name = os.path.join(
        out_path,
        sv_def_name + ".svh")

    if os.path.exists(file_name):
        os.remove(file_name)

    env = Environment(
        loader=PackageLoader("register_printer", "templates"),
        trim_blocks=True,
        lstrip_blocks=True
    )
    template = env.get_template("register_defines.svh")

    content = template.render(
        {
            "top_sys": top_sys
        }
    )

    with open(file_name, "w") as bfh:
        bfh.write(content)

    return


def print_uvm(top_sys):
    LOGGER.debug("Generating UVM register model...")

    out_dir = "regmodels"
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    for block in top_sys.blocks:
        print_uvm_block(block, out_dir)

    print_uvm_sys(top_sys, out_dir)

    print_sv_defines(top_sys, out_dir)

    LOGGER.debug("UVM register model generated in directory %s", out_dir)
    return
