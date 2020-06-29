from register_printer.data_model import Register


def is_field_row(row):
    '''
        row: xlrd row object.
    '''
    if row[2].value != "":
        return True
    return False


def validate_register_row_empty_field(row):
    """
        row can be obtained by xlrd sheet.row() method.
        It's a sequence of cell objects.
    """
    field_map = [
        (2, "msb"),
        (3, "lsb"),
        (4, "field"),
        (5, "access"),
        (6, "default")
    ]
    for (col, field_name) in field_map:
        if row[col].value != "":
            raise Exception("%s must be emtpy." % field_name)
    return


def parse_register_row(row):
    """
        row: xlrd row object. You can obtain it by sheet.row()
                 a sequence of cells.
    """

    validate_register_row_empty_field(row)

    offset = int(row[0].value, 16)
    name = row[1].value
    description = "%s" % (row[7].value)

    result = {
        "offset": offset,
        "name": name,
        "description": description
    }

    return result
