import re
import os
import os.path
import logging
from register_printer.template_loader import get_template


LOGGER = logging.getLogger(__name__)


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
        tmp_register = {}
        tmp_register["name"] = reg.name
        tmp_register["fields"] = []
        rw_flds = []
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
        for fld in reg.fields:
            tmp_register["fields"].append(fld)
            if fld.access == "RW":
                rw_flds.append(fld)
            elif fld.access == "RC":
                rc_flds.append(fld)
            elif fld.access == "RO":
                ro_flds.append(fld)
            elif fld.access == "RS":
                rs_flds.append(fld)
            elif fld.access == "W1C":
                w1c_flds.append(fld)
            elif fld.access == "W0C":
                w0c_flds.append(fld)
            elif fld.access == "WC":
                wc_flds.append(fld)
            elif fld.access == "WO":
                wo_flds.append(fld)
            elif fld.access == "WRC":
                wrc_flds.append(fld)
            elif fld.access == "WRS":
                wrs_flds.append(fld)
            elif fld.access == "-":
                ro_flds.append(fld)
        tmp_register["rw_flds"] = rw_flds
        tmp_register["ro_flds"] = ro_flds
        tmp_register["rc_flds"] = rc_flds
        tmp_register["rs_flds"] = rs_flds
        tmp_register["w1c_flds"] = w1c_flds
        tmp_register["w0c_flds"] = w0c_flds
        tmp_register["wc_flds"] = wc_flds
        tmp_register["wo_flds"] = wo_flds
        tmp_register["wrc_flds"] = wrc_flds
        tmp_register["wrs_flds"] = wrs_flds
        tmp_registers.append(tmp_register)

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
