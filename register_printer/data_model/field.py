from register_printer.constants import RW_TYPES


class Field:
    def __init__(self, field_template):
        self._field_template = field_template
        return

    @property
    def name(self):
        return self._field_template.name

    @property
    def msb(self):
        return self._field_template.msb

    @property
    def lsb(self):
        return self._field_template.lsb

    @property
    def default(self):
        return self._field_template.default

    @property
    def access(self):
        return self._field_template.access

    @property
    def description(self):
        return self._field_template.description

    def __str__(self):
        result = "Field: " + str(self.name) + "\n"
        result += "    msb        : " + str(self.msb) + "\n"
        result += "    lsb        : " + str(self.lsb) + "\n"
        result += "    default    : " + str(self.default) + "\n"
        result += "    access     : " + str(self.access) + "\n"
        result += "    description: " \
            + str(self.description)
        return result
