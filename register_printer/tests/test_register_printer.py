import os.path
from tempfile import TemporaryDirectory
from ..register_printer import RegisterPrinter
from unittest import TestCase

DATASET_ROOT_PATH = os.path.join(
    os.path.dirname(__file__),
    "dataset"
)


class TestRegisterPrinter(TestCase):

    DATASET_PATH = os.path.join(DATASET_ROOT_PATH, "dataset1")

    def test_c_generator(self):
        config_file = os.path.join(
            TestRegisterPrinter.DATASET_PATH,
            "abc.xlsx"
        )
        excel_path = os.path.join(
            TestRegisterPrinter.DATASET_PATH,
            "excels"
        )
        with TemporaryDirectory() as tmp_dir:
            output_path = tmp_dir
            register_printer = RegisterPrinter(
                config_file=config_file,
                excel_path=excel_path,
                output_path=output_path
            )
            register_printer.generate_c_header()

            reg_headers_file_path = os.path.join(tmp_dir, "regheaders")
            top_module_filename = os.path.join(reg_headers_file_path, "regs_top_module.h")
            self.assertTrue(
                os.path.exists(top_module_filename),
                "Top module header file is not generated."
            )
            type1_header_filename = os.path.join(
                reg_headers_file_path,
                "regs_type1.h"
            )
            self.assertTrue(
                os.path.exists(type1_header_filename),
                "Type1 header file is not generated."
            )
            type2_header_filename = os.path.join(
                reg_headers_file_path,
                "regs_type2.h"
            )
            self.assertTrue(
                os.path.exists(type2_header_filename),
                "Type2 header file is not generated."
            )
            test_c_filename = os.path.join(
                reg_headers_file_path,
                "test.c"
            )
            self.assertTrue(
                os.path.exists(test_c_filename),
                "test.c is not generated."
            )
        return
