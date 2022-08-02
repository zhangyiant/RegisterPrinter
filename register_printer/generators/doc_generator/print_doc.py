import os
import os.path
import logging
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from register_printer.data_model import Register, Array, Field

LOGGER = logging.getLogger(__name__)


def print_doc_reg(reg, dh, reg_idx, blk_idx, blk_insts, array=None):
    dh.add_page_break()
    dh.add_heading("  %d.%d  %s" % (blk_idx, reg_idx + 1, reg.name), level=2)
    p = dh.add_paragraph()
    p.add_run('    Offset : ').bold = True
    if array is None:
        p.add_run('%s\n' % (hex(reg.offset)))
    else:
        offset_str = hex(
            reg.offset + array.start_address)
        offset_str += " + " + hex(array.offset) + " * n"
        offset_str += " (n >= 0, n < " + str(array.length) + ")"
        p.add_run('%s\n' % offset_str)

    for blk_inst in blk_insts:
        p.add_run('    %s Address : ' % (blk_inst.name)).bold = True
        if array is None:
            p.add_run('%s\n' % (hex(blk_inst.base_address + reg.offset)))
        else:
            addr = blk_inst.base_address + array.start_address + reg.offset
            p.add_run('%s\n' % hex(addr))

    p.add_run("    Reset Value : ").bold = True
    p.add_run("0x%x\n" % (reg.calculate_register_default()))
    if array is not None:
        for index in range(array.length):
            offset = array.start_address + array.offset * index + reg.offset
            temp_reg = Register(offset)
            temp_reg.name = reg.name
            for field in reg.fields:
                temp_reg.fields.append(field)
            found = False
            for overwrite_entry in array.default_overwrite_entries:
                if overwrite_entry.index == index and \
                        overwrite_entry.register_name == temp_reg.name:
                    found = True
                    field_name = overwrite_entry.field_name
                    for field in temp_reg.fields:
                        if field.name == field_name:
                            temp_reg.fields.remove(field)
                            new_field = Field()
                            new_field.name = field.name
                            new_field.msb = field.msb
                            new_field.lsb = field.lsb
                            new_field.default = overwrite_entry.default
                            new_field.access = field.access
                            new_field.description = field.description
                            temp_reg.fields.append(new_field)
            if found:
                p.add_run(
                    "           " +
                    hex(temp_reg.offset) + ":0x%x\n" %
                    temp_reg.calculate_register_default()
                )

    p.add_run("    Description : ").bold = True
    p.add_run("%s\n" % (reg.description))

    headers = [
        "LSB",
        "MSB",
        "Field",
        "Access",
        "Default",
        "Description"]
    row_count = 1
    for field in reg.fields:
        if field.name != "-":
            row_count += 1
    tb = dh.add_table(
        row_count,
        len(headers),
        style="Light Grid")
    tb.autofit = 1
    hcells = tb.rows[0].cells
    i = 0
    for header in headers:
        p = hcells[i].paragraphs[0]
        p.add_run(header)
        p.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        i += 1

    i = 1
    for field in reg.fields:
        if field.name == "-":
            continue
        tb.cell(i, 0).text = str(field.lsb)
        tb.cell(i, 1).text = str(field.msb)
        tb.cell(i, 2).text = str(field.name)
        tb.cell(i, 3).text = str(field.access)
        tb.cell(i, 4).text = hex(field.default)
        tb.cell(i, 5).text = "%s" % (field.description)
        i += 1
    return


def get_unreserved_non_array_register(block):
    result = []
    for register in block.registers:
        if isinstance(register, Array):
            result.append(register)
        elif isinstance(register, Register):
            if register.is_reserved:
                continue
            else:
                result.append(register)
    return result


def calc_row_num(registers):
    num = 0
    for register in registers:
        if isinstance(register, Array):
            struct = register.content_type
            for struct_register in struct.registers:
                if struct_register.is_reserved:
                    continue
                else:
                    num += 1
        else:
            num += 1
    return num


