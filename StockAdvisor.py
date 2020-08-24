# coding: utf-8
# version: 0.01a

import sys
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
        self.table_info_stock.setRowCount(16)
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
        self.table_info_stock.setItem(0, 0, QTableWidgetItem("현재가"))
        self.table_info_stock.setItem(0, 2, QTableWidgetItem("전일대비"))
        self.table_info_stock.setItem(0, 4, QTableWidgetItem("등락률(%)"))
        self.table_info_stock.setItem(0, 6, QTableWidgetItem("거래량"))
        self.table_info_stock.setItem(0, 8, QTableWidgetItem("거래대금(백만)"))
        self.table_info_stock.setItem(0, 10, QTableWidgetItem("액면가"))
        self.table_info_stock.setItem(0, 12, QTableWidgetItem("상한가"))
        self.table_info_stock.setItem(0, 14, QTableWidgetItem("하한가"))
        self.table_info_stock.setItem(0, 16, QTableWidgetItem("전일상한"))
        self.table_info_stock.setItem(0, 18, QTableWidgetItem("전일하한"))
        self.table_info_stock.setItem(0, 20, QTableWidgetItem("매도호가"))
        self.table_info_stock.setItem(0, 22, QTableWidgetItem("매수호가"))
        self.table_info_stock.setItem(0, 24, QTableWidgetItem("전일가"))
        self.table_info_stock.setItem(0, 26, QTableWidgetItem("시가"))
        self.table_info_stock.setItem(0, 28, QTableWidgetItem("고가"))
        self.table_info_stock.setItem(0, 30, QTableWidgetItem("현재가"))
        self.table_info_stock.setItem(0, 32, QTableWidgetItem("현재가"))

def main():
    app = QApplication(sys.argv)
    ex = frame_main()
    ex.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()