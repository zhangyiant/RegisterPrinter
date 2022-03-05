import os
import os.path
import logging
from register_printer.template_loader import get_template
from register_printer.data_model import Register, Array, Struct


LOGGER = logging.getLogger(__name__)


def get_register_dict_from_register(register):
    tmp_register = {}
    tmp_register["name"] = register.name
    tmp_register["fields"] = []
    tmp_register["offset"] = register.offset
    rw_flds = []
    rwp_flds = []
    ro_flds = []
    rc_flds = []
    rs_flds = []
    w1c_flds = []
    w0c_flds = []
    wc_flds = []
    wo_flds = []
    wrc_flds = []
    wrs_flds = []
    #rsc_flds = []
    for fld in register.fields:
        field_dict = {}
        field_dict["name"] = fld.name
        field_dict["msb"] = fld.msb
        field_dict["lsb"] = fld.lsb
        field_dict["default"] = fld.default
        field_dict["access"] = fld.access
        field_dict["description"] = fld.description
        tmp_register["fields"].append(field_dict)
        if fld.access == "RW":
            rw_flds.append(field_dict)
        elif fld.access == "RWP":
            rwp_flds.append(field_dict)
        elif fld.access == "RC":
            rc_flds.append(field_dict)
        elif fld.access == "RO":
            ro_flds.append(field_dict)
        elif fld.access == "RS":
            rs_flds.append(field_dict)
        elif fld.access == "W1C":
            w1c_flds.append(field_dict)
        elif fld.access == "W0C":
            w0c_flds.append(field_dict)
        elif fld.access == "WC":
            wc_flds.append(field_dict)
        elif fld.access == "WO":
            wo_flds.append(field_dict)
        elif fld.access == "WRC":
            wrc_flds.append(field_dict)
        elif fld.access == "WRS":
            wrs_flds.append(field_dict)
        elif fld.access == "-":
            ro_flds.append(field_dict)
    tmp_register["rw_flds"] = rw_flds
    tmp_register["rwp_flds"] = rwp_flds
    tmp_register["ro_flds"] = ro_flds
    tmp_register["rc_flds"] = rc_flds
    tmp_register["rs_flds"] = rs_flds
    tmp_register["w1c_flds"] = w1c_flds
    tmp_register["w0c_flds"] = w0c_flds
    tmp_register["wc_flds"] = wc_flds
    tmp_register["wo_flds"] = wo_flds
    tmp_register["wrc_flds"] = wrc_flds
    tmp_register["wrs_flds"] = wrs_flds
    return tmp_register


def update_default(register_dict, index, overwrite_entries):
    for overwrite_entry in overwrite_entries:
        if overwrite_entry.index != index:
            continue
        if register_dict["name"] != overwrite_entry.register_name:
            continue
        for field in register_dict["fields"]:
            if field["name"] == overwrite_entry.field_name:
                field["default"] = overwrite_entry.default
    return

def print_rtl_block(block, out_path):
    file_name = os.path.join(
        out_path,
        block.block_type + "_reg.sv")

    if os.path.exists(file_name):
        os.remove(file_name)

    LOGGER.debug("Generating RTL %s", block.block_type)

    template = get_template("reg_rtl.sv")

    tmp_registers = []
    for reg in block.registers:
        if isinstance(reg, Register):
            if not reg.is_reserved:
                register_dict = get_register_dict_from_register(
                    reg
                )
                tmp_registers.append(register_dict)
        elif isinstance(reg, Array):
            if not isinstance(reg.content_type, Struct):
                msg = "Unsupported: Content type in Array is not Struct."
                LOGGER.error(msg)
                raise Exception(msg)
            struct = reg.content_type
            for idx in range(reg.length):
                for struct_reg in struct.registers:
                    if not struct_reg.is_reserved:
                        tmp_register_dict = get_register_dict_from_register(
                            struct_reg
                        )
                        # Update default before register/field name update.
                        update_default(tmp_register_dict, idx, reg.default_overwrite_entries)
                        tmp_register_dict["name"] = f"{struct_reg.name}_{idx}"
                        tmp_register_dict["offset"] = reg.start_address + idx * reg.offset + struct_reg.offset
                        for field_dict in tmp_register_dict["fields"]:
                            field_dict["name"] = f'{struct_reg.name}_{idx}_{field_dict["name"]}'
                        tmp_registers.append(tmp_register_dict)
        else:
            LOGGER.warning("Unsupported register type!")

    content = template.render(
        {
            "block": block,
            "registers": tmp_registers
        }
    )

    with open(file_name, "w") as bfh:
        bfh.write(content)

    return


def print_rtl(top_sys, output_path="."):

    LOGGER.debug("Generating register RTL files...")

    out_dir = os.path.join(
        output_path,
        'regrtls')

    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    for block in top_sys.blocks:
        print_rtl_block(block, out_dir)

    LOGGER.debug("Register RTL files are generated in directory %s", out_dir)
    return
