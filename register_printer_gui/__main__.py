import sys
from PySide2.QtCore import (
    Slot,
    QDir
)
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog
)
from .ui_mainwindow import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.logging_editor.append("Hello")
        self.ui.pushButton.clicked.connect(self.update_logging)
        self.ui.config_file_button.clicked.connect(self.select_config_file)
        self.ui.excel_path_button.clicked.connect(self.select_excel_path)
        self.ui.output_path_button.clicked.connect(self.select_output_path)
        return

    @Slot()
    def update_logging(self):
        self.ui.logging_editor.append(" World!")
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
