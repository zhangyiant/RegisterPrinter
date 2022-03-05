import textwrap

class Struct:
    def __init__(self, name):
        self.name = name
        self.registers = []
        return

    def size(self):
        result = 0
        for register in self.registers:
            result += register.size()
        return result

    def __str__(self):
        result = "Struct: " + self.name + "\n"
        register_strings = []
        for register in self.registers:
            register_string = str(register)
            register_string = textwrap.indent(register_string, " " * 4)
            register_strings.append(register_string)
        result += "\n".join(register_strings)
        return result
