import os
import os.path
import logging
from register_printer.template_loader import get_template


LOGGER = logging.getLogger(__name__)


def print_sv_defines(top_sys, out_path):

    sv_def_name = top_sys.name.lower() + "_register_defines"
    file_name = os.path.join(
        out_path,
        sv_def_name + ".svh")

    if os.path.exists(file_name):
        os.remove(file_name)

    template = get_template("register_defines.svh")

    content = template.render(
        {
            "top_sys": top_sys
        }
    )

    with open(file_name, "w") as bfh:
        bfh.write(content)

    return