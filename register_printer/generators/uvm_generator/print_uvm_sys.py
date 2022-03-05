import os
import os.path
import logging
from register_printer.template_loader import get_template

LOGGER = logging.getLogger(__name__)


def print_uvm_sys(top_sys, out_path):
    uvm_sys_name = top_sys.name.lower() + "_reg_model"
    file_name = os.path.join(
        out_path,
        uvm_sys_name + ".sv")

    if os.path.exists(file_name):
        os.remove(file_name)

    template = get_template("sys_model.sv")

    content = template.render(
        {
            "top_sys": top_sys
        }
    )

    with open(file_name, "w") as bfh:
        bfh.write(content)

    return
