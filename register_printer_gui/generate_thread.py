import traceback
from PySide2.QtCore import (
    Signal,
    QThread
)

from register_printer import RegisterPrinter

class GenerateThread(QThread):

    log = Signal(str)
    done = Signal()

    def __init__(self, config_file, excel_path, output_path,
            gen_doc_flag, gen_c_header_flag, gen_uvm_flag, gen_rtl_flag):
        super().__init__()
        self.config_file = config_file
        self.excel_path = excel_path
        self.output_path = output_path
        self.gen_doc_flag = gen_doc_flag
        self.gen_c_header_flag = gen_c_header_flag
        self.gen_uvm_flag = gen_uvm_flag
        self.gen_rtl_flag = gen_rtl_flag
        return

    def _generate(
        self,
        register_printer,
        gen_uvm=False,
        gen_rtl=False,
        gen_doc=False,
        gen_c_header=False):

        if gen_uvm:
            self.log.emit("Generate UVM models...")
            register_printer.generate_uvm()

        if gen_rtl:
            self.log.emit("Generating RTL modules...")
            register_printer.generate_rtl()

        if gen_doc:
            self.log.emit("Generating documentations...")
            register_printer.generate_document()

        if gen_c_header:
            self.log.emit("Generating C headers...")
            register_printer.generate_c_header()

        return

    def run(self):
        config_file = self.config_file
        excel_path = self.excel_path
        output_path = self.output_path
        self.log.emit(
            "Config file: {0}".format(config_file))
        self.log.emit(
            "Excel files path: {0}".format(excel_path))
        self.log.emit(
            "Output path: {0}".format(output_path))

        gen_doc_flag = self.gen_doc_flag
        gen_c_header_flag = self.gen_c_header_flag
        gen_uvm_flag = self.gen_uvm_flag
        gen_rtl_flag = self.gen_rtl_flag
        self.log.emit(
            "Generate documents: {0}".format(gen_doc_flag))
        self.log.emit(
            "Generate C header files: {0}".format(gen_c_header_flag))
        self.log.emit(
            "Generate UVM models: {0}".format(gen_uvm_flag))
        self.log.emit(
            "Generate RTL modules: {0}".format(gen_rtl_flag))

        try:
            if not output_path:
                output_path = "."
            register_printer = RegisterPrinter(
                config_file,
                excel_path,
                output_path
            )

            display_info = register_printer.display_string()

            self.log.emit(display_info)

            self._generate(
                register_printer,
                gen_uvm=gen_uvm_flag,
                gen_rtl=gen_rtl_flag,
                gen_doc=gen_doc_flag,
                gen_c_header=gen_c_header_flag
            )
        except Exception as e:
            error_info = traceback.format_exc()
            self.log.emit(error_info)
        self.done.emit()
        return
