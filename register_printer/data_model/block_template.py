import logging
import textwrap

from .register_template import RegisterTemplate
from .field_template import FieldTemplate
from .array_template import ArrayTemplate
from .register import Register
from .field import Field
from .array import Array, DefaultOverwriteEntry
from .struct import Struct

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
        self.register_templates = []
        self.array_templates = []
        return

    @property
    def block_type(self):
        return self._block_type

    def add_register(self, register):
        self.register_templates.append(register)
        self.sort_register_by_offset()
        return

    def add_array(self, array):
        self.array_templates.append(array)
        return

    def find_register_template_by_offset(self, offset):
        for register in self.register_templates:
            if register.offset == offset:
                return register
        return None

    def get_array_template_by_offset(self, offset):
        result = None
        for array_template in self.array_templates:
            start_address = array_template.array_start_address
            stop_address = array_template.array_stop_address
            if offset >=start_address and offset < stop_address:
                result = array_template
        return result

    def sort_register_by_offset(self):
        offsets = []
        for register in self.register_templates:
            offsets.append(register.offset)
        offsets.sort()
        registers = []
        for offset in offsets:
            registers.append(self.find_register_template_by_offset(offset))
        self.register_templates = registers
        return

    def get_minimum_block_size(self, data_width):
        biggest_offset = self._biggest_register_offset()
        array_template = self.get_array_template_by_offset(biggest_offset)
        if array_template is None:
            return biggest_offset + data_width // 8
        else:
            return array_template.array_stop_address

    def _biggest_register_offset(self):
        result = 0
        for register in self.register_templates:
            if register.offset > result:
                result = register.offset
        return result

    def _get_register_by_offset(self, offset):
        # offset must not in range of an array
        register = None
        register_template = self.find_register_template_by_offset(
            offset
        )
        if register_template is not None:
            register = Register.from_register_template(
                offset,
                register_template
            )
        else:
            register = Register.create_reserved_register(offset)
        return register

    def _get_array_by_array_template(self, array_template):
        start_address = array_template.start_address
        offset = start_address
        struct = Struct(array_template.name)
        while offset < start_address + array_template.offset:
            register_template = self.find_register_template_by_offset(offset)
            if register_template is None:
                register = Register.create_reserved_register(
                    offset - start_address,
                )
            else:
                register = Register.from_register_template(
                    offset - start_address,
                    register_template
                )
            struct.registers.append(register)
            offset += register.size
        array = Array(
            struct,
            array_template.length,
            array_template.start_address
        )
        while offset < array_template.array_stop_address:
            register_template = self.find_register_template_by_offset(offset)
            if register_template is None:
                offset += 1
                continue
            index = (register_template.offset - start_address) // array_template.offset
            register_name = register_template.name
            for field_template in register_template.fields:
                field_name = field_template.name
                default = field_template.default
                default_overwrite_entry = DefaultOverwriteEntry()
                default_overwrite_entry.index = index
                default_overwrite_entry.register_name = register_name
                default_overwrite_entry.field_name = field_name
                default_overwrite_entry.default = default
                array.default_overwrite_entries.append(default_overwrite_entry)
            offset += register_template.num_of_bytes
        return array

    def generate_registers(self, data_width):
        registers = []
        block_size = self.get_minimum_block_size(data_width)
        LOGGER.debug("Blocksize %s", block_size)
        offset = 0
        while offset < block_size:
            array_template = self.get_array_template_by_offset(offset)
            if array_template is not None:
                array = self._get_array_by_array_template(array_template)
                registers.append(array)
                offset += array_template.size
                continue

            register = self._get_register_by_offset(offset)
            registers.append(register)

            offset += register.size
        return registers

    def generate_register_by_offset(self, offset):
        register_template = self.find_register_template_by_offset(offset)
        if register_template is not None:
            register = Register(offset, register_template=register_template)
            for field_template in register_template.fields:
                field = Field(field_template=field_template)
                register.fields.append(field)
        else:
            if offset > self._biggest_register_offset():
                register = None            
            else:
                register = Register(offset, reserved=True)
        return register

    def __str__(self):
        result = "Block Template: " + str(self._block_type) + "\n"

        if len(self.array_templates) > 0:
            result += "    Arrays:\n"
            array_strings = []
            for array in self.array_templates:
                array_string = str(array)
                array_string = textwrap.indent(array_string, "        ")
                array_strings.append(array_string)
            result += "\n".join(array_strings)
            result += "\n"
        result += "    Registers:\n"
        register_strings = []
        for register in self.register_templates:
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
        for register in self.register_templates:
            register_dict = register.to_dict()
            result["registers"].append(register_dict)
        return result
