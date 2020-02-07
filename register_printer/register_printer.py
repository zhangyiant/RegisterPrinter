from .parse_config import parse_top_sys
import os.path
import json


class RegisterPrinter:
    def __init__(self, config_file, excel_path, output_path="."):
        self.config_file = config_file
        self.excel_path = excel_path
        self.output_path = output_path
        self.top_sys = parse_top_sys(self.config_file, self.excel_path)
        return

    def display_string(self):
        return str(self.top_sys)

    def display(self):
        print(self.top_sys)
        return

    def parse(self, config_file, excel_path):
        return

    def generate_uvm(self):
        self.top_sys.print_uvm(self.output_path)
        return

    def generate_rtl(self):
        self.top_sys.print_rtl(self.output_path)
        return

    def generate_c_header(self):
        self.top_sys.print_c_header(self.output_path)
        return

    def generate_document(self):
        self.top_sys.print_doc(self.output_path)
        return

    def generate_json(self):
        rp_dict = self.top_sys.to_dict()
        json_doc = json.dumps(rp_dict, indent=4)
        filename = os.path.join(
            self.output_path,
            "register_printer.json")
        with open(filename, "w") as f:
            f.write(json_doc)
        return
