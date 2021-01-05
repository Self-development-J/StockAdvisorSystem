import sys, threading

from PyQt5.QtGui import QCloseEvent, QIcon
from PyQt5.QtWidgets import QMessageBox, QWidget, QApplication
from PyQt5.QAxContainer import QAxWidget

from StockAdvisor import MainWindow
from GUI.Login import Ui_loginFrame

class LoginWindow(QWidget, Ui_loginFrame):
    connect = None

    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(None)
        self.setupUi(self)
        self.setWindowIcon(QIcon("./Images/favicon.png"))
        self.setFixedSize(self.size())

        try:
            self.connect = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
            self.connect.OnEventConnect.connect(self.connectEvent)
        except Exception as e:
            e.with_traceback()

        self.loginBtn.clicked.connect(self.loginClicked)
        self.exitBtn.clicked.connect(self.exitClicked)

    def loginClicked(self):
        self.connect.dynamicCall("CommConnect()")

    def exitClicked(self):
        self.closeEvent(QCloseEvent())

    def connectEvent(self, err_code):
        if err_code == 0:
            mainWindow = MainWindow(self)
            MainWindow.connect = self.connect
            mainWindow.show()
        else:
            print(err_code)

    # close event 처리
    def closeEvent(self, closeEvent=QCloseEvent()):
        wantExit = QMessageBox.question(self, '종료?', "프로그램을 종료하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if wantExit == QMessageBox.Yes:
            exit(0)
        elif wantExit == QMessageBox.No:
            closeEvent.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loginWindow = LoginWindow()
    loginWindow.show()
    sys.exit(app.exec_())