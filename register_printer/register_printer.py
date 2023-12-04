import logging
import os.path
import json
import re
from register_printer.data_model import (
    TopSys
)

from register_printer.parser import (
    parse_top_sys,
    parse_block_template_file_from_first_sheet,
    parse_top_sys_from_json)

from .generators import (
    ExcelGenerator,
    CHeaderGenerator,
    DocGenerator,
    RtlGenerator,
    UvmGenerator
)

from .get_version import get_version


LOGGER = logging.getLogger(__name__)


class RegisterPrinter:
    def __init__(
            self,
            config_file=None,
            excel_path=None,
            output_path=".",
            json_file=None,
            top_sys = None
        ):
        self.config_file = config_file
        self.excel_path = excel_path
        self.output_path = output_path
        self.json_file = json_file
        if self.config_file is not None:
            self.top_sys = parse_top_sys(self.config_file, self.excel_path)
        elif self.json_file is not None:
            self.top_sys = parse_top_sys_from_json(
                self.json_file)
        elif top_sys != None:
            self.top_sys = TopSys.from_dict(top_sys)
        else:
            raise Exception("Config file or JSON file must be provided")
        return

    def display_string(self):
        return str(self.top_sys)

    def display(self):
        output_string = self.display_string()
        lines = output_string.split("\n")
        for line in lines:
            print(line)
        return

    def parse(self, config_file, excel_path):
        return

    def generate_uvm(self):
        uvm_generator = UvmGenerator(
            self.top_sys,
            self.output_path
        )
        uvm_generator.generate()
        return

    def generate_rtl(self):
        rtl_generator = RtlGenerator(
            self.top_sys,
            self.output_path
        )
        rtl_generator.generate()
        return

    def generate_c_header(self):
        c_header_generator = CHeaderGenerator(
            self.top_sys,
            self.output_path
        )
        c_header_generator.generate()
        return

    def generate_document(self):
        doc_generator = DocGenerator(
            self.top_sys,
            self.output_path
        )
        doc_generator.generate()
        return

    def generate_json(self):
        rp_dict = self.top_sys.to_dict()
        json_doc = json.dumps(
            rp_dict,
            indent=4,
            ensure_ascii=False
        )
        filename = os.path.join(
            self.output_path,
            "register_printer.json")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(json_doc)
        return

    def generate_excel(self):
        LOGGER.debug("Generate excel files to %s", self.output_path)
        excel_generator = ExcelGenerator(self.top_sys, self.output_path)
        excel_generator.generate()
        return

    def add_excel(self,excel_path):
        if re.search(".xlsx", excel_path) is not None:
            temp_block_template_dict_list = parse_block_template_file_from_first_sheet(
                excel_path)
        with open(self.json_file, "r", encoding="utf-8") as json_file_handler:
            rp_dict = json.load(json_file_handler)
        for block_template in temp_block_template_dict_list:
            if block_template["blockType"] not in [item["blockType"] for item in rp_dict["blockTemplates"]] :
                rp_dict["blockTemplates"].append(block_template)
        json_doc = json.dumps(
            rp_dict,
            indent=4,
            ensure_ascii=False
        )
        filename = os.path.join(
            self.output_path,
            "register_printer.json")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(json_doc)
        os.remove(self.json_file)
        return

    @staticmethod
    def get_version():
        return get_version()
