import os
import os.path
import logging
from register_printer.template_loader import get_template
from register_printer.data_model import Register, Array, Struct


LOGGER = logging.getLogger(__name__)

def get_full_registers(registers):
    # remove reserved registers
    # expand registers in Array
    result = []
    for register in registers:
        if isinstance(register, Register):
            if not register.is_reserved:
                result.append(register)
        elif isinstance(register, Array):
            if not isinstance(register.content_type, Struct):
                msg = "Unsupported: Content type in Array is not Struct."
                LOGGER.error(msg)
                raise Exception(msg)
            struct = register.content_type
            regs = get_full_registers(struct.registers)
            result.extend(regs)
        else:
            LOGGER.warning("Unsupported register type")
    return result

def print_uvm_block(block, out_path):
    uvm_block_name = block.block_type.lower() + "_reg_model"
    file_name = os.path.join(
        out_path,
        uvm_block_name + ".sv")

    if os.path.exists(file_name):
        os.remove(file_name)

    template = get_template("reg_model.sv")

    registers = get_full_registers(block.registers)

    content = template.render(
        {
            "uvm_block_name": block.block_type + "_reg_model",
            "address_width": block.addr_width,
            "data_width": block.data_width,
            "registers": registers
        }
    )

    with open(file_name, "w") as bfh:
        bfh.write(content)

    return
