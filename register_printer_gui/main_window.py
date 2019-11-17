from PySide2.QtCore import (
    Slot,
    QDir,
    Qt,
    QThread
)
from PySide2.QtWidgets import (
    QMainWindow,
    QFileDialog
)

from .ui_mainwindow import Ui_MainWindow
from .generate_thread import GenerateThread

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.generate)
        self.ui.config_file_button.clicked.connect(self.select_config_file)
        self.ui.excel_path_button.clicked.connect(self.select_excel_path)
        self.ui.output_path_button.clicked.connect(self.select_output_path)
        return

    @Slot()
    def generated(self):
        self.ui.logging_editor.append("Done")
        self.ui.pushButton.setEnabled(True)
        return

    @Slot(str)
    def log_message(self, message):
        self.ui.logging_editor.append(message)
        return

    @Slot()
    def generate(self):

        self.ui.logging_editor.clear()
        self.ui.pushButton.setDisabled(True)

        config_file = self.ui.config_file_editor.text()
        excel_path = self.ui.excel_path_editor.text()
        output_path = self.ui.output_path_editor.text()

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

        self.generateThread = GenerateThread(
            config_file,
            excel_path,
            output_path,
            gen_doc_flag,
            gen_c_header_flag,
            gen_uvm_flag,
            gen_rtl_flag)

        self.generateThread.log.connect(self.log_message)
        self.generateThread.done.connect(self.generated)

        self.generateThread.start()

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
