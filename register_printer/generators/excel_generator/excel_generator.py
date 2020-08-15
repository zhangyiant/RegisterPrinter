import logging
import os.path

from openpyxl import Workbook


LOGGER = logging.getLogger(__name__)


class ExcelGenerator:

    def __init__(self, top_sys, output_path="."):
        self.top_sys = top_sys
        self.output_path = output_path
        return

    def collect_block_templates(self):
        block_templates = []
        for block in self.top_sys.blocks:
            if block.block_template not in block_templates:
                block_templates.append(block.block_template)
        return block_templates

    def generate(self):
        LOGGER.debug("Generating Excel files...")

        self.generate_top()

        blocks_path = os.path.join(self.output_path, "blocks")

        os.makedirs(blocks_path, exist_ok=True)

        block_templates = self.collect_block_templates()

        for block_template in block_templates:
            LOGGER.debug(
                "Generate excel block template %s",
                block_template.block_type
            )
            filename = os.path.join(
                blocks_path,
                '{0}.xlsx'.format(
                    block_template.block_type
                )
            )
            self.generate_block_template(
                filename,
                block_template
            )

        return

    def generate_block_template(
            self,
            filename,
            block_template):
        LOGGER.debug(
            "Generate file: %s for block template %s",
            filename,
            block_template.block_type)
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
