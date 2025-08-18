import os
import os.path
import logging
from register_printer.template_loader import get_template
from register_printer.data_model import Register, Array, Struct
import re


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
    structs = []
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
                reg_dict["hdl_name"] = register.hdl_name
                reg_dict["offset"] = register.offset
                reg_dict["start_address"] = 0
                reg_dict["is_struct"] = False
                reg_dict["length"] = 0
                reg_dict["default_overwrites"] = []
                reg_dict["registers"] = [register]
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
            reg_dict["registers"] = get_full_registers(struct.registers)
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
    registers = get_full_registers(block.registers)
    for register in registers:
        register.hdl_name = register.name
        if not re.match("^"+block.block_type+"_",register.name,re.IGNORECASE):
            register.name = block.block_type+"_"+register.name

    structs = get_struct_list(block.registers)
    uvm_block = get_uvm_block(block)

    uvm_block_name = block.block_type.lower() + "_reg_model"
    file_name = os.path.join(
        out_path,
        uvm_block_name + ".sv")
    gen_reg_model(uvm_block, block.addr_width, block.data_width, registers, structs, block.block_type.lower(), file_name)
    
    hdl_dir = os.path.join(
        out_path,
        "hdl")
    os.makedirs(hdl_dir, exist_ok=True)
    uvm_block_name = block.block_type.lower() + "_hdl"
    file_name = os.path.join(
        hdl_dir,
        uvm_block_name + ".svh")
    gen_hdl(uvm_block, block.addr_width, block.data_width, registers, block.block_type.lower(), file_name)

    file_name = os.path.join(
        out_path,
        block.block_type.lower() + "_reg_vars.svh")
    gen_reg_vars(uvm_block, block.addr_width, block.data_width, registers, structs, file_name)

    file_name = os.path.join(
        out_path,
        block.block_type.lower() + "_reg_vars_def_cons.svh")
    gen_reg_vars_def_cons(uvm_block, block.addr_width, block.data_width, registers, structs, file_name)

    file_name = os.path.join(
        out_path,
        block.block_type.lower() + "_reg_cfg_body.svh")
    gen_reg_cfg_body(uvm_block, block.addr_width, block.data_width, registers, structs, file_name)

    file_name = os.path.join(
        out_path,
        block.block_type.lower() + "_cfg_base_seq.sv")
    gen_cfg_base_seq(block.block_type.lower(), file_name)
    
    gen_field_cfg_seq(block.block_type.lower(), uvm_block, out_path)

    file_name = os.path.join(
        out_path,
        block.block_type.lower() + "_reg_covergroup.svh")
    gen_reg_covergroup(uvm_block, block.addr_width, block.data_width, registers, structs, file_name)

    return

def gen_reg_model(block, block_addr_width, block_data_width, registers, structs, block_type, file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
    template = get_template("reg_model.sv")
    content = template.render(
        {
            "uvm_block": block,
            "address_width": block_addr_width,
            "data_width": block_data_width,
            "registers": registers,
            "block_type": block_type,
            "structs": structs
        }
    )

    with open(file_name, "w") as bfh:
        bfh.write(content)

def gen_reg_vars(block, block_addr_width, block_data_width, registers, structs, file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
    template = get_template("reg_vars.sv")
    content = template.render(
        {
            "uvm_block": block,
        }
    )

    with open(file_name, "w") as bfh:
        bfh.write(content)

def gen_reg_vars_def_cons(block, block_addr_width, block_data_width, registers, structs, file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
    template = get_template("reg_vars_def_cons.sv")
    content = template.render(
        {
            "uvm_block": block,
        }
    )

    with open(file_name, "w") as bfh:
        bfh.write(content)

def gen_reg_cfg_body(block, block_addr_width, block_data_width, registers, structs, file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
    template = get_template("reg_cfg_body.sv")
    content = template.render(
        {
            "uvm_block": block,
        }
    )

    with open(file_name, "w") as bfh:
        bfh.write(content)


def gen_cfg_base_seq(name, file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
    template = get_template("cfg_base_seq.sv")
    content = template.render(
        {
            "name": name,
        }
    )

    with open(file_name, "w") as bfh:
        bfh.write(content)

def gen_reg_covergroup(block, block_addr_width, block_data_width, registers, structs, file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
    template = get_template("reg_covergroup.sv")
    content = template.render(
        {
            "uvm_block": block,
        }
    )

    with open(file_name, "w") as bfh:
        bfh.write(content)


def gen_field_cfg_seq(name, block, out_path):
    seq_dir = os.path.join(
        out_path,
        "cfg_seq")
    os.makedirs(seq_dir, exist_ok=True)
    template = get_template("field_cfg_base_seq.sv")
    for item in block["registers"]:
        for register in item["registers"]:
            for field in register.fields:
                if field.access == "RW" or field.access == "RWP":
                    file_name = os.path.join(
                        seq_dir,
                        f"{name.lower()}_{field.name.lower()}_seq.sv")
                    content = template.render(
                        {
                            "name": name,
                            "item": item,
                            "field": field,
                        }
                    )
                    with open(file_name, "w") as bfh:
                        bfh.write(content)

def gen_hdl(block, block_addr_width, block_data_width, registers, block_type, file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
    template = get_template("reg_hdl.sv")
    content = template.render(
        {
            "uvm_block": block,
            "address_width": block_addr_width,
            "data_width": block_data_width,
            "block_type": block_type,
            "registers": registers
        }
    )

    with open(file_name, "w") as bfh:
        bfh.write(content)
