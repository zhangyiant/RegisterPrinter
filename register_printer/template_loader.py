import logging
import sys
import pkgutil
from jinja2 import Environment, PackageLoader, Template


LOGGER = logging.getLogger(__name__)


def _get_template_pyinstaller(name):
    template_bin = pkgutil.get_data("register_printer", "templates/" + name)
    template_str = template_bin.decode('UTF-8')
    template = Template(
        template_str,
        trim_blocks=True,
        lstrip_blocks=True
    )
    return template


def _get_template_pkg_loader(name):
    env = Environment(
        loader=PackageLoader("register_printer", "templates"),
        trim_blocks=True,
        lstrip_blocks=True
    )
    template = env.get_template(name)
    return template


def get_template(name):
    if hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
        return _get_template_pyinstaller(name)
    else:
        return _get_template_pyinstaller(name)

