from gui.main_window import MainWindow
from PySide6.QtWidgets import QApplication

import sys


def main():
    application = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(application.exec())


if __name__ == '__main__':
    main()
