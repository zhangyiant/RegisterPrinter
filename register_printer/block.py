import textwrap
from .register import *

class Block:
    def __init__(self, block_type, size, addr_len, data_len):
        self._block_type = block_type
        self._size = size
        self._addr_len = addr_len
        self._data_len = data_len
        self.registers = []
        return

    @property
    def block_type(self):
        return self._block_type

    @property
    def size(self):
        return self._size

    @property
    def addr_len(self):
        return self._addr_len

    @property
    def data_len(self):
        return self._data_len

    def add_register(self, register):
        self.registers.append(register)
        self.sort_register_by_offset()
        return

    def find_register_by_name(self, name):
        for register in self.registers:
            if register.name == name:
                return register
        return None

    def find_register_by_offset(self, offset):
        for register in self.registers:
            if register.offset == offset:
                return register
        return None

    def sort_register_by_offset(self):
        offsets = []
        for register in self.registers:
            offsets.append(register.offset)
        offsets.sort()
        registers = []
        for offset in offsets:
            registers.append(self.find_register_by_offset(offset))
        self.registers = registers
        return

    def __str__(self):
        result = "Block " + str(self._block_type) + "\n"
        result += "    Size         : " + str(self._size) + "\n"
        result += "    Address width: " + str(self._addr_len) + "\n"
        result += "    Data width   : " + str(self._data_len) + "\n"
        result += "    Registers:\n"
        register_strings = []
        for register in self.registers:
            register_string = str(register)
            register_string = textwrap.indent(register_string, "        ")
            register_strings.append(register_string)
        result += "\n".join(register_strings)
        return result

