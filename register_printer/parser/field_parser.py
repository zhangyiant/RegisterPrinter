from atexit import register
import re
import logging
from .parse_exception import ExcelParseException
from register_printer.constants import RW_TYPES


LOGGER = logging.getLogger(__name__)


def parse_field_row(row, register_table_column_mapping, previous_context):
    """
        row is the type in xlrd library.
        It's a sequence of cells.
    """
    context = previous_context.copy()

    context.column = register_table_column_mapping["msb"]
    try:
        msb = int(row[context.column].value)
    except Exception as exc:
        msg = "Parse 'msb' error: {}.".format(exc)
        raise ExcelParseException(msg, context)

    context.column = register_table_column_mapping["lsb"]
    try:
        lsb = int(row[context.column].value)
    except Exception as exc:
        msg = "Parse 'lsb' error: {}.".format(exc)
        raise ExcelParseException(msg, context)
    if lsb > msb:
        msg = "Error: lsb %d > msb %d." % (lsb, msb)
        raise ExcelParseException(msg, context)

    context.column = register_table_column_mapping["field name"]
    field_name = row[context.column].value
    if field_name == "":
        msg = "No Field Name."
        raise ExcelParseException(msg, context)

    context.column = register_table_column_mapping["access"]
    access = row[context.column].value.upper()
    if access not in RW_TYPES:
        msg = "Invalid access type: {}.".format(access)
        raise ExcelParseException(msg, context)

    context.column = register_table_column_mapping["default"]
    default = row[context.column].value
    try:
        if re.match(r"0x", str(default)):
            default = int(default, 16)
        else:
            default = int(default)
    except Exception as exc:
        msg = "Parse 'default' error: {}.".format(exc)
        raise ExcelParseException(msg, context)
    if default >= (1 << (msb - lsb + 1)):
        msg = "Default value is out of range."
        raise ExcelParseException(msg, context)

    context.column = register_table_column_mapping["description"]
    description = "%s" % row[context.column].value

    field_dict = {
        "name": field_name,
        "msb": msb,
        "lsb": lsb,
        "defaultValue": default,
        "access": access,
        "description": description
    }
    return field_dict
