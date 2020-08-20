import re
import logging


LOGGER = logging.getLogger(__name__)


def parse_field_row(row):
    """
        row is the type in xlrd library.
        It's a sequence of cells.
    """
    msb = int(row[2].value)
    lsb = int(row[3].value)
    field_name = row[4].value
    access = row[5].value.upper()
    default = row[6].value
    description = "%s" % row[7].value
    if re.match(r"0x", str(default)):
        default = int(default, 16)
    else:
        try:
            default = int(default)
        except:
            raise Exception("Invalid default value")
    field_dict = {
        "name": field_name,
        "msb": msb,
        "lsb": lsb,
        "defaultValue": default,
        "access": access,
        "description": description
    }
    return field_dict
