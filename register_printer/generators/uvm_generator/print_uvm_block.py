import os
import os.path
import logging
from register_printer.template_loader import get_template


LOGGER = logging.getLogger(__name__)

def print_uvm_block(block, out_path):
    uvm_block_name = block.block_type.lower() + "_reg_model"
    file_name = os.path.join(
        out_path,
        uvm_block_name + ".sv")

    if os.path.exists(file_name):
        os.remove(file_name)

    template = get_template("reg_model.sv")

    content = template.render(
        {
            "block": block
        }
    )

    with open(file_name, "w") as bfh:
        bfh.write(content)

    return
