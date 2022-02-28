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
