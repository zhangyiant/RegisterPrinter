import logging
import argparse
from . import RegisterPrinter

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(module)s %(message)s')

LOGGER = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        prog="python -m register_printer",
        )
    parser.add_argument(
        "-f", dest="config_file",
        required=True,
        help="Configuration input filename.",
        metavar="CONFIG_FILE_NAME")
    parser.add_argument(
        "-p", dest="work_path",
        required=True,
        help="Directory path of Excel source files.",
        metavar="EXCEL_FILES_PATH"
    )
    parser.add_argument(
        "-d", dest="gen_doc",
        action="store_true",
        help="Generate register documents."
    )
    parser.add_argument(
        "-c", dest="gen_c_header",
        action="store_true",
        help="Generate register C header files."
    )
    parser.add_argument(
        "-u", dest="gen_uvm",
        action="store_true",
        help="Generate register UVM models."
    )
    parser.add_argument(
        "-r", dest="gen_rtl",
        action="store_true",
        help="Generate register RTL module."
    )
    parser.add_argument(
        "-a", dest="gen_all",
        action="store_true",
        help="Generate all files, same as -d -c -u -r"
    )

    opts = parser.parse_args()

    if opts.gen_all:
        opts.gen_doc = True
        opts.gen_uvm = True
        opts.gen_rtl = True
        opts.gen_c_header = True

    LOGGER.debug("Initialize RegisterPrinter...")
    register_printer = RegisterPrinter(
        opts.config_file,
        opts.work_path
    )

    register_printer.display()

    if opts.gen_uvm:
        LOGGER.debug("Generate UVM models...")
        register_printer.generate_uvm()

    if opts.gen_rtl:
        LOGGER.debug("Generating RTL modules...")
        register_printer.generate_rtl()

    if opts.gen_doc:
        LOGGER.debug("Generating documentations...")
        register_printer.generate_document()

    if opts.gen_c_header:
        LOGGER.debug("Generating C headers...")
        register_printer.generate_c_header()

    return

if __name__ == "__main__":
    main()
