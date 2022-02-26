from enum import Enum
import textwrap


class RegisterType(Enum):
    NORMAL = 1
    RESERVED = 2
    ARRAY = 3

class Register:
    def __init__(self, offset, reserved=False, register_template=None, array_template=None):
        self._offset = offset
        self._register_template = register_template
        self._array_template = array_template
        if reserved:
            self._type = RegisterType.RESERVED
        else:
            if self.array_template is not None:
                self._type = RegisterType.ARRAY
            else:
                self._type = RegisterType.NORMAL
        self.array_index = None
        self.fields = []
        return

    @property
    def name(self):
        if self._type != RegisterType.RESERVED:
            return self._register_template.name
        return None

    @property
    def offset(self):
        return self._offset

    @property
    def description(self):
        if self._type != RegisterType.RESERVED:
            return self._register_template.description
        return None

    def calculate_register_default(self):
        value = 0
        for field in self.fields:
            pos = field.lsb
            val = field.default
            value = value | (val << pos)
        return value

    def __str__(self):
        result = "Register " + str(self.name) + "\n"
        result += "    offset: " + ("0x%x" % self.offset) + "\n"
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

    def to_dict(self):
        result = {}
        result["name"] = self.name
        result["offset"] = self.offset
        result["description"] = self.description
        result["fields"] = []
        for field in self.fields:
            result["fields"].append(field.to_dict())
        return result
