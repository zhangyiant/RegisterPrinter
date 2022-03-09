import textwrap

from register_printer.data_model.utility import msb_to_bytes
from .field import Field
from .utility import msb_to_bytes


class Register:
    def __init__(self, offset):
        self.offset = offset
        self.name = ""
        self.description = ""
        self.is_reserved = False
        self.fields = []
        return

    def calculate_register_default(self):
        value = 0
        for field in self.fields:
            pos = field.lsb
            val = field.default
            value = value | (val << pos)
        return value

    @property
    def size(self):
        if self.is_reserved:
            return 1
        biggest_msb = 0
        for field in self.fields:
            msb = field.msb
            if msb > biggest_msb:
                biggest_msb = msb
        num_of_bytes = msb_to_bytes(biggest_msb)
        return num_of_bytes

    def __str__(self):
        if self.is_reserved:
            result = "Register: RESERVED\n"
        else:
            result = "Register: " + str(self.name) + "\n"
        result += "    offset: " + ("0x%x" % self.offset) + "\n"
        result += "    size: " + str(self.size) + " bytes\n"
        result += "    description: " \
            + str(self.description) \
            + "\n"
        result += "    Fields:\n"
        field_strings = []
        for field in self.fields:
            field_string = str(field)
            field_string = textwrap.indent(field_string, "        ")
            field_strings.append(field_string)
        result += "\n".join(field_strings)
        return result

    @staticmethod
    def from_register_template(offset, register_template):
        register = Register(offset)
        register.name = register_template.name
        register.description = register_template.description
        for field_template in register_template.fields:
            field = Field.from_field_template(field_template)
            register.fields.append(field)
        return register

    @staticmethod
    def create_reserved_register(offset):
        register = Register(offset)
        register.is_reserved = True
        return register
