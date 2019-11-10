import sys
from PySide2.QtCore import Slot
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
        return

    @Slot()
    def update_logging(self):
        self.ui.logging_editor.append(" World!")
        return

    @Slot()
    def select_config_file(self):
        filename = QFileDialog.getOpenFileName(
            self,
            "Choose a config file",
            filter="Excel files (*.xlsx)")
        print(filename)
        return

    @Slot()
    def select_excel_path(self):
        path = QFileDialog.getExistingDirectory(
            self,
            "Choose input excel path"
        )
        print(path)
        return

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    return

if __name__ == "__main__":
    main()
