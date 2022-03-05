import sys
import logging
import argparse
import traceback
from . import RegisterPrinter


LOGGER = logging.getLogger(__name__)


def get_argument_parser():
    version = RegisterPrinter.get_version()
    parser = argparse.ArgumentParser(
        prog="python -m register_printer",
        )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=version,
        help="Display version"
    )
    input_file_group = parser.add_mutually_exclusive_group()
    input_file_group.add_argument(
        "-f", "--file", dest="config_file",
        help="Configuration input filename.",
        metavar="CONFIG_FILE_NAME")
    input_file_group.add_argument(
        "--input-json",
        dest="input_json",
        help="Input JSON documents.",
        metavar="INPUT_JSON_FILE"
    )
    parser.add_argument(
        "-p", dest="work_path",
        help="Directory path of Excel source files.",
        metavar="EXCEL_FILES_PATH"
    )
    parser.add_argument(
        "-o", "--output-path", dest="output_path",
        default=".",
        help="Output path of generated files. Default \".\"",
        metavar="OUTPUT_PATH"
    )
    parser.add_argument(
        "--print", dest="print",
        action="store_true",
        help="Print parsed document."
    )
    parser.add_argument(
        "--verbose", dest="verbose",
        action="count",
        default=0,
        help="Logging more information."
    )
    parser.add_argument(
        "-d", "--gen-doc", dest="gen_doc",
        action="store_true",
        help="Generate register documents."
    )
    parser.add_argument(
        "-c", "--gen-c-header", dest="gen_c_header",
        action="store_true",
        help="Generate register C header files."
    )
    parser.add_argument(
        "-u", "--gen-uvm", dest="gen_uvm",
        action="store_true",
        help="Generate register UVM models."
    )
    parser.add_argument(
        "-j", "--gen-json", dest="gen_json",
        action="store_true",
        help="Generate JSON documents."
    )
    parser.add_argument(
        "-r", "--gen-rtl", dest="gen_rtl",
        action="store_true",
        help="Generate register RTL module."
    )
    parser.add_argument(
        "-x", "--gen-excel", dest="gen_excel",
        action="store_true",
        help="Generate excel files."
    )
    parser.add_argument(
        "-a", "--gen-all", dest="gen_all",
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
        gen_json=False,
        gen_excel=False):

    if gen_uvm:
        LOGGER.info("Generate UVM models...")
        register_printer.generate_uvm()

    if gen_rtl:
        LOGGER.info("Generating RTL modules...")
        register_printer.generate_rtl()

    if gen_doc:
        LOGGER.info("Generating documentations...")
        register_printer.generate_document()

    if gen_c_header:
        LOGGER.info("Generating C headers...")
        register_printer.generate_c_header()

    if gen_json:
        LOGGER.info("Generating JSON documents...")
        register_printer.generate_json()

    if gen_excel:
        LOGGER.info("Generating Excel files...")
        register_printer.generate_excel()

    return


def main():

    sys.stdout.reconfigure(encoding="utf-8")

    parser = get_argument_parser()

    opts = parser.parse_args()

    if opts.verbose > 0:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(module)s %(levelname)s: %(message)s')
    else:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(module)s %(levelname)s: %(message)s')

    if opts.config_file is None and \
       opts.input_json is None:
        parser.print_usage()
        print(
            "Error: one of CONFIG_FILE_NAME and "
            "INPUT_JSON_FILE must be provided."
        )
        return 1

    if opts.gen_all:
        opts.gen_doc = True
        opts.gen_uvm = True
        opts.gen_rtl = True
        opts.gen_c_header = True

    if opts.config_file is not None:
        if opts.work_path is None:
            parser.print_usage()
            print(
                "error: EXCEL_FILES_PATH must be provied "
                "if CONFIG_FILE_NAME is provided.")
            return 1

    try:
        LOGGER.debug("Initialize RegisterPrinter...")
        register_printer = RegisterPrinter(
            config_file=opts.config_file,
            excel_path=opts.work_path,
            output_path=opts.output_path,
            json_file=opts.input_json
        )

        if opts.print:
            register_printer.display()
            sys.stdout.flush()

        generate(
            register_printer=register_printer,
            gen_uvm=opts.gen_uvm,
            gen_rtl=opts.gen_rtl,
            gen_doc=opts.gen_doc,
            gen_c_header=opts.gen_c_header,
            gen_json=opts.gen_json,
            gen_excel=opts.gen_excel
        )
    except Exception as exc:
        traceback.print_exc()
        print("Error: " + str(exc))
        return 1
    return 0


if __name__ == "__main__":
    EXIT_CODE = main()
    sys.exit(EXIT_CODE)
