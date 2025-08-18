import os
import logging

from register_printer.data_model import Register, Array, Struct
from register_printer.template_loader import get_template


LOGGER = logging.getLogger(__name__)


def get_default_value(registers):
    result = 0xffffffff
    if len(registers) > 0:
        register = registers[0]
        if isinstance(register, Register):
            if not register.is_reserved:
                result = register.calculate_register_default()
        elif isinstance(register, Array):
            if not isinstance(register.content_type, Struct):
                msg = "Unsupported: Content type in Array is not Struct."
                LOGGER.error(msg)
                raise Exception(msg)
            struct = register.content_type
            result = get_default_value(struct.registers)
    return result


def generate_test_parameters(block_instance):
    default_value = get_default_value(block_instance.block.registers)
    test_parameters = {}
    test_parameters["instance_name"] = block_instance.name
    test_parameters["base_address"] = block_instance.base_address
    test_parameters["block_size"] = block_instance.block_size
    test_parameters["default_value"] = default_value
    return test_parameters


def print_c_test(top_sys, out_path):
    LOGGER.debug("Print top sys C test...")

    file_name = os.path.join(
        out_path,
        "register_sanity_scan.c")

    if os.path.exists(file_name):
        os.remove(file_name)

    template = get_template("c_test.c")

    fields = []
    for blockinst in top_sys.block_instances:
        block = blockinst.block
        for register in block.registers:
            try:
                for field in register.fields:
                    if field.access.upper() == "RW":
                        test_field = {}
                        test_field["name"] = f"{blockinst.name}.{register.name}.{field.name}"
                        test_field["addr"] = "0x%x"%(register.offset) + " + " + blockinst.name.upper() + "_BASE"
                        test_field["default"] = "0x%x" % (field.default << field.lsb)
                        test_field["mask"] = "0x%x"%((1<<(field.msb+1)) - (1<<(field.lsb)))
                        fields.append(test_field)
                        break
                else:
                    continue
            except:
                continue
            break

    test_parameters_list = []
    for block_instance in top_sys.block_instances:
        test_parameters = generate_test_parameters(block_instance)
        test_parameters_list.append(test_parameters)

    content = template.render(
        {
            "fields": fields
        }
    )

    with open(file_name, "w") as sfh:
        sfh.write(content)

    return
