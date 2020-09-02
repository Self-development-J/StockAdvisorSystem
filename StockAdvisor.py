# coding: utf-8
# version: 0.01a

import sys
import re
import Scrapper, DBSetter

if "" in sys.path:
    sys.path.remove("")

from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QTableWidget, QTableWidgetItem, QAbstractItemView, QListWidget, QListWidgetItem, QMessageBox, QListView, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QDesktopServices, QCursor, QFont, QStandardItemModel, QStandardItem
from PyQt5.QtCore import *

class frame_main(QWidget):
    ## field area ##
    font_lab_n = QFont("나눔고딕", 10)
    font_btn1_n = QFont("나눔바탕", 12)

    headStockCode = None
    ListItem = []

    def __init__(self):
        super().__init__()
        print("make class...")
        self.load_initData()    # 파일을 로드
        self.initUI()

    def initUI(self):
        print("make GUI...")
        self.sel =      QLabel("종목 선택")                 # QLabels list
        self.sel.setFont(self.font_lab_n)
        self.info =     QLabel("종목 정보")
        self.info.setFont(self.font_lab_n)

        self.list_s = QListWidget(self)                       # ListView and setting
        self.list_s.resize(300, 500)
        self.list_s.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Load saved Data..
        self.setListItem()

        self.table_info_stock = QTableWidget(self)          # QTableWidget and setting
        self.table_info_stock.resize(300, 500)
        self.table_info_stock.setRowCount(24)
        self.table_info_stock.setColumnCount(2)
        self.table_info_stock.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # add Item on Table
        self.setTableItem() # 종목 선택할 때 마다 이거 호출하도록 할까?

        self.setter_Stocks = QPushButton("추가")                 # Buttons list
        self.setter_Stocks.setFont(self.font_btn1_n)
        self.setter_Stocks.clicked.connect(self.addStocks)
        self.setter_Stocks.setIcon(QIcon('./Images/add.png'))
        self.remove_stocks = QPushButton("제거")
        self.remove_stocks.setFont(self.font_btn1_n)
        self.remove_stocks.setIcon(QIcon('.Images/remove.png'))
        self.load_stocks = QPushButton("불러오기")
        self.load_stocks.setFont(self.font_btn1_n)
        self.load_stocks.clicked.connect(self.setTableItem_re)
        self.setting = QPushButton("설정..")
        self.setting.setFont(self.font_btn1_n)
        self.setting.setIcon(QIcon('./Images/edit.png'))
        self.setting.clicked.connect(self.openSettingFrame)

        self.window_news = QPushButton("관련 기사")
        self.window_news.setFont(self.font_btn1_n)
        self.window_news.clicked.connect(self.openInformationFrame)
        self.window_port = QPushButton("선택 종목 분석")
        self.window_port.setFont(self.font_btn1_n)
        self.window_port.clicked.connect(self.openRelatedarticlesFrame)

        # Layout list
        vbox_l_btn = QHBoxLayout()                          # left LayoutBox
        vbox_l_btn.addWidget(self.setter_Stocks)
        vbox_l_btn.addWidget(self.remove_stocks)
        vbox_l_btn.addWidget(self.load_stocks)
        vbox_l_btn.addWidget(self.setting)
        vbox_l = QVBoxLayout()
        vbox_l.addWidget(self.sel)
        vbox_l.addWidget(self.list_s)
        vbox_l.addLayout(vbox_l_btn)

        vbox_r_btn = QHBoxLayout()
        vbox_r_btn.addWidget(self.window_news)
        vbox_r_btn.addWidget(self.window_port)

        vbox_r = QVBoxLayout()                              # Right LayoutBox
        vbox_r.addWidget(self.info)
        vbox_r.addWidget(self.table_info_stock)
        vbox_r.addLayout(vbox_r_btn)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox_l)
        hbox.addStretch(1)
        hbox.addLayout(vbox_r)

        # extra setting
        self.setLayout(hbox)
        self.setWindowIcon(QIcon('images\SAS.png'))
        self.setWindowTitle("Stock Advisor System")
        self.move(300, 300)
        self.setFixedSize(600, 500)

    def setListItem(self):                   # 왼쪽 리스트에 Item을 채워넣음
        for l in self.ListItem:
            item = QListWidgetItem(self.list_s)
            item.setText(l.strip())
            self.list_s.addItem(item)

    def setTableItem(self):                  # 오른쪽 Table에 아이템을 채워넣음
        # set item of main table
        send_url = Scrapper.getURL(9, self.headStockCode)
        mainSettingObject = Scrapper.URLcrawlingInfoObject(send_url)
        if mainSettingObject.code == "CASE_CONNECT_FAILED":
            exit(-1)    # 나중에 DB로 전환하는 기능을 만들어야함

        item = mainSettingObject.crawlingmainStockInfo(mainSettingObject.code)
        item_title = item['r1']
        item_attribute_comp_previousday = item['r2']
        item_attribute_nv = item['r3']
        item_attribute = item['r4']
        item_attribute_t = item['r5']

        j = 0
        for i in range(0, len(item_title)):
            self.table_info_stock.setItem(0, j, QTableWidgetItem(item_title[i]))
            j += 2

        j = 1
        for i in range(0, len(item_attribute_comp_previousday)):
            self.table_info_stock.setItem(0, j, QTableWidgetItem(item_attribute_comp_previousday[i]))
            j += 2

        for i in range(0, len(item_attribute_nv)):
            self.table_info_stock.setItem(0, j, QTableWidgetItem(item_attribute_nv[i]))
            j += 2

        for i in range(0, len(item_attribute)):
            self.table_info_stock.setItem(0, j, QTableWidgetItem(item_attribute[i]))
            j += 2

        for i in range(0, len(item_attribute_t)):
            self.table_info_stock.setItem(0, j, QTableWidgetItem(item_attribute_t[i]))
            j += 2

    def setTableItem_re(self):               # 오른쪽 Table의 아이템을 다른 종목으로 바꿈.
        data_ = self.list_s.currentItem().text()
        res = re.findall('\(([^)]+)', data_)
        self.headStockCode = res[0]
        self.setTableItem()

    def load_initData(self):                 # 설정파일을 불러옴
        print("load initData...")
        f = open("data/InitData.txt", 'r', encoding='UTF8')

        for line in f:
            if line != "head:\n":
                striphead = line.strip()
                break

        res = re.findall('\(([^)]+)', striphead)        # 괄호 안의 종목번호 추출
        self.headStockCode = res[0]                     # head로 설정된 종목 정보 세팅

        for line in f:
            if line != "list:\n":
                stripline = line.strip()
                self.ListItem.append(stripline)

        f.close()

    def addStocks(self):                     # (미구현) add버튼을 누르면 종목을 추가하는 로직 실행
        f = open("./data/InitData.txt", "a")
        f.close()

    def removeStocks(self):                   # (미구현) remove버튼을 누르면 종목을 제거하는 로직 실행
        pass

    # 다이얼로그 오픈 함수
    def openSettingFrame(self):              # 설정창 열기
        frame_setting(self)

    def openInformationFrame(self):          # 관련기사 창 열기
        frame_MoreInformation(self)

    def openRelatedarticlesFrame(self):      # 설정창 열기
        frame_Relatedarticles(self)

    def closeEvent(self, event):
        cBox = QMessageBox.question(self, 'Message', "프로그램을 종료하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if cBox == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class frame_setting(QDialog):
    def __init__(self, mainframe):
        super(frame_setting, self).__init__(mainframe)
        self.initUI()

    def initUI(self):

        self.op1 = QLabel("로드 파일 설정")
        self.op1.setToolTip("처음 프로그램이 실행되면서 불러올 종목을 지정합니다.")

        self.set1 = QLineEdit()

        vbox = QVBoxLayout()
        vbox.addWidget(self.op1)
        vbox.addWidget(self.set1)

        self.setLayout(vbox)
        self.setWindowIcon(QIcon('images\SAS.png'))
        self.setWindowTitle("Setting")
        self.move(300, 300)
        self.setFixedSize(400, 400)
        self.show()

class frame_MoreInformation(QDialog):
    def __init__(self, mainframe):
        super(frame_MoreInformation, self).__init__(mainframe)
        self.initUI()

    def initUI(self):

        vbox = QVBoxLayout()

        self.setLayout(vbox)
        self.setWindowIcon(QIcon('images\SAS.png'))
        self.setWindowTitle("뉴스")
        self.move(300, 300)
        self.setFixedSize(400, 400)
        self.show()

class frame_Relatedarticles(QDialog):
    def __init__(self, mainframe):
        super(frame_Relatedarticles, self).__init__(mainframe)
        self.initUI()

    def initUI(self):

        vbox = QVBoxLayout()

        self.setLayout(vbox)
        self.setWindowIcon(QIcon('images\SAS.png'))
        # self.setWindowFlags(self Union[]) @ 언젠가 구현할 다이얼로그 창 물음표 없애닌 코드
        self.setWindowTitle("종목 분석")
        self.move(300, 300)
        self.setFixedSize(400, 400)
        self.show()

def main():
    app = QApplication(sys.argv)
    ex = frame_main()
    print("create complete.")
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
