#!/usr/bin/env python
# coding: utf-8

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon

from PyQt5 import uic

trade_class = uic.loadUiType("GUI/Qt/TradeWindow.ui")[0]

class TradeWindow(QMainWindow, trade_class):
    def __init__(self, parent=None):
        super(TradeWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon("Images/favicon.png"))
        self.setFixedSize(self.size())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = TradeWindow()
    myWindow.show()
    sys.exit(app.exec_())
