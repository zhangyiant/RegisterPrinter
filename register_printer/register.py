from .field import *

class Register:
    def __init__(self, name, offset, description):
        self._name = name
        self._offset = offset
        self._desciption = description
        self.fields = []
        return

    @property
    def name(self):
        return self._name

    @property
    def offset(self):
        return self._offset

    @property
    def description(self):
        return self._desciption

    def add_field(self, field):
        self.fields.append(field)
        return

    def calculate_register_default(self):
        value = 0
        for field in self.fields:
            pos = field.lsb
            val = field.default
            value = value | (val << pos)
        return value

    def __str__(self):
        result = "---------------------------------\n"
        result += "Register " + str(self.name) + "\n"
        result += "    offset: " + str(self.offset) + "\n"
        result += "    fields:\n"
        for field in self.fields:
            result += "          " + str(field) + "\n"
        result += "---------------------------------"
        return result
