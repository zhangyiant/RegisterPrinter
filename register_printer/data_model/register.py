import textwrap

class Register:
    def __init__(self, offset, data_width=32):
        self.offset = offset
        self.data_width = data_width
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

    def size(self):
        return self.data_width // 8

    def __str__(self):
        if self.is_reserved:
            result = "Register: RESERVED\n"
        else:
            result = "Register: " + str(self.name) + "\n"
        result += "    offset: " + ("0x%x" % self.offset) + "\n"
        result += "    data width: " + str(self.data_width)
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
