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

def get_struct_list(registers):
    structs= []
    for register in registers:
        if isinstance(register, Array):
            if not isinstance(register.content_type, Struct):
                msg = "Unsupported: Content type in Array is not Struct."
                LOGGER.error(msg)
                raise Exception(msg)
            struct = register.content_type
            struct_dict = {}
            struct_dict["name"] = struct.name
            struct_dict["registers"] = []
            for reg in struct.registers:
                if isinstance(reg, Register):
                    # only support 1 level nesting
                    if not reg.is_reserved:
                        register_dict = {}
                        register_dict["name"] = reg.name
                        register_dict["offset"] = reg.offset
                        struct_dict["registers"].append(register_dict)
            structs.append(struct_dict)
    return structs


def get_uvm_block(block):
    result = {}
    result["name"] = (block.block_type + "_reg_model").lower()
    result["registers"] = []
    for register in block.registers:
        if isinstance(register, Register):
            if not register.is_reserved:
                reg_dict = {}
                reg_dict["name"] = register.name
                reg_dict["offset"] = register.offset
                reg_dict["start_address"] = 0
                reg_dict["is_struct"] = False
                reg_dict["length"] = 0
                reg_dict["default_overwrites"] = []
                result["registers"].append(reg_dict)
        elif isinstance(register, Array):
            if not isinstance(register.content_type, Struct):
                msg = "Unsupported: Content type in Array is not Struct."
                LOGGER.error(msg)
                raise Exception(msg)
            struct = register.content_type
            reg_dict = {}
            reg_dict["name"] = struct.name
            reg_dict["start_address"] = register.start_address
            reg_dict["offset"] = register.offset
            reg_dict["is_struct"] = True
            reg_dict["length"] = register.length
            reg_dict["default_overwrites"] = []
            for overwrite in register.default_overwrite_entries:
                overwrite_dict = {}
                overwrite_dict["index"] = overwrite.index
                overwrite_dict["register_name"] = overwrite.register_name
                overwrite_dict["field_name"] = overwrite.field_name
                overwrite_dict["default"] = overwrite.default
                reg_dict["default_overwrites"].append(overwrite_dict)
            result["registers"].append(reg_dict)
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

    structs = get_struct_list(block.registers)

    uvm_block = get_uvm_block(block)

    content = template.render(
        {
            "uvm_block": uvm_block, 
            "address_width": block.addr_width,
            "data_width": block.data_width,
            "registers": registers,
            "structs": structs
        }
    )

    with open(file_name, "w") as bfh:
        bfh.write(content)

    return
