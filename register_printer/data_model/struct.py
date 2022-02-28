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
        result = "Struct: " + self.name
        for register in self.registers:
            result += "\n" + str(register)
        return result