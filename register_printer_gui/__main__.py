import sys
import traceback
from PySide2.QtCore import (
    Signal,
    Slot,
    QDir,
    Qt
)
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog
)
from .ui_mainwindow import Ui_MainWindow
from register_printer import RegisterPrinter

class MainWindow(QMainWindow):

    log = Signal(str)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.generate)
        self.ui.config_file_button.clicked.connect(self.select_config_file)
        self.ui.excel_path_button.clicked.connect(self.select_excel_path)
        self.ui.output_path_button.clicked.connect(self.select_output_path)
        self.log.connect(self.log_message)
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

        self.log.emit("Done")
        return

    @Slot(str)
    def log_message(self, message):
        self.ui.logging_editor.append(message)
        return

    @Slot()
    def generate(self):

        self.ui.logging_editor.clear()

        config_file = self.ui.config_file_editor.text()
        excel_path = self.ui.excel_path_editor.text()
        output_path = self.ui.output_path_editor.text()
        self.log.emit(
            "Config file: {0}".format(config_file))
        self.log.emit(
            "Excel files path: {0}".format(excel_path))
        self.log.emit(
            "Output path: {0}".format(output_path))

        gen_doc_check_state = self.ui.gen_doc_checkbox.checkState()
        gen_doc_flag = None
        if gen_doc_check_state == Qt.Checked:
            gen_doc_flag = True
        else:
            gen_doc_flag = False

        gen_c_header_check_state = self.ui.gen_c_header_checkbox.checkState()
        gen_c_header_flag = None
        if gen_c_header_check_state == Qt.Checked:
            gen_c_header_flag = True
        else:
            gen_c_header_flag = False

        gen_uvm_check_state = self.ui.gen_uvm_checkbox.checkState()
        gen_uvm_flag = None
        if gen_uvm_check_state == Qt.Checked:
            gen_uvm_flag = True
        else:
            gen_uvm_flag = False

        gen_rtl_check_state = self.ui.gen_rtl_checkbox.checkState()
        gen_rtl_flag = None
        if gen_rtl_check_state == Qt.Checked:
            gen_rtl_flag = True
        else:
            gen_rtl_flag = False

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

            self.ui.logging_editor.append(display_info)

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

        return

    @Slot()
    def select_config_file(self):
        result = QFileDialog.getOpenFileName(
            self,
            "Choose a config file",
            filter="Excel files (*.xlsx)")
        filename = result[0]
        if filename:
            native_config_file = QDir.toNativeSeparators(filename)
            self.ui.config_file_editor.setText(native_config_file)
        return

    @Slot()
    def select_excel_path(self):
        excel_path = QFileDialog.getExistingDirectory(
            self,
            "Choose input excel path"
        )
        if excel_path:
            native_excel_path = QDir.toNativeSeparators(
                excel_path
            )
        self.ui.excel_path_editor.setText(native_excel_path)
        return

    @Slot()
    def select_output_path(self):
        output_path = QFileDialog.getExistingDirectory(
            self,
            "Choose output path"
        )
        if output_path:
            native_output_path = QDir.toNativeSeparators(
                output_path
            )
        self.ui.output_path_editor.setText(native_output_path)
        return

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    return

if __name__ == "__main__":
    main()
