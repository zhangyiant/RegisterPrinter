import logging
import os.path

from openpyxl import Workbook


LOGGER = logging.getLogger(__name__)


class ExcelGenerator:

    def __init__(self, top_sys, output_path="."):
        self.top_sys = top_sys
        self.output_path = output_path
        return

    def generate(self):
        LOGGER.debug("Generating Excel files...")

        self.generate_top()

        blocks_path = os.path.join(self.output_path, "blocks")

        os.makedirs(blocks_path, exist_ok=True)

        block_templates = self.top_sys.block_templates

        for block_template in block_templates:
            filename = os.path.join(
                blocks_path,
                '{0}.xlsx'.format(
                    block_template.block_type
                )
            )
            ExcelGenerator.generate_block_template(
                filename,
                block_template
            )

        return

    @staticmethod
    def generate_block_template(
            filename,
            block_template):
        LOGGER.debug(
            "Generate file: %s for block template %s",
            filename,
            block_template.block_type)

        wb = Workbook()
        ws = wb.active

        ws.title = block_template.block_type

        ws.cell(1, 1).value = "Module description:"
        current_row = 3
        ws.cell(current_row, 1).value = "Offset"
        ws.cell(current_row, 2).value = "Name"
        ws.cell(current_row, 3).value = "MSB"
        ws.cell(current_row, 4).value = "LSB"
        ws.cell(current_row, 5).value = "Field Name"
        ws.cell(current_row, 6).value = "Access"
        ws.cell(current_row, 7).value = "Default Value"
        ws.cell(current_row, 8).value = "Description"
        current_row = 4
        for register in block_template.register_templates:
            offset_cell = ws.cell(current_row, 1)
            offset_cell.value = hex(register.offset)
            name_cell = ws.cell(current_row, 2)
            name_cell.value = register.name
            description_cell = ws.cell(current_row, 8)
            description_cell.value = register.description
            current_row += 1
            for field in register.fields:
                msb_cell = ws.cell(current_row, 3)
                msb_cell.value = field.msb
                lsb_cell = ws.cell(current_row, 4)
                lsb_cell.value = field.lsb
                field_name_cell = ws.cell(current_row, 5)
                field_name_cell.value = field.name
                access_cell = ws.cell(current_row, 6)
                access_cell.value = field.access
                default_value_cell = ws.cell(current_row, 7)
                default_value_cell.value = hex(field.default)
                field_description_cell = ws.cell(current_row, 8)
                field_description_cell.value = field.description
                current_row += 1
            # Add an empty line
            current_row += 1
        wb.save(filename=filename)

        return

    def generate_top(self):
        filename = os.path.join(
            self.output_path,
            "top.xlsx"
        )

        LOGGER.debug(
            "Generating Top excel to %s",
            filename)

        wb = Workbook()
        ws = wb.active
        ws.title = "Top"

        ws["A1"] = "Top"
        ws["B1"] = "Top_Module"
        ws["A2"] = "AddrWidth"
        ws["B2"] = self.top_sys.addr_width
        ws["A3"] = "DataWidth"
        ws["B3"] = self.top_sys.data_width
        ws["A4"] = "Author"
        ws["B4"] = self.top_sys.author
        ws["A5"] = "Version"
        ws["B5"] = self.top_sys.version

        # starting from row 8
        row = 8
        for block_instance in self.top_sys.block_instances:
            name_cell = ws.cell(row, 1)
            name_cell.value = block_instance.name
            type_cell = ws.cell(row, 2)
            type_cell.value = block_instance.block.block_type
            base_address_cell = ws.cell(row, 3)
            base_address_cell.value = hex(block_instance.base_address)
            size_cell = ws.cell(row, 4)
            size_cell.value = hex(block_instance.size)
            addr_width_cell = ws.cell(row, 5)
            raw_addr_width = block_instance.block.raw_addr_width
            if raw_addr_width is None:
                addr_width_cell.value = ""
            else:
                addr_width_cell.value = raw_addr_width
            data_width_cell = ws.cell(row, 6)
            raw_data_width = block_instance.block.raw_data_width
            if raw_data_width is None:
                data_width_cell.value = ""
            else:
                data_width_cell.value = raw_data_width
            row += 1
        wb.save(filename=filename)
        return
