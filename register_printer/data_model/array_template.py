class ArrayTemplate:
    def __init__(self, name, length, offset, start_address, end_address, description):
        self._name = name
        self._length = length
        self._offset = offset
        self._start_address = start_address
        self._end_address = end_address
        self._description = description
        return

    @property
    def name(self):
        return self._name

    @property
    def length(self):
        return self._length

    @property
    def offset(self):
        return self._offset

    @property
    def start_address(self):
        return self._start_address

    @property
    def end_address(self):
        return self._end_address

    @property
    def array_start_address(self):
        return self.start_address

    @property
    def array_stop_address(self):
        return self.start_address + self.offset * self.length

    @property
    def size(self):
        return self.array_stop_address - self.array_start_address

    @property
    def description(self):
        return self._description

    def __str__(self):
        result = "Array Template: " + str(self.name) + "\n"
        result += "    length        : " + str(self.length) + "\n"
        result += "    offset        : 0x%x\n" % self.offset
        result += "    start address : 0x%x\n" % self.start_address
        result += "    end address   : 0x%x\n" % self.end_address
        result += "    description: " \
            + str(self.description)
        return result

    def to_dict(self):
        result = {}
        result["name"] = self.name
        result["length"] = self.length
        result["offset"] = self.offset
        result["startAddress"] = self.start_address
        result["endAddress"] = self.end_address
        result["description"] = self.description
        return result

    @staticmethod
    def from_dict(array_dict):
        name = array_dict["name"]
        length = array_dict["length"]
        offset = array_dict["offset"]
        start_address = array_dict["startAddress"]
        end_address = array_dict["endAddress"]
        description = array_dict["description"]
        array = ArrayTemplate(
            name=name,
            length=length,
            offset=offset,
            start_address=start_address,
            end_address=end_address,
            description=description
        )
        return array
