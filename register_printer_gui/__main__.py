import sys
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow
)
from .ui_mainwindow import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.logging_editor.append("Hello")
        return

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    return

if __name__ == "__main__":
    main()
