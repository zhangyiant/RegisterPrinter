import logging
import os

from register_printer.template_loader import get_template
from register_printer.data_model import Register, Array, Struct


LOGGER = logging.getLogger(__name__)

def get_filename(out_path, block):
    filename = os.path.join(
        out_path,
        "regs_" + block.block_type.lower() + ".h")
    return filename

def generate_array_structs(registers):
    c_structs = []
    for register in registers:
        if isinstance(register, Array):
            if not isinstance(register.content_type, Struct):
                msg = "Unsupported: Content type in Array is not Struct."
                LOGGER.error(msg)
                raise Exception(msg)
            struct = register.content_type
            c_struct = {}
            c_struct["name"] = struct.name + "_NAME"
            struct_fields = generate_struct_fields(struct.registers)
            c_struct["struct_fields"] = struct_fields
            c_structs.append(c_struct)
    return c_structs

def generate_struct_fields(registers):
    struct_fields = []
    rsvd_idx = 0
    accumulated_number_rsvd_register = 0
    for reg in registers:
        if isinstance(reg, Register):
            if reg.is_reserved:
                accumulated_number_rsvd_register += 1
            else:
                if accumulated_number_rsvd_register > 1:
                    struct_field = {
                        "type": "volatile const int",
                        "name": "RSVD%d[%d]" % (rsvd_idx, accumulated_number_rsvd_register)
                    }
                    struct_fields.append(struct_field)
                    rsvd_idx = rsvd_idx + 1
                    # reset accumulated_number_rsvd_register
                    accumulated_number_rsvd_register = 0
                struct_field = {
                    "type": "volatile int",
                    "name": reg.name.upper()
                }
                struct_fields.append(struct_field)
        elif isinstance(reg, Array):
            if not isinstance(reg.content_type, Struct):
                msg = "Unsupported: Content type in Array is not Struct."
                LOGGER.error(msg)
                raise Exception(msg)
            struct = reg.content_type
            struct_field = {
                "type": (struct.name + "_NAME").upper(),
                "name": (struct.name).upper() + f"[{reg.length}]"
            }
            struct_fields.append(struct_field)
        else:
            LOGGER.warning("Unsupported register type.")
    return struct_fields


def generate_pos_mask_macros_from_array(array):
    if not isinstance(array.content_type, Struct):
        msg = "Unsupported: Content type in Array is not Struct."
        LOGGER.error(msg)
        raise Exception(msg)
    struct = array.content_type
    registers = struct.registers
    pos_mask_macros = generate_pos_mask_macros(registers)
    return pos_mask_macros

def generate_pos_mask_macros(registers):
    pos_mask_macros = []
    for reg in registers:
        if isinstance(reg, Register):
            if reg.is_reserved:
                continue
            else:
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
        elif isinstance(reg, Array):
            tmp_pos_mask_macros = generate_pos_mask_macros_from_array(reg)
            pos_mask_macros.extend(tmp_pos_mask_macros)
        else:
            LOGGER.warning("Unsupported register type.")
    return pos_mask_macros


def print_c_header_block(block, out_path):

    LOGGER.debug("Print block %s C header...", block.block_type)

    file_name = get_filename(out_path, block)

    if os.path.exists(file_name):
        os.remove(file_name)

    c_structs = generate_array_structs(block.registers)

    struct_fields = generate_struct_fields(block.registers)

    pos_mask_macros = generate_pos_mask_macros(block.registers)

    template = get_template("c_header_block.h")

    content = template.render(
        {
            "block_type": block.block_type,
            "c_structs": c_structs,
            "struct_fields": struct_fields,
            "pos_mask_macros": pos_mask_macros
        }
    )

    with open(file_name, "w") as bfh:
        bfh.write(content)

    return
