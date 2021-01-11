import textwrap

from .register import Register
from .field import Field


def generate_block_template(block_template_dict):
    block_template = BlockTemplate(
        block_template_dict["blockType"]
    )
    for register_dict in block_template_dict["registers"]:
        register = Register(
            register_dict["name"],
            register_dict["offset"],
            register_dict["description"]
        )
        for field_dict in register_dict["fields"]:
            field = Field(
                field_dict["name"],
                field_dict["msb"],
                field_dict["lsb"],
                field_dict["defaultValue"],
                field_dict["access"],
                field_dict["description"]
            )
            register.add_field(field)
        block_template.add_register(register)
    return block_template


class BlockTemplate:

    def __init__(self, block_type):
        self._block_type = block_type
        self.registers = []
        return

    @property
    def block_type(self):
        return self._block_type

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
        result = "Block Template" + str(self._block_type) + "\n"
        result += "    Registers:\n"
        register_strings = []
        for register in self.registers:
            register_string = str(register)
            register_string = textwrap.indent(register_string, "        ")
            register_strings.append(register_string)
        result += "\n".join(register_strings)
        return result

    @staticmethod
    def from_dict(block_template_dict):
        return generate_block_template(block_template_dict)

    def to_dict(self):
        result = {
            "blockType": self.block_type,
            "registers": []
        }
        for register in self.registers:
            register_dict = register.to_dict()
            result["registers"].append(register_dict)
        return result
