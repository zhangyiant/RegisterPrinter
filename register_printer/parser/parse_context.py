class ExcelParseContext:
    def __init__(self, filename=None, sheet_name=None, row=None, column=None):
        self.filename = filename
        self.sheet_name = sheet_name
        self.row = row
        self.column = column
        return

    def copy(self):
        new_instance = ExcelParseContext()
        new_instance.filename = self.filename
        new_instance.sheet_name = self.sheet_name
        new_instance.row = self.row
        new_instance.column = self.column
        return new_instance
