# coding: utf-8
# version: 0.10a

import sys, time, re

from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QWidget, QDialog, QTableWidget, QBoxLayout, QTableWidgetItem, QAbstractItemView, QListWidget, QListWidgetItem, QMessageBox, QGroupBox, QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout, QInputDialog, QHBoxLayout
from PyQt5.QtGui import QCloseEvent, QIcon, QFont
from PyQt5 import QtCore
from PyQt5.QAxContainer import QAxWidget

from Info import InfoWindow

from GUI.OptionDlg import Ui_OptionDialog

class OptionDialog(QDialog, Ui_OptionDialog):
    def __init__(self, parent=None):
        super(OptionDialog, self).__init__(parent)
        self.setModal(True)
        self.setupUi(self)

        self.checkBtn.clicked.connect(self.checkConnectionEvent)
        self.buttonBox.accepted.connect(self.accept) 
        self.buttonBox.rejected.connect(self.reject) 
        self.infoUsr.clicked.connect(self.loadLoginUserInfoEvent)

    def loadLoginUserInfoEvent(self):
        res = []
        try:
            res.append(MainWindow.connect.dynamicCall("GetLoginInfo(ACCLIST)"))
            res.append(MainWindow.connect.dynamicCall("GetLoginInfo(USER_NAME)"))
            res.append(MainWindow.connect.dynamicCall("GetLoginInfo(USER_ID)"))
            res.append(MainWindow.connect.dynamicCall("GetLoginInfo(GetServerGubun)"))
            print(res)
        except AttributeError as e:
            print(e.args)
            self.connectServer()

    def connectServer(self):
        msg = QMessageBox.information(self, '알림', "서버에 연결되어 있지 않습니다. 연결하시겠습니까?", QMessageBox.Yes|QMessageBox.No)
        if msg == QMessageBox.Yes:
            MainWindow.connect = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
            MainWindow.connect.dynamicCall("CommConnect()")
        elif msg == QMessageBox.No:
            return

    def checkConnectionEvent(self):
        try:
            res = MainWindow.connect.dynamicCall("GetConnectState()")
            if res == 1:
                msg = QMessageBox.information(self, '알림', "서버에 연결되어 있습니다.", QMessageBox.Ok)
                if msg == QMessageBox.Ok:
                    return
            elif res == 0:
                self.connectServer()
        except AttributeError as e:
            print(e.args)
            self.connectServer()