def print_doc_block(doc, idx, block, instances):
    block_type = block.block_type

    registers = get_unreserved_non_array_register(block)
    num_register = calc_row_num(registers)

    doc.add_heading("%d %s Registers" % (idx, block_type), level=1)
    tb = doc.add_table(
        num_register + 1,
        2 + len(instances),
        style="Light Grid")
    hcells = tb.rows[0].cells
    hdr = ["Offset"]
    for instance in instances:
        hdr.append("%s Addr" % instance.name)
    hdr.append("Register")
    for i in range(len(hdr)):
        p = hcells[i].paragraphs[0]
        p.add_run(hdr[i])
        p.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    i = 1
    for register in registers:
        if isinstance(register, Register):
            tb.cell(i, 0).text = hex(register.offset)
            for k in range(len(instances)):
                tb.cell(i, k + 1).text = hex(
                    instances[k].base_address + register.offset)
            tb.cell(i, len(hdr) - 1).text = str(register.name)
            i += 1
        elif isinstance(register, Array):
            struct = register.content_type
            for struct_registers in struct.registers:
                if struct_registers.is_reserved:
                    continue
                offset_str = hex(
                    struct_registers.offset + register.start_address)
                offset_str += " + " + hex(register.offset) + " * n"
                offset_str += " (n >= 0, n < " + str(register.length) + ")"
                tb.cell(i, 0).text = offset_str
                for k in range(len(instances)):
                    tb.cell(i, k + 1).text = hex(
                        instances[k].base_address + register.start_address +
                        struct_registers.offset
                    )
                tb.cell(i, len(hdr) - 1).text = str(struct_registers.name)
                i += 1

    reg_idx = 0
    for register in registers:
        if isinstance(register, Register):
            print_doc_reg(register, doc, reg_idx, idx, instances)
            reg_idx += 1
        if isinstance(register, Array):
            struct = register.content_type
            for struct_reg in struct.registers:
                if struct_reg.is_reserved:
                    continue
                print_doc_reg(
                    struct_reg,
                    doc,
                    reg_idx,
                    idx,
                    instances,
                    register
                )
                reg_idx += 1
    doc.add_page_break()
    return


def generate_doc(top_sys):
    doc = Document()

    title = doc.add_heading(
        top_sys.name + " Registers",
        level=0)
    title.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    p = doc.add_paragraph()
    p.add_run("Version : %s\n" % top_sys.version)
    p.add_run("Author : %s" % top_sys.author)
    p.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    doc.add_page_break()

    block_idx = 1
    doc.add_heading("%d Address Map" % block_idx, level=1)
    table = doc.add_table(
        len(top_sys.block_instances) + 1,
        3,
        style="Light Grid")
    hcell = table.rows[0].cells
    headers = ["Block", "Start Address", "Size"]
    for i in range(3):
        p = hcell[i].paragraphs[0]
        p.add_run(headers[i])
        p.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    i = 1
    for block_instance in top_sys.block_instances:
        table.cell(i, 0).text = block_instance.name
        table.cell(i, 1).text = hex(block_instance.base_address)
        table.cell(i, 2).text = hex(block_instance.size)
        i += 1
    doc.add_page_break()

    block_idx += 1
    for block in top_sys.blocks:
        block_type = block.block_type
        blk_insts = []
        for instance in top_sys.block_instances:
            if instance.block_type == block_type:
                blk_insts.append(instance)

        print_doc_block(doc, block_idx, block, blk_insts)
        block_idx = block_idx + 1
    return doc


def print_doc(top_sys, output_path="."):
    LOGGER.debug("Generating register description document...")

    doc_file_name = os.path.join(
        output_path,
        top_sys.name.lower() + "_registers.docx"
    )
    if os.path.exists(doc_file_name):
        os.remove(doc_file_name)

    doc = generate_doc(top_sys)

    doc.save(doc_file_name)

    LOGGER.debug(
        "Register description document is generated %s",
        doc_file_name
    )
    return
