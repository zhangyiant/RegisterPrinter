import re
import textwrap
from .field_template import FieldTemplate

class RegisterTemplate:
    def __init__(self, name, offset, description):
        self._name = name
        self._offset = offset
        self._description = description
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
        return self._description

    # all fields msb/lsb are in ascending order
    def add_field(self, new_field):
        fields = []
        inserted = False
        for field in self.fields:
            if inserted:
                fields.append(field)
                continue
            overlapped = False
            if new_field.lsb > field.lsb:
                if new_field.lsb > field.msb:
                    fields.append(field)
                else:
                    overlapped = True
            elif new_field.lsb == field.lsb:
                overlapped = True
            else:
                # new_field.lsb < field.lsb
                if new_field.msb < field.msb:
                    fields.append(new_field)
                    fields.append(field)
                    inserted = True
                else:
                    overlapped = True

            if overlapped:
                error_msg = "Fields overlap: \n{0}\n{1}".format(
                    field, new_field)
                raise Exception(error_msg)
        if not inserted:
            fields.append(new_field)
        self.fields = fields
        return

    def calculate_register_default(self):
        value = 0
        for field in self.fields:
            pos = field.lsb
            val = field.default
            value = value | (val << pos)
        return value

    def __str__(self):
        result = "Register " + str(self.name) + "\n"
        result += "    offset: " + str(self.offset) + "\n"
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

    @staticmethod
    def from_dict(register_dict):
        name = register_dict["name"]
        offset = register_dict["offset"]
        description = register_dict["description"]
        register = RegisterTemplate(
            name=name,
            offset=offset,
            description=description)
        fields_dict = register_dict["fields"]
        for field_dict in fields_dict:
            field = FieldTemplate.from_dict(
                field_dict)
            register.fields.append(
                field)
        return register
