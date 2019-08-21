from .top_sys import TopSys
from .block import Block
from .register import Register
from .field import Field

from .parse_config import parse_config
from .parse_excels import parse_excels
from .print_c_header import print_c_header
from .print_doc import print_doc


class RegisterPrinter:
    def __init__(self, config_file, excel_path):
        self.config_file = config_file
        self.excel_path = excel_path
        self.top_sys = parse_config(config_file)
        self.top_sys = parse_excels(self.top_sys, excel_path)
        # self._create_top_sys_for_test()
        return

    def _create_top_sys_for_test(self):
        self.top_sys = TopSys("abc")
        block = Block("block A", 25, 12, 32)
        register = Register("register 1", 23, "Register 1")
        field = Field("Field 1", 23, 12, 1, "RW", "Field1")
        register.add_field(field)
        field = Field("Field 2", 23, 12, 1, "RCCC", "Field2")
        register.add_field(field)
        block.add_register(register)
        register = Register("register 2", 24, "Register 2")
        field = Field("Field 3", 23, 12, 1, "RW", "Field3")
        register.add_field(field)
        field = Field("Field 4", 32, 12, 1, "RCCC", "Field4")
        register.add_field(field)
        block.add_register(register)
        self.top_sys.add_block(block)
        block = Block("block B", 33, 24, 64)
        register = Register("register 3", 25, "Register 3")
        field = Field("Field 5", 23, 12, 1, "RW", "Field5")
        register.add_field(field)
        field = Field("Field 6", 32, 12, 1, "RO", "Field6")
        register.add_field(field)
        block.add_register(register)
        register = Register("register 4", 26, "Register 4")
        field = Field("Field 7", 24, 12, 1, "RW", "Field7")
        register.add_field(field)
        field = Field("Field 8", 64, 6, 1, "RCCC", "Field8")
        register.add_field(field)
        block.add_register(register)
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
        print_c_header(self.top_sys)
        return

    def generate_document(self):
        print_doc(self.top_sys)
        return
