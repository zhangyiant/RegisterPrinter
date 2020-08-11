import textwrap
from .register import Register


class Block:
    def __init__(
            self,
            parent,
            block_template,
            addr_width=None,
            data_width=None):
        self.parent = parent
        self._block_template = block_template
        self._addr_width = addr_width
        self._data_width = data_width
        return

    @property
    def block_type(self):
        return self._block_template.block_type

    @property
    def addr_width(self):
        if self._addr_width is not None:
            return self._addr_width

        if self.parent is not None:
            return self.parent.addr_width

        return None

    @property
    def raw_addr_width(self):
        return self._addr_width

    @raw_addr_width.setter
    def raw_addr_width(self, value):
        self._addr_width = value
        return

    @property
    def data_width(self):
        if self._data_width is not None:
            return self._data_width

        if self.parent is not None:
            return self.parent.data_width

        return None

    @property
    def raw_data_width(self):
        return self._data_width

    @raw_data_width.setter
    def raw_data_width(self, value):
        self._data_width = value
        return

    @property
    def block_template(self):
        return self._block_template

    @block_template.setter
    def block_template(self, value):
        self._block_template = value
        return

    @property
    def registers(self):
        return self._block_template.registers

    def add_register(self, register):
        self._block_template.add_register(register)
        return

    def find_register_by_name(self, name):
        return self._block_template.find_register_by_name(
            name
        )

    def find_register_by_offset(self, offset):
        return self._block_template.find_register_by_offset(
            offset
        )

    def __str__(self):
        result = "Block " + str(self.block_type) + "\n"
        result += "    Address width: " + str(self.addr_width) + "\n"
        result += "    Data width   : " + str(self.data_width) + "\n"
        result += "    Registers:\n"
        register_strings = []
        for register in self.registers:
            register_string = str(register)
            register_string = textwrap.indent(register_string, "        ")
            register_strings.append(register_string)
        result += "\n".join(register_strings)
        return result

    def to_dict(self):
        result = {}
        result["name"] = self.block_type
        result["addressWidth"] = self.addr_width
        result["dataWidth"] = self.data_width
        result["registers"] = []
        for register in self.registers:
            result["registers"].append(register.to_dict())
        return result

    @staticmethod
    def from_dict(block_type_dict):
        name = block_type_dict["name"]
        addr_width = block_type_dict["addressWidth"]
        data_width = block_type_dict["dataWidth"]
        block_type = Block(
            block_type=name,
            addr_len=addr_width,
            data_len=data_width)
        registers_dict = block_type_dict["registers"]
        for register_dict in registers_dict:
            register = Register.from_dict(
                register_dict)
            block_type.registers.append(
                register)
        return block_type
