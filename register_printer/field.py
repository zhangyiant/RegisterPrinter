import re


RW_TYPES = ['RW', 'RO', 'WO', 'RS', 'W1C', "W0C", 'RC', 'WRC', 'WRS', 'WSC', 'WC', '-']

class Field:
    def __init__(self, name, msb, lsb, default, access, description):
        self._name = name
        self._msb = msb
        self._lsb = lsb
        self._default = default
        self._access = access
        self._description = description
        return

    @property
    def name(self):
        return self._name

    @property
    def msb(self):
        return self._msb

    @property
    def lsb(self):
        return self._lsb

    @property
    def default(self):
        return self._default

    @property
    def access(self):
        return self._access

    @property
    def description(self):
        return self._description

    def validate(self):
        msb = self.msb
        lsb = self.lsb
        name = self.name
        access = self.access
        default = self.default
        if lsb > msb:
            raise Exception("lsb %d > msb %d" % (lsb, msb))
        if name == "":
            raise Exception("no Field Name")
        if access not in RW_TYPES:
            raise Exception("Invalid access type.")
        if default >= (1 << (msb-lsb + 1)):
            raise Exception("Default value is out of range.")
        return

    @staticmethod
    def parse_excel_row(row):
        '''
            row is the type in xlrd library.
            It's a sequence of cells.
        '''
        msb = int(row[2].value)
        lsb = int(row[3].value)
        field_name = row[4].value
        access = row[5].value.upper()
        default = row[6].value
        description = "%s" % (row[7].value)
        if re.match(r"0x", str(default)):
            default = int(default, 16)
        else:
            try:
                default = int(default)
            except:
                raise Exception("Invalid default value")
        field = Field(field_name, msb, lsb, default, access, description)
        field.validate()
        return field

    def __str__(self):
        result = "Field " + str(self.name) + "\n"
        result += "    msb      : " + str(self.msb) + "\n"
        result += "    lsb      : " + str(self.lsb) + "\n"
        result += "    default  : " + str(self.default) + "\n"
        result += "    access   : " + str(self.access)
        return result
