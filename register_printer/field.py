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

    def __str__(self):
        result = "Field " + str(self.name) + "\n"
        result += "    msb      : " + str(self.msb) + "\n"
        result += "    lsb      : " + str(self.lsb) + "\n"
        result += "    default  : " + str(self.default) + "\n"
        result += "    access   : " + str(self.access)
        return result
