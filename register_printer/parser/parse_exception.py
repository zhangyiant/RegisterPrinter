class ParseException(Exception):
    def __init__(self, msg):
        self.msg = msg
        return


class ExcelParseException(ParseException):
    def __init__(self, msg, context):
        ParseException.__init__(self, msg)
        self.context = context
        return

    @property
    def filename(self):
        return self.context.filename

    @property
    def sheet_name(self):
        return self.context.sheet_name

    @property
    def row(self):
        return self.context.row

    @property
    def column(self):
        return self.context.column

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
