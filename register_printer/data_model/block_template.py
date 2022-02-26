import logging
import textwrap

from .register_template import RegisterTemplate
from .field_template import FieldTemplate
from .array_template import ArrayTemplate
from .register import Register


LOGGER = logging.getLogger(__name__)

def generate_block_template(block_template_dict):
    block_template = BlockTemplate(
        block_template_dict["blockType"]
    )
    for register_dict in block_template_dict["registers"]:
        register = RegisterTemplate(
            register_dict["name"],
            register_dict["offset"],
            register_dict["description"]
        )
        for field_dict in register_dict["fields"]:
            field = FieldTemplate(
                field_dict["name"],
                field_dict["msb"],
                field_dict["lsb"],
                field_dict["defaultValue"],
                field_dict["access"],
                field_dict["description"]
            )
            register.add_field(field)
        block_template.add_register(register)
    for array_dict in block_template_dict["arrays"]:
        array = ArrayTemplate.from_dict(array_dict)
        block_template.add_array(array)
    return block_template


class BlockTemplate:

    def __init__(self, block_type):
        self._block_type = block_type
        self.registers = []
        self.arrays = []
        return

    @property
    def block_type(self):
        return self._block_type

    def add_register(self, register):
        self.registers.append(register)
        self.sort_register_by_offset()
        return

    def add_array(self, array):
        self.arrays.append(array)
        return

    def find_register_by_name(self, name):
        for register in self.registers:
            if register.name == name:
                return register
        return None

    def find_register_template_by_offset(self, offset):
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
            registers.append(self.find_register_template_by_offset(offset))
        self.registers = registers
        return

    def generate_register_by_offset(self, offset):
        LOGGER.debug("Generate register by offset: 0x%x", offset)
        register_template = self.find_register_template_by_offset(offset)
        if register_template is not None:
            register = Register(offset, register_template=register_template)
        else:
            register = Register(offset, reserved=True)
        return register

    def __str__(self):
        result = "Block Template: " + str(self._block_type) + "\n"

        if len(self.arrays) > 0:
            result += "    Arrays:\n"
            array_strings = []
            for array in self.arrays:
                array_string = str(array)
                array_string = textwrap.indent(array_string, "        ")
                array_strings.append(array_string)
            result += "\n".join(array_strings)
            result += "\n"
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
