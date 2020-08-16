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

    def __str__(self):
        result = "Field " + str(self.name) + "\n"
        result += "    msb        : " + str(self.msb) + "\n"
        result += "    lsb        : " + str(self.lsb) + "\n"
        result += "    default    : " + str(self.default) + "\n"
        result += "    access     : " + str(self.access) + "\n"
        result += "    description: " \
            + str(self.description)
        return result

    def to_dict(self):
        result = {}
        result["name"] = self.name
        result["msb"] = self.msb
        result["lsb"] = self.lsb
        result["defaultValue"] = self.default
        result["access"] = self.access
        result["description"] = self.description
        return result

    @staticmethod
    def from_dict(field_dict):
        name = field_dict["name"]
        msb = field_dict["msb"]
        lsb = field_dict["lsb"]
        default_value = field_dict["defaultValue"]
        access = field_dict["access"]
        description = field_dict["description"]
        field = Field(
            name=name,
            msb=msb,
            lsb=lsb,
            default=default_value,
            access=access,
            description=description)
        return field
