import re
import textwrap
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

    # all fields msb/lsb are in ascending order
    def add_field(self, new_field):
        fields = []
        inserted = False
        for field in self.fields:
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

    @staticmethod
    def validate_register_row_empty_field(row):
        '''
            row can be obtained by xlrd sheet.row() method.
            It's a sequence of cell objects.
        '''
        field_map = [
            (2, "msb"),
            (3, "lsb"),
            (4, "field"),
            (5, "access"),
            (6, "default")
        ]
        for (col, field_name) in field_map:
            if row[col].value != "":
                raise Exception("%s must be emtpy." % field_name)
        return


    @staticmethod
    def parse_register_row(row):
        '''
            row: xlrd row object. You can obtain it by sheet.row()
                 a sequence of cells.
        '''

        Register.validate_register_row_empty_field(row)

        offset = int(row[0].value, 16)
        name = row[1].value
        description = "%s" % (row[7].value)
        register = Register(name, offset, description)

        return register

    @staticmethod
    def is_register_row(row):
        '''
            row: xlrd row object.
        '''
        if re.match(r'0x', str(row[0].value)):
            return True
        return False

    def __str__(self):
        result = "Register " + str(self.name) + "\n"
        result += "    offset: " + str(self.offset) + "\n"
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
