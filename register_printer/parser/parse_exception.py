class ParseException(Exception):
    def __init__(self, msg):
        self.msg = msg
        return


class ExcelParseException(ParseException):
    def __init__(self, msg, filename=None, sheet_name=None, row=None, column=None):
        ParseException.__init__(self, msg)
        self.filename = filename
        self.sheet_name = sheet_name
        self.row = row
        self.column = column
        return

    def __str__(self):
        msg = self.msg
        info = []
        if self.filename is not None:
            info.append("Filename: {}".format(self.filename))
        if self.sheet_name is not None:
            info.append("Sheet name: {}".format(self.sheet_name))
        if self.row is not None:
            info.append("Row: {}".format(self.row))
        if self.column is not None:
            info.append("Column: {}".format(self.column))
        msg += " " + ", ".join(info)
        return msg
