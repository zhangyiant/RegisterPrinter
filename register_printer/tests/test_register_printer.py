import os.path
from tempfile import TemporaryDirectory
import filecmp
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
            baseline_reg_headers_file_path = os.path.join(
                TestRegisterPrinter.DATASET_PATH,
                "output",
                "regheaders"
            )

            # Compare top module header file
            top_module_filename = os.path.join(
                reg_headers_file_path, "regs_top_module.h")
            self.assertTrue(
                os.path.exists(top_module_filename),
                "Top module header file is not generated."
            )
            baseline_top_module_filename = os.path.join(
                baseline_reg_headers_file_path,
                "regs_top_module.h"
            )
            self.assertTrue(
                filecmp.cmp(
                    top_module_filename,
                    baseline_top_module_filename
                ),
                "Top module header file content is not correct."
            )

            # Compare block header files
            type1_header_filename = os.path.join(
                reg_headers_file_path,
                "regs_type1.h"
            )
            baseline_type1_header_filename = os.path.join(
                baseline_reg_headers_file_path,
                "regs_type1.h"
            )
            self.assertTrue(
                os.path.exists(type1_header_filename),
                "Type1 header file is not generated."
            )
            self.assertTrue(
                filecmp.cmp(
                    type1_header_filename,
                    baseline_type1_header_filename
                ),
                "Type1 file content is not correct."
            )
            type2_header_filename = os.path.join(
                reg_headers_file_path,
                "regs_type2.h"
            )
            baseline_type2_header_filename = os.path.join(
                baseline_reg_headers_file_path,
                "regs_type2.h"
            )
            self.assertTrue(
                os.path.exists(type2_header_filename),
                "Type2 header file is not generated."
            )
            self.assertTrue(
                filecmp.cmp(
                    type2_header_filename,
                    baseline_type2_header_filename
                ),
                "Type2 file content is not correct."
            )

            # compare test.c file
            test_c_filename = os.path.join(
                reg_headers_file_path,
                "test.c"
            )
            baseline_test_c_filename = os.path.join(
                baseline_reg_headers_file_path,
                "test.c"
            )
            self.assertTrue(
                os.path.exists(test_c_filename),
                "test.c is not generated."
            )
            self.assertTrue(
                filecmp.cmp(
                    test_c_filename,
                    baseline_test_c_filename
                ),
                "Test.c file content is not correct."
            )
        return
