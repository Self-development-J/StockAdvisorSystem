import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
from PyQt5.QAxContainer import QAxWidget

from StockAdvisor import frame_main

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 300, 150)
        self.setWindowIcon(QIcon('images\SAS.png'))
        try:
            self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        except Exception as e:
            e.with_traceback()

        btn1 = QPushButton("Login", self)
        btn1.move(20, 20)
        btn1.clicked.connect(self.btn1_clicked)

        btn2 = QPushButton("Check state", self)
        btn2.move(20, 70)
        btn2.clicked.connect(self.btn2_clicked)

    def btn1_clicked(self):
        ret = self.kiwoom.dynamicCall("CommConnect()")
        if self.kiwoom.dynamicCall("GetConnectState()") == 0:
            self.hide()
            ap = frame_main()
            ap.show()

    def btn2_clicked(self):
        if self.kiwoom.dynamicCall("GetConnectState()") == 0:
            self.statusBar().showMessage("Not connected")
        elif self.kiwoom.dynamicCall("GetConnectState()") == 1:
            self.statusBar().showMessage("Connected")
            # self.hide()
            # ap = frame_main()
            # ap.show()
        else:
            print("오류!")
            exit(-1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = LoginWindow()
    myWindow.show()
    app.exec_()