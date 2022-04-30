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

    # parse msb field
    msb = parse_msb(row[context.column].value, context)

    # parse lsb field
    context.column = register_table_column_mapping["lsb"]
    lsb = parse_lsb(row[context.column].value, context)
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
        msg = "Invalid access type: {}, valid access types are {}.".format(
            access,
            RW_TYPES
        )
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


def parse_lsb(value, context):
    try:
        lsb = int(value)
    except Exception as exc:
        msg = "Parse 'lsb' error: {}.".format(exc)
        raise ExcelParseException(msg, context)
    return lsb


def parse_msb(value, context):
    try:
        msb = int(value)
    except Exception as exc:
        msg = "Parse 'msb' error: {}.".format(exc)
        raise ExcelParseException(msg, context)
    return msb
