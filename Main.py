# coding: utf-8
# version: 0.10a

import sys

from PyQt5.QtWidgets import QAction, QApplication, QWidget, QDialog, QTableWidget, QBoxLayout, QTableWidgetItem, QAbstractItemView, QListWidget, QListWidgetItem, QMessageBox, QGroupBox, QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout, QInputDialog, QHBoxLayout
from PyQt5.QtGui import QCloseEvent, QIcon, QFont
from PyQt5 import QtCore
from PyQt5.QAxContainer import QAxWidget
from PyQt5 import uic

from Info import InfoWindow
from Trade import TradeWindow

opt_class = uic.loadUiType("GUI/Qt/SysOption.ui")[0]

class OptionDialog(QDialog, opt_class):

    def __init__(self, parent=None):
        super(OptionDialog, self).__init__(parent)
        self.setModal(True)
        self.setupUi(self)

        self.checkBtn.clicked.connect(self.checkConnectionEvent)
        self.buttonBox.accepted.connect(self.accept) 
        self.buttonBox.rejected.connect(self.reject) 
        self.infoUsr.clicked.connect(self.loadLoginUserInfoEvent)
    # 현재 이부분을 사용하기 위한 버튼이 준비가 안됨!
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
    
    def btn1_clicked(self): # 접속된 사용자의 계좌 정보를 가져오는 함수(현재 미사용)
        account_num = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
        self.text_edit.append("계좌번호: " + account_num.rstrip(';'))

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

