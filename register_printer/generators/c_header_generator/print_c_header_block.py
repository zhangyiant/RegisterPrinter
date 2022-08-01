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
            c_struct["name"] = struct.name.upper() + "_TypeDef"
            struct_fields = generate_struct_fields(struct.registers)
            c_struct["struct_fields"] = struct_fields
            c_structs.append(c_struct)
    return c_structs


def get_union_fields(register):
    fields = register.fields
    fields_struct = []
    current_bit = 0
    register_bits = register.size * 8
    reserve_index = 0
    for field in fields:
        if field.lsb > current_bit:
            reserve_bits = field.lsb - current_bit
            field_type = "uint32_t"
            field_name = f"RSVD{reserve_index}"
            field_length = reserve_bits
            fields_struct.append({
                "type": field_type,
                "name": field_name,
                "length": field_length
            })
            current_bit = field.lsb
            reserve_index += 1
            field_type = "uint32_t"
            if field.name == "-":
                field_name = f"RSVD{reserve_index}"
                reserve_index += 1
            else:
                field_name = field.name.upper()
            field_length = field.size
            fields_struct.append({
                "type": field_type,
                "name": field_name,
                "length": field_length
            })
            current_bit = field.msb + 1
        elif field.lsb == current_bit:
            field_type = "uint32_t"
            if field.name == "-":
                field_name = f"RSVD{reserve_index}"
                reserve_index += 1
            else:
                field_name = field.name.upper()
            field_length = field.size
            fields_struct.append({
                "type": field_type,
                "name": field_name,
                "length": field_length
            })
            current_bit = field.msb + 1
        else:
            raise Exception("Error field lsb.")
    if current_bit < register_bits:
        reserve_bits = register_bits - current_bit
        field_type = "uint32_t"
        field_name = f"RSVD{reserve_index}"
        field_length = reserve_bits
        fields_struct.append({
            "type": field_type,
            "name": field_name,
            "length": field_length
        })
    return fields_struct


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
                    name = "RSVD%d[%d]" % \
                           (rsvd_idx, accumulated_number_rsvd_register)
                    struct_field = {
                        "category": "reserved",
                        "type": "const uint8_t",
                        "name": name
                    }
                    struct_fields.append(struct_field)
                    rsvd_idx = rsvd_idx + 1
                    # reset accumulated_number_rsvd_register
                    accumulated_number_rsvd_register = 0
                type_str = get_c_type_by_size(reg.size)
                fields = get_union_fields(reg)
                struct_field = {
                    "category": "register",
                    "type": type_str,
                    "name": reg.name.upper(),
                    "fields": fields
                }
                struct_fields.append(struct_field)
        elif isinstance(reg, Array):
            if accumulated_number_rsvd_register > 1:
                name = "RSVD%d[%d]" % \
                       (rsvd_idx, accumulated_number_rsvd_register)
                struct_field = {
                    "category": "reserved",
                    "type": "const uint8_t",
                    "name": name
                }
                struct_fields.append(struct_field)
                rsvd_idx = rsvd_idx + 1
                # reset accumulated_number_rsvd_register
                accumulated_number_rsvd_register = 0
            if not isinstance(reg.content_type, Struct):
                msg = "Unsupported: Content type in Array is not Struct."
                LOGGER.error(msg)
                raise Exception(msg)
            struct = reg.content_type
            struct_field = {
                "category": "array",
                "type": struct.name.upper() + "_TypeDef",
                "name": struct.name.upper() + f"[{reg.length}]"
            }
            struct_fields.append(struct_field)
        else:
            LOGGER.warning("Unsupported register type.")

    # write the last reserved register
    if accumulated_number_rsvd_register > 1:
        struct_field = {
            "category": "reserved",
            "type": "const uint8_t",
            "name": "RSVD%d[%d]" % (rsvd_idx, accumulated_number_rsvd_register)
        }
        struct_fields.append(struct_field)
        rsvd_idx = rsvd_idx + 1
        # reset accumulated_number_rsvd_register
        accumulated_number_rsvd_register = 0
    return struct_fields


def get_c_type_by_size(size):
    if size == 1:
        type_str = "uint8_t"
    elif size == 2:
        type_str = "uint16_t"
    elif size == 4:
        type_str = "uint32_t"
    return type_str


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
