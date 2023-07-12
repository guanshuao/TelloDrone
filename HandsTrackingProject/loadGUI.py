"加载GUI文件"

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5 import uic

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = uic.loadUi("UI01.ui")

    ui.show()

    app.exec_()

