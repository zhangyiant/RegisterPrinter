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

            compare_files = [
                "regs_top_module.h",
                "regs_type1.h",
                "regs_type2.h",
                "test.c"
            ]

            (match_list, mismatch_list, error_list) = filecmp.cmpfiles(
                reg_headers_file_path,
                baseline_reg_headers_file_path,
                compare_files
            )

            self.assertTrue(
                len(mismatch_list) == 0,
                "C generator files mismatched: {}".format(mismatch_list)
            )
            self.assertTrue(
                len(error_list) == 0,
                "C generator files errored: {}".format(error_list)
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
