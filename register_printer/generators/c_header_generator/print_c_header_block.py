import logging
import os

from register_printer.template_loader import get_template


LOGGER = logging.getLogger(__name__)

def get_filename(out_path, block):
    filename = os.path.join(
        out_path,
        "regs_" + block.block_type.lower() + ".h")
    return filename


def print_c_header_block(block, out_path):

    LOGGER.debug("Print block %s C header...", block.block_type)

    file_name = get_filename(out_path, block)

    if os.path.exists(file_name):
        os.remove(file_name)

    struct_fields = []
    rsvd_idx = 0
    accumulated_number_rsvd_register = 0
    for reg in block.mapped_registers:
        # Todo: reimplement this function
        if reg.type == "RegisterType.RESERVED":
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

    pos_mask_macros = []
    for reg in block.mapped_registers:
        if reg.type != RegisterType.RESERVED:
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

    template = get_template("c_header_block.h")

    content = template.render(
        {
            "block_type": block.block_type,
            "struct_fields": struct_fields,
            "pos_mask_macros": pos_mask_macros
        }
    )

    with open(file_name, "w") as bfh:
        bfh.write(content)

    return
