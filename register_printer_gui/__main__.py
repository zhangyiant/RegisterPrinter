import sys

from PySide2.QtWidgets import (
    QApplication
)

from .main_window import MainWindow


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    return

if __name__ == "__main__":
    main()
