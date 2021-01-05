import sys, time, re

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QTableWidget, QBoxLayout, QTableWidgetItem, QAbstractItemView, QListWidget, QListWidgetItem, QMessageBox, QGroupBox, QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout, QInputDialog, QHBoxLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import QtCore

from GUI.MoreInfo import Ui_MainWindow as Ui_InfoWindow

class InfoWindow(QDialog, Ui_InfoWindow):
    def __init__(self, parent=None):
        super(InfoWindow, self).__init__(parent)
        self.setupUi(self)
        self.setModal(True)
        self.setWindowIcon(QIcon("Images/favicon.png"))
        self.setFixedSize(self.size())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = InfoWindow()
    myWindow.show()
    sys.exit(app.exec_())
        

