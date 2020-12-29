import re
import logging
from .parse_exception import ExcelParseException


LOGGER = logging.getLogger(__name__)


def parse_field_row(row, previous_context):
    """
        row is the type in xlrd library.
        It's a sequence of cells.
    """
    context = previous_context.copy()

    context.column = 2
    try:
        msb = int(row[2].value)
    except Exception as exc:
        msg = "Parse 'msb' error: {}.".format(exc)
        raise ExcelParseException(msg, context)

    context.column = 3
    try:
        lsb = int(row[3].value)
    except Exception as exc:
        msg = "Parse 'lsb' error: {}.".format(exc)
        raise ExcelParseException(msg, context)

    field_name = row[4].value
    access = row[5].value.upper()

    context.column = 6
    default = row[6].value
    try:
        if re.match(r"0x", str(default)):
            default = int(default, 16)
        else:
            default = int(default)
    except Exception as exc:
        msg = "Parse 'default' error: {}.".format(exc)
        raise ExcelParseException(msg, context)

    description = "%s" % row[7].value

    field_dict = {
        "name": field_name,
        "msb": msb,
        "lsb": lsb,
        "defaultValue": default,
        "access": access,
        "description": description
    }
    return field_dict
