import os
import logging

from register_printer.template_loader import get_template


LOGGER = logging.getLogger(__name__)


def print_c_test(top_sys, out_path):
    LOGGER.debug("Print top sys C test...")

    file_name = os.path.join(
        out_path,
        "test.c")

    if os.path.exists(file_name):
        os.remove(file_name)

    template = get_template("c_test.c")

    content = template.render(
        {
            "top_sys": top_sys
        }
    )

    with open(file_name, "w") as sfh:
        sfh.write(content)

    return