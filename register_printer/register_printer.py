from .top_sys import TopSys


class RegisterPrinter:
    def __init__(self, config_file, excel_path):
        self.config_file = config_file
        self.excel_path = excel_path
        self.top_sys = TopSys("abc")
        return

    def display(self):
        print(self.top_sys)
        return

    def parse(self, config_file, excel_path):
        return

    def generate_uvm(self):
        return

    def generate_rtl(self):
        return

    def generate_c_header(self):
        return

    def generate_document(self):
        return
