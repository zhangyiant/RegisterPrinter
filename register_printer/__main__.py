import logging
import argparse
from . import RegisterPrinter

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(module)s %(message)s')

LOGGER = logging.getLogger(__name__)


def get_argument_parser():
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
        "-o", dest="output_path",
        default=".",
        help="Output path of generated files. Default \".\"",
        metavar="OUTPUT_PATH"
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
        "-j", dest="gen_json",
        action="store_true",
        help="Generate JSON documents."
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
    return parser


def generate(
        register_printer,
        gen_uvm=False,
        gen_rtl=False,
        gen_doc=False,
        gen_c_header=False,
        gen_json=False):

    if gen_uvm:
        LOGGER.debug("Generate UVM models...")
        register_printer.generate_uvm()

    if gen_rtl:
        LOGGER.debug("Generating RTL modules...")
        register_printer.generate_rtl()

    if gen_doc:
        LOGGER.debug("Generating documentations...")
        register_printer.generate_document()

    if gen_c_header:
        LOGGER.debug("Generating C headers...")
        register_printer.generate_c_header()

    if gen_json:
        LOGGER.debug("Genarating JSON documents...")
        register_printer.generate_json()
    return


def main():

    parser = get_argument_parser()

    opts = parser.parse_args()

    if opts.gen_all:
        opts.gen_doc = True
        opts.gen_uvm = True
        opts.gen_rtl = True
        opts.gen_c_header = True

    LOGGER.debug("Initialize RegisterPrinter...")
    register_printer = RegisterPrinter(
        opts.config_file,
        opts.work_path,
        opts.output_path
    )

    register_printer.display()

    generate(
        register_printer=register_printer,
        gen_uvm=opts.gen_uvm,
        gen_rtl=opts.gen_rtl,
        gen_doc=opts.gen_doc,
        gen_c_header=opts.gen_c_header,
        gen_json=opts.gen_json
    )

    return

if __name__ == "__main__":
    main()
