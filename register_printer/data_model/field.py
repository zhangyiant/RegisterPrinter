from register_printer.constants import RW_TYPES


class Field:
    def __init__(self):
        self.name = ""
        self.msb = 0
        self.lsb = 0
        self.default = 0
        self.access = None
        self.description = ""
        return

    def __str__(self):
        result = "Field: " + str(self.name) + "\n"
        result += "    msb        : " + str(self.msb) + "\n"
        result += "    lsb        : " + str(self.lsb) + "\n"
        result += "    default    : " + str(self.default) + "\n"
        result += "    access     : " + str(self.access) + "\n"
        result += "    description: " \
            + str(self.description)
        return result

    @property
    def size(self):
        result = self.msb - self.lsb + 1
        return result

    @staticmethod
    def from_field_template(field_template):
        field = Field()
        field.name = field_template.name
        field.msb = field_template.msb
        field.lsb = field_template.lsb
        field.default = field_template.default
        field.access = field_template.access
        field.description = field_template.description
        return field
