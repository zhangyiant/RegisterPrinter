from register_printer.constants import RW_TYPES


class FieldTemplate:
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
        field = FieldTemplate(
            name=name,
            msb=msb,
            lsb=lsb,
            default=default_value,
            access=access,
            description=description)
        return field
