class ExcelParseContext:
    def __init__(self, filename=None, sheet_name=None, row=None, column=None):
        self.filename = filename
        self.sheet_name = sheet_name
        self.row = row
        self.column = column
        return
