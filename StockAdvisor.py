# coding: utf-8
# version: 0.01a

import sys
import Scrapper

if "" in sys.path:
    sys.path.remove("")

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QAbstractItemView, QListView, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QDesktopServices, QCursor, QFont
#from PyQt5.QtCore import * @Not use yet

class frame_main(QWidget):
    ## field area ##
    font_lab_n = QFont("나눔고딕", 10)
    font_btn1_n = QFont("나눔바탕", 12)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.sel =      QLabel("종목 선택")                 # QLabels list
        self.sel.setFont(self.font_lab_n)
        self.info =     QLabel("종목 정보")
        self.info.setFont(self.font_lab_n)

        self.list_s = QListView(self)                       # ListView and setting
        self.list_s.resize(300, 500)
        # Load saved Data..

        self.table_info_stock = QTableWidget(self)          # QTableWidget and setting
        self.table_info_stock.resize(300, 500)
        self.table_info_stock.setRowCount(24)
        self.table_info_stock.setColumnCount(2)
        self.table_info_stock.setEditTriggers(QAbstractItemView.NoEditTriggers)


        # add Item on Table
        self.setTableItem1()

        self.window_news = QPushButton("경제 뉴스")         # Buttons list
        self.window_news.setFont(self.font_btn1_n)
        self.window_port = QPushButton("포트폴리오 현황")
        self.window_port.setFont(self.font_btn1_n)

        vbox_l = QVBoxLayout()                              # Layout list
        vbox_l.addWidget(self.sel)
        vbox_l.addWidget(self.list_s)

        vbox_r = QVBoxLayout()
        vbox_r.addWidget(self.info)
        vbox_r.addWidget(self.table_info_stock)
        vbox_r.addWidget(self.window_news)
        vbox_r.addWidget(self.window_port)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox_l)
        hbox.addStretch(1)
        hbox.addLayout(vbox_r)

        self.setLayout(hbox)                                # setting
        self.setWindowIcon(QIcon('images\SAS.png'))
        self.setWindowTitle("Stock Advisor System")
        self.move(300, 300)
        self.setFixedSize(600, 500)

    def setTableItem1(self):
        # set item of main table
        send_url = Scrapper.getURL(9, "007070")
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

def main():
    app = QApplication(sys.argv)
    ex = frame_main()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
