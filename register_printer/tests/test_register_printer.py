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

    def setUp(self):
        self.config_file = os.path.join(
            TestRegisterPrinter.DATASET_PATH,
            "abc.xlsx"
        )
        self.excel_path = os.path.join(
            TestRegisterPrinter.DATASET_PATH,
            "excels"
        )
        return

    def test_uvm_generator(self):
        with TemporaryDirectory() as tmp_dir:
            output_path = tmp_dir
            register_printer = RegisterPrinter(
                config_file=self.config_file,
                excel_path=self.excel_path,
                output_path=output_path
            )
            register_printer.generate_uvm()

            reg_models_file_path = os.path.join(tmp_dir, "regmodels")
            baseline_reg_models_file_path = os.path.join(
                TestRegisterPrinter.DATASET_PATH,
                "output",
                "regmodels"
            )

            compare_files = [
                "top_module_reg_model.sv",
                "top_module_register_defines.svh",
                "type1_reg_model.sv",
                "type2_reg_model.sv"
            ]

            (match_list, mismatch_list, error_list) = filecmp.cmpfiles(
                reg_models_file_path,
                baseline_reg_models_file_path,
                compare_files
            )

            self.assertTrue(
                len(mismatch_list) == 0,
                "UVM generator files mismatched: {}".format(mismatch_list)
            )
            self.assertTrue(
                len(error_list) == 0,
                "UVM generator files errored: {}".format(error_list)
            )

        return

    def test_rtl_generator(self):
        with TemporaryDirectory() as tmp_dir:
            output_path = tmp_dir
            register_printer = RegisterPrinter(
                config_file=self.config_file,
                excel_path=self.excel_path,
                output_path=output_path
            )
            register_printer.generate_rtl()

            reg_rtl_file_path = os.path.join(tmp_dir, "regrtls")
            baseline_reg_rtl_file_path = os.path.join(
                TestRegisterPrinter.DATASET_PATH,
                "output",
                "regrtls"
            )

            compare_files = [
                "Type1_reg.sv",
                "Type2_reg.sv"
            ]

            (match_list, mismatch_list, error_list) = filecmp.cmpfiles(
                reg_rtl_file_path,
                baseline_reg_rtl_file_path,
                compare_files
            )

            self.assertTrue(
                len(mismatch_list) == 0,
                "RTL generator files mismatched: {}".format(mismatch_list)
            )
            self.assertTrue(
                len(error_list) == 0,
                "RTL generator files errored: {}".format(error_list)
            )

        return

    def test_c_generator(self):
        with TemporaryDirectory() as tmp_dir:
            output_path = tmp_dir
            register_printer = RegisterPrinter(
                config_file=self.config_file,
                excel_path=self.excel_path,
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

    def test_doc_generator(self):
        with TemporaryDirectory() as tmp_dir:
            output_path = tmp_dir
            register_printer = RegisterPrinter(
                config_file=self.config_file,
                excel_path=self.excel_path,
                output_path=output_path
            )
            register_printer.generate_document()

            doc_file_path = tmp_dir

            doc_filename = os.path.join(
                doc_file_path,
                "top_module_registers.docx"
            )
            self.assertTrue(
                os.path.exists(doc_filename),
                "Docx file is not generated."
            )

            # Currently, it's not easy to compare the docx contents,
            # because there are generated datetime in the content of docx.
            # So here, we only make sure the file is generated.

        return
