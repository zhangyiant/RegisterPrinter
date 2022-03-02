import os
import os.path
import logging
from register_printer.template_loader import get_template
from register_printer.data_model import Register, Array, Struct


LOGGER = logging.getLogger(__name__)


def get_instances(block_instances):
    result = []
    for block_instance in block_instances:
        instance_dict = {}
        instance_dict["name"] = block_instance.name
        instance_dict["base_address"] = block_instance.base_address
        instance_dict["registers"] = []
        for register in block_instance.block.registers:
            if isinstance(register, Register):
                if not register.is_reserved:
                    reg_dict = {}
                    reg_dict["name"] = register.name
                    reg_dict["offset"] = register.offset
                    instance_dict["registers"].append(reg_dict)
        result.append(instance_dict)
    return result

def print_sv_defines(top_sys, out_path):

    sv_def_name = top_sys.name.lower() + "_register_defines"
    file_name = os.path.join(
        out_path,
        sv_def_name + ".svh")

    if os.path.exists(file_name):
        os.remove(file_name)

    template = get_template("register_defines.svh")

    instances = get_instances(top_sys.block_instances)

    content = template.render(
        {
            "sv_def_name": top_sys.name.lower() + "_register_defines",
            "instances": instances
        }
    )

    with open(file_name, "w") as bfh:
        bfh.write(content)

    return