class MainWindow(QWidget):
    # 현재 선택된 종목(이름, 코드)
    stock_now = None
    stock_now_code = None

    connect = None
    # fonts
    font_lab_n = QFont("나눔고딕", 10)
    font_btn1_n = QFont("나눔바탕", 12)

    __ListItem = []

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.server_connect()
        self.initUI()
        self.load_init_data()

    def initUI(self):
        # QAction list
        # 1) common
        viewAction = QAction("종목 조회", self)     # 2) FavoriteList
        removeAction = QAction("제거", self)

        # QLabels list
        self.sel = QLabel("종목 검색")                      
        self.sel.setFont(self.font_lab_n)
        self.fav = QLabel("관심 종목")                      
        self.fav.setFont(self.font_lab_n)
        self.info = QLabel("종목 정보")
        self.info.setFont(self.font_lab_n)

        # QlineEdit list
        self.search = QLineEdit(self)

        # ListView and setting
        self.list_s = QListWidget(self)                         
        self.list_s.resize(300, 500)
        self.list_s.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.list_s.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.list_s.addAction(viewAction)
        self.list_s.addAction(removeAction)

        # QTableWidget and setting
        self.table_info_stock = QTableWidget(self)
        self.table_info_stock.resize(300, 500)
        self.table_info_stock.setRowCount(23)
        self.table_info_stock.setColumnCount(2)
        self.table_info_stock.verticalHeader().setVisible(False)
        self.table_info_stock.horizontalHeader().setVisible(False)
        self.table_info_stock.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_info_stock.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        self.table_info_stock.setItem(0, 0, QTableWidgetItem("현재가"))
        self.table_info_stock.setItem(1, 0, QTableWidgetItem("시가"))
        self.table_info_stock.setItem(2, 0, QTableWidgetItem("고가"))
        self.table_info_stock.setItem(3, 0, QTableWidgetItem("저가"))
        self.table_info_stock.setItem(4, 0, QTableWidgetItem("거래량"))
        self.table_info_stock.setItem(5, 0, QTableWidgetItem("거래대비"))
        self.table_info_stock.setItem(6, 0, QTableWidgetItem("상한가"))
        self.table_info_stock.setItem(7, 0, QTableWidgetItem("하한가"))
        self.table_info_stock.setItem(8, 0, QTableWidgetItem("기준가"))
        self.table_info_stock.setItem(9, 0, QTableWidgetItem("전일대비"))
        self.table_info_stock.setItem(10, 0, QTableWidgetItem("액면가"))
        self.table_info_stock.setItem(11, 0, QTableWidgetItem("연중최고"))
        self.table_info_stock.setItem(12, 0, QTableWidgetItem("연중최저"))
        self.table_info_stock.setItem(13, 0, QTableWidgetItem("등락율"))
        self.table_info_stock.setItem(14, 0, QTableWidgetItem("ROE"))
        self.table_info_stock.setItem(15, 0, QTableWidgetItem("PER"))
        self.table_info_stock.setItem(16, 0, QTableWidgetItem("PBR"))
        self.table_info_stock.setItem(17, 0, QTableWidgetItem("EV"))
        self.table_info_stock.setItem(18, 0, QTableWidgetItem("BPS"))
        self.table_info_stock.setItem(19, 0, QTableWidgetItem("시가총액"))
        self.table_info_stock.setItem(20, 0, QTableWidgetItem("상장주식수"))
        self.table_info_stock.setItem(21, 0, QTableWidgetItem("외인소진률"))
        self.table_info_stock.setItem(22, 0, QTableWidgetItem("자본금"))

        # Buttons list
        self.setter_Stocks = QPushButton("추가")
        self.setter_Stocks.setFont(self.font_btn1_n)
        self.setter_Stocks.setIcon(QIcon('./Images/add.png'))
        self.setter_Stocks.clicked.connect(self.add_favorite_event)
        self.remove_stocks = QPushButton("제거")
        self.remove_stocks.setFont(self.font_btn1_n)
        self.remove_stocks.setIcon(QIcon('./Images/remove.png'))
        self.remove_stocks.clicked.connect(self.remove_favorite_event)
        self.load_stocks = QPushButton("종목 조회")
        self.load_stocks.setFont(self.font_btn1_n)
        self.load_stocks.clicked.connect(self.remove_favorite_event)
        self.setting = QPushButton("설정..")
        self.setting.setFont(self.font_btn1_n)
        self.setting.setIcon(QIcon('./Images/edit.png'))
        self.setting.clicked.connect(self.option_event)
        self.search_btn = QPushButton("검색")
        self.search_btn.setFont(self.font_btn1_n)
        self.search_btn.clicked.connect(self.searchEvent)
        self.window_trade = QPushButton("주식 거래")
        self.window_trade.setFont(self.font_btn1_n)
        self.window_trade.clicked.connect(self.trade_event)
        self.window_port = QPushButton("현재 종목 분석")
        self.window_port.setFont(self.font_btn1_n)
        self.window_port.clicked.connect(self.more_info_event)
        
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
        vbox_l.addWidget(self.fav)
        vbox_l.addWidget(self.list_s)
        vbox_l.addLayout(vbox_l_btn)

        vbox_r_btn = QHBoxLayout()                              # Right LayoutBox
        vbox_r_btn.addWidget(self.window_trade)
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
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.move(300, 300)
        self.setFixedSize(self.size())

    #Events
    def closeEvent(self, closeEvent=QCloseEvent()):             # window close event
        wantExit = QMessageBox.question(self, '종료?', "프로그램을 종료하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if wantExit == QMessageBox.Yes:
            exit(0)
        elif wantExit == QMessageBox.No:
            closeEvent.ignore()

    def add_favorite_event(self):                                    # add버튼을 누르면 종목을 추가하는 로직 실행
        text, ok = QInputDialog.getText(self, 'add', "종목번호를 입력")

        if ok:
            try:
                # OpenAPI+ add favorite Event
                self.connect.OnReceiveTrData.connect(self.search_favorite_data)

                # SetInputValue
                self.connect.dynamicCall("SetInputValue(QString, QString)", "종목코드", text)

                # CommRqData
                self.connect.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10001_req", "opt10001", 0, "0101")

                add = QMessageBox.question(self, '관심종목 추가', "현재 조회중인 종목:"+self.stock_now+"("+self.stock_now_code+")"+"\n추가하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
                if add == QMessageBox.Yes:
                    with open("Data/InitData.txt", "a", encoding='UTF8') as f:
                        f.write("\n   "+self.stock_now+"("+self.stock_now_code+")")

                    item = QListWidgetItem(self.list_s)
                    item.setText(self.stock_now)
                    self.list_s.addItem(item)
                elif add == QMessageBox.No:
                    return

            except AttributeError as e:
                QMessageBox.warning(self, 'Warning', "종목을 선택해 주세요!", QMessageBox.Ok)

    def remove_favorite_event(self):
        try:
            rem = QMessageBox.question(self, '관심종목 제거', "현재 선택된 종목:"+self.list_s.currentItem().text()+"\n목록에서 제거하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if rem == QMessageBox.Yes:
                listOfFile = []
                search_str = "\n    "+self.list_s.currentItem().text()
                # 설정파일에서 지우기
                with open("Data/InitData.txt", "r+", encoding='UTF8') as f:
                    for line in f:
                        if line.lower().find(search_str) != -1:
                            listOfFile.append("")
                        else:
                            res = line.strip()
                            res = res.strip("\n")
                            listOfFile.append(res)

                with open("Data/InitData.txt", "w", encoding='UTF8') as f:
                    for line in listOfFile:
                        if line == "":
                            continue
                        elif line == "list:":
                            f.writelines("%s\n" % line)
                        else:
                            f.writelines("  %s\n" % line)
                
                # 현재 목록에서 지우기
                # self.list_s.removeItemWidget()
            
            elif rem == QMessageBox.No:
                return

        except AttributeError as e:
            QMessageBox.warning(self, 'Warning', "종목을 선택해 주세요!", QMessageBox.Ok)

    def searchEvent(self):
        if self.search.text() == "" or self.search.text() == None:
            QMessageBox.warning(self, 'Warning', "검색어를 입력해 주세요!", QMessageBox.Ok)
            return

        name = self.search.text()

        try:
            # OpenAPI+ Search Event
            self.connect.OnReceiveTrData.connect(self.recieveData)
        except AttributeError as e:
            QMessageBox.warning(self, 'Warning', "API 서버에 연결되어있지 않습니다. 설정>서버 연결 확인 버튼을 눌러 서버에 연결해 주세요.", QMessageBox.Ok)
            return

        # SetInputValue
        self.connect.dynamicCall("SetInputValue(QString, QString)", "종목코드", name)

        # CommRqData
        self.connect.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10001_req", "opt10001", 0, "0101")

    def recieveData(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
                    
    # 출력 요소 변수명
    # name :                종목명
    # code :                종목코드

    # price :               현재가
    # market_price :        시가
    # high_price :          고가
    # low_price :           저가
    # volume :              거래량
    # preparation :         거래대비
    # upper_limit :         상한가
    # lower_limit :         하한가
    # center_limit :        기준가
    # prev_per :            전일대비
    # face_value :          액면가
    # high_year :           연중최고
    # low_year :            연중최저
    # rate :                등락율
    # roe :                 ROE
    # per :                 PER
    # pbr :                 PBR
    # ev :                  EV
    # bps :                 BPS
    # market_cap :          시가총액
    # listed_shares :       상장주식수
    # foreigner_per :       외인소진률
    # capital :             자본금

        if err_code == None:
            print("오류!", err_code)
            return

        if rqname == "opt10001_req":
            name =              self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "종목명")
            code =              self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "종목코드")
            market_price =      self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "시가")
            high_price =        self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "고가")
            low_price =         self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "저가")
            volume =            self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "거래량")
            preparation =       self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "거래대비")
            upper_limit =       self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "상한가")
            lower_limit =       self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "하한가")
            center_limit =      self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "기준가")
            price =             self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "현재가")
            prev_per =          self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "전일대비")
            face_value =        self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "액면가")
            high_year =         self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "연중최고")
            low_year =          self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "연중최저")
            rate =              self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "등락율")
            roe =               self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "ROE")
            per =               self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "PER")
            pbr =               self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "PBR")
            ev =                self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "EV")
            bps =               self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "BPS")
            market_cap =        self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "시가총액")
            listed_shares =     self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "상장주식수")
            foreigner_per =     self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "외인소진률")
            capital =           self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "자본금")

            self.stock_now =        name.strip()
            self.stock_now_code =   code.strip()
            self.info.setText("종목 정보("+self.stock_now+"("+self.stock_now_code+")"+")")

            self.table_info_stock.setItem(0, 1, QTableWidgetItem(market_price.strip()))
            self.table_info_stock.setItem(1, 1, QTableWidgetItem(high_price.strip()))
            self.table_info_stock.setItem(2, 1, QTableWidgetItem(low_price.strip()))
            self.table_info_stock.setItem(3, 1, QTableWidgetItem(volume.strip()))
            self.table_info_stock.setItem(4, 1, QTableWidgetItem(preparation.strip()))
            self.table_info_stock.setItem(5, 1, QTableWidgetItem(upper_limit.strip()))
            self.table_info_stock.setItem(6, 1, QTableWidgetItem(lower_limit.strip()))
            self.table_info_stock.setItem(7, 1, QTableWidgetItem(center_limit.strip()))
            self.table_info_stock.setItem(8, 1, QTableWidgetItem(price.strip()))
            self.table_info_stock.setItem(9, 1, QTableWidgetItem(prev_per.strip()))
            self.table_info_stock.setItem(10, 1, QTableWidgetItem(face_value.strip()))
            self.table_info_stock.setItem(11, 1, QTableWidgetItem(high_year.strip()))
            self.table_info_stock.setItem(12, 1, QTableWidgetItem(low_year.strip()))
            self.table_info_stock.setItem(13, 1, QTableWidgetItem(rate.strip()))
            self.table_info_stock.setItem(14, 1, QTableWidgetItem(roe.strip()))
            self.table_info_stock.setItem(15, 1, QTableWidgetItem(per.strip()))
            self.table_info_stock.setItem(16, 1, QTableWidgetItem(pbr.strip()))
            self.table_info_stock.setItem(17, 1, QTableWidgetItem(ev.strip()))
            self.table_info_stock.setItem(18, 1, QTableWidgetItem(bps.strip()))
            self.table_info_stock.setItem(19, 1, QTableWidgetItem(market_cap.strip()))
            self.table_info_stock.setItem(20, 1, QTableWidgetItem(listed_shares.strip()))
            self.table_info_stock.setItem(21, 1, QTableWidgetItem(foreigner_per.strip()))
            self.table_info_stock.setItem(22, 1, QTableWidgetItem(capital.strip()))

    def search_favorite_data(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        if err_code == None:
            print("오류!", err_code)
            return

        if rqname == "opt10001_req":
            res_name = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "종목명")
            res_code = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "종목코드")

            self.stock_now =        res_name.strip()
            self.stock_now_code =   res_code.strip()

    def option_event(self):
        optionDlog = OptionDialog(self)
        optionDlog.show()

    def trade_event(self):
        trade = TradeWindow(self)
        trade.show()

    def more_info_event(self):
        info = InfoWindow(self)
        info.show()

    #initialize method
    def server_connect(self):
        try:
            self.connect = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
            self.connect.dynamicCall("CommConnect()")
            self.connect.OnEventConnect.connect(self.event_connect)
        except AttributeError as e:
            QMessageBox.critical(self, 'Program execution error!', "실행에 실패했습니다! 32비트 가상환경을 설정 후 실행해 주세요!", QMessageBox.Ok)
            exit(-10)

    def event_connect(self, err_code):
        if err_code == 0:
            print("로그인 성공")


    def load_init_data(self):                                    # 설정파일을 불러옴
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

        # res = re.findall('\(([^)]+)', striphead)            # 괄호 안의 종목번호 추출

    # Getter and Setter

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
    