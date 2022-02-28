import textwrap

class Array:
    def __init__(self, content_type, length):
        self.content_type = content_type
        self.length = length
        return

    def __str__(self):
        result = "Array of " + self.content_type.name
        result += "\n    length: " + str(self.length)
        result += "\n    content type:"
        content_type_string = str(self.content_type)
        content_type_string = textwrap.indent(content_type_string, " " * 4)
        result += "\n" + content_type_string
        return result