import sys
from PySide2.QtCore import (
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
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.logging_editor.append("Hello")
        self.ui.pushButton.clicked.connect(self.generate)
        self.ui.config_file_button.clicked.connect(self.select_config_file)
        self.ui.excel_path_button.clicked.connect(self.select_excel_path)
        self.ui.output_path_button.clicked.connect(self.select_output_path)
        return

    @Slot()
    def generate(self):
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

        self.ui.logging_editor.clear()
        self.ui.logging_editor.append(str(gen_doc_flag))
        self.ui.logging_editor.append(str(gen_c_header_flag))
        self.ui.logging_editor.append(str(gen_uvm_flag))
        self.ui.logging_editor.append(str(gen_rtl_flag))

        config_file = self.ui.config_file_editor.text()
        excel_path = self.ui.excel_path_editor.text()
        output_path = self.ui.output_path_editor.text()
        self.ui.logging_editor.append(config_file)
        self.ui.logging_editor.append(excel_path)
        self.ui.logging_editor.append(output_path)

        register_printer = RegisterPrinter(
            config_file,
            excel_path
        )

        display_info = register_printer.display_string()

        self.ui.logging_editor.append(display_info)

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
