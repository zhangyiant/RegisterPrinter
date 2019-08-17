from .top_sys import TopSys
from .block import Block

class RegisterPrinter:
    def __init__(self, config_file, excel_path):
        self.config_file = config_file
        self.excel_path = excel_path
        self._create_top_sys_for_test()
        return

    def _create_top_sys_for_test(self):
        self.top_sys = TopSys("abc")
        block = Block("block A", 25, 12, 32)
        self.top_sys.add_block(block)
        block = Block("block B", 33, 24, 64)
        self.top_sys.add_block(block)
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
