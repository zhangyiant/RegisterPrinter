import textwrap

class DefaultOverwriteEntry:
    def __init__(self):
        self.index = None
        self.register_name = None
        self.field_name = None
        self.default = None
        return

    def __str__(self):
        result = "Overwrite: "
        result += "\n    index: " + str(self.index)
        result += "\n    register name: " + str(self.register_name)
        result += "\n    field name: " + str(self.field_name)
        result += "\n    default: " + hex(self.default)
        return result

class Array:
    def __init__(self, content_type, length, start_address):
        self.content_type = content_type
        self.length = length
        self.default_overwrite_entries = []
        self.start_address = start_address
        return

    @property
    def offset(self):
        return self.content_type.size()

    def __str__(self):
        result = "Array of " + self.content_type.name
        result += "\n    length: " + str(self.length)
        result += "\n    start address: " + str(self.start_address)
        result += "\n    content type:"
        content_type_string = str(self.content_type)
        content_type_string = textwrap.indent(content_type_string, " " * 4)
        result += "\n" + content_type_string
        result += "\n    default overwrite entries: "
        overwrite_strings = []
        for default_overwrite_entry in self.default_overwrite_entries:
            overwrite_string = str(default_overwrite_entry)
            overwrite_string = textwrap.indent(overwrite_string, " " * 8)
            overwrite_strings.append(overwrite_string)
        result += "\n" + "\n".join(overwrite_strings)
        return result