class MainWindow(QDialog):
    connect = None

    font_lab_n = QFont("나눔고딕", 10)
    font_btn1_n = QFont("나눔바탕", 12)

    __ListItem = []

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.initUI()
        self.loadInitData()

    def initUI(self):
        # QLabels list
        self.sel = QLabel("종목 선택")                      
        self.sel.setFont(self.font_lab_n)
        self.info = QLabel("종목 정보")
        self.info.setFont(self.font_lab_n)
        self.info.setText("종목 정보")

        # QlineEdit list
        self.search = QLineEdit(self)

        # ListView and setting
        self.list_s = QListWidget(self)                         
        self.list_s.resize(300, 500)
        self.list_s.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # QTableWidget and setting
        self.table_info_stock = QTableWidget(self)
        self.table_info_stock.resize(300, 500)
        self.table_info_stock.setRowCount(24)
        self.table_info_stock.setColumnCount(2)
        self.table_info_stock.verticalHeader().setVisible(False)
        self.table_info_stock.horizontalHeader().setVisible(False)
        self.table_info_stock.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.table_info_stock.setItem(0, 0, QTableWidgetItem("1"))
        self.table_info_stock.setItem(1, 0, QTableWidgetItem("2"))
        self.table_info_stock.setItem(2, 0, QTableWidgetItem("3"))
        self.table_info_stock.setItem(3, 0, QTableWidgetItem("4"))
        self.table_info_stock.setItem(4, 0, QTableWidgetItem("5"))
        self.table_info_stock.setItem(5, 0, QTableWidgetItem("6"))
        self.table_info_stock.setItem(6, 0, QTableWidgetItem("7"))
        self.table_info_stock.setItem(7, 0, QTableWidgetItem("8"))

        # Buttons list
        self.setter_Stocks = QPushButton("추가")
        self.setter_Stocks.setFont(self.font_btn1_n)
        self.setter_Stocks.setIcon(QIcon('./Images/add.png'))
        self.setter_Stocks.clicked.connect(self.addStocks)
        self.remove_stocks = QPushButton("제거")
        self.remove_stocks.setFont(self.font_btn1_n)
        self.remove_stocks.setIcon(QIcon('./Images/remove.png'))
        self.load_stocks = QPushButton("불러오기")
        self.load_stocks.setFont(self.font_btn1_n)
        self.setting = QPushButton("설정..")
        self.setting.setFont(self.font_btn1_n)
        self.setting.setIcon(QIcon('./Images/edit.png'))
        self.setting.clicked.connect(self.optionEvent)
        self.search_btn = QPushButton("검색")
        self.search_btn.setFont(self.font_btn1_n)
        self.search_btn.clicked.connect(self.searchEvent)
        self.window_news = QPushButton("관련 기사")
        self.window_news.setFont(self.font_btn1_n)
        self.window_port = QPushButton("선택 종목 분석")
        self.window_port.setFont(self.font_btn1_n)
        self.window_port.clicked.connect(self.moreInformationEvent)
        
        # Layout list
        vbox_l_btn = QHBoxLayout()                              # left LayoutBox
        vbox_l_btn.addWidget(self.setter_Stocks)
        vbox_l_btn.addWidget(self.remove_stocks)
        vbox_l_btn.addWidget(self.load_stocks)
        vbox_l_btn.addWidget(self.setting)
        vbox_l_search = QHBoxLayout()
        vbox_l_search.addWidget(self.search)
        vbox_l_search.addWidget(self.search_btn)
        vbox_l = QVBoxLayout()
        vbox_l.addWidget(self.sel)
        vbox_l.addLayout(vbox_l_search)
        vbox_l.addWidget(self.list_s)
        vbox_l.addLayout(vbox_l_btn)

        vbox_r_btn = QHBoxLayout()                              # Right LayoutBox
        vbox_r_btn.addWidget(self.window_news)
        vbox_r_btn.addWidget(self.window_port)

        vbox_r = QVBoxLayout()
        vbox_r.addWidget(self.info)
        vbox_r.addWidget(self.table_info_stock)
        vbox_r.addLayout(vbox_r_btn)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox_l)
        hbox.addStretch(1)
        hbox.addLayout(vbox_r)

        self.setLayout(hbox)                                    # extra setting
        self.setWindowIcon(QIcon("./Images/favicon.png"))
        self.setWindowTitle("Stock Advisor System")
        self.move(300, 300)
        self.setFixedSize(640, 480)

    #Events
    def closeEvent(self, closeEvent=QCloseEvent()):  # window close event
        wantExit = QMessageBox.question(self, '종료?', "프로그램을 종료하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if wantExit == QMessageBox.Yes:
            exit(0)
        elif wantExit == QMessageBox.No:
            closeEvent.ignore()

    def searchEvent(self):
        if self.search.text() == "" or self.search.text() == None:
            QMessageBox.warning(self, 'Warning', "검색어를 입력해 주세요!", QMessageBox.Ok)
            return

        name = self.search.text()

        # OpenAPI+ Event
        self.connect.OnReceiveTrData.connect(self.recieveData)

        # SetInputValue
        self.connect.dynamicCall("SetInputValue(QString, QString)", "종목코드", name)

        # CommRqData
        self.connect.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10001_req", "opt10001", 0, "0101")
        self.info.setText("종목코드: " + name)


    def connectEvent(self, err_code):
        if err_code == 0:
            print("로그인 성공")

    def recieveData(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        if err_code == None:
            print("오류!", err_code)
            return

        if rqname == "opt10001_req":
            print("CommGet>>>")
            # CommGetData <<< 곧 사용이 중단된다고 한다..다른 방법을 빨리 알아보도록 하자.
            name = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "종목명")  
            volume = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "거래량")
            price = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "현재가")

            print("종목명: " + name.strip())
            print("거래량: " + volume.strip())
            print("현재가: " + price.strip())

    def optionEvent(self):
        optionDlog = OptionDialog(self)
        optionDlog.show()

    def newsEvent(self):
        pass

    def moreInformationEvent(self):
        info = InfoWindow(self)
        info.show()

    #initialize method
    def loadInitData(self):                                    # 설정파일을 불러옴
        # 1. load list in left window
        with open("./Data/InitData.txt", 'r', encoding='UTF8') as f:
            for line in f:
                if line != "list:\n":
                    self.__ListItem.append(line.strip())

        for l in self.__ListItem:
            item = QListWidgetItem(self.list_s)
            item.setText(l.strip())
            self.list_s.addItem(item)
        # 2. etc..

        # res = re.findall('\(([^)]+)', striphead)                # 괄호 안의 종목번호 추출

    def addStocks(self):                                        # add버튼을 누르면 종목을 추가하는 로직 실행
        text, ok = QInputDialog.getText(self, 'add', "[종목명(종목번호)] 형식으로 입력")

        if ok:
            with open("./data/InitData.txt", "a", encoding='utf8') as f:
                if text == "":
                    print("없음")
                    return

                f.write("  "+text)
                item = QListWidgetItem(self.list_s)
                item.setText(text)
                self.list_s.addItem(item)

    # Getter and Setter
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
    