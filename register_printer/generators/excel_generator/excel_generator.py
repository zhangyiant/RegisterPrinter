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

        wb.save(filename=filename)
        return
