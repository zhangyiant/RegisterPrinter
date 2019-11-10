from .parse_config import parse_config
from .parse_excels import parse_excels
from .print_c_header import print_c_header
from .print_uvm import print_uvm
from .print_doc import print_doc
from .print_rtl import print_rtl


class RegisterPrinter:
    def __init__(self, config_file, excel_path, output_path="."):
        self.config_file = config_file
        self.excel_path = excel_path
        self.output_path = output_path
        self.top_sys = parse_config(config_file)
        self.top_sys = parse_excels(self.top_sys, excel_path)
        return

    def display_string(self):
        return str(self.top_sys)

    def display(self):
        print(self.top_sys)
        return

    def parse(self, config_file, excel_path):
        return

    def generate_uvm(self):
        print_uvm(self.top_sys, self.output_path)
        return

    def generate_rtl(self):
        print_rtl(self.top_sys, self.output_path)
        return

    def generate_c_header(self):
        print_c_header(self.top_sys, self.output_path)
        return

    def generate_document(self):
        print_doc(self.top_sys, self.output_path)
        return
