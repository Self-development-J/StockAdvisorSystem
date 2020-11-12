# coding: utf-8
# version: 0.10a

import sys, time, re

import Scrapper, DBSetter
import MoreInfo

if "" in sys.path:
    sys.path.remove("")

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QTableWidget, QBoxLayout, QTableWidgetItem, QAbstractItemView, QListWidget, QListWidgetItem, QMessageBox, QGroupBox, QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout, QInputDialog, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QDesktopServices, QCursor, QFont, QStandardItemModel, QStandardItem, QColor, QBrush
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import *

global ListItem
ListItem = []
global head

class frame_main(QWidget):
    ## field area ##
    font_lab_n = QFont("나눔고딕", 10)
    font_btn1_n = QFont("나눔바탕", 12)

    headStockCode = None
    global ListItem
    #################

    def __init__(self, parent=None):
        super().__init__(parent)
        print("make class...")
        self.load_initData()                                    # File load
        self.initUI()

    def initUI(self):
        print("make GUI...")
        self.sel =      QLabel("종목 선택")                      # QLabels list
        self.sel.setFont(self.font_lab_n)
        self.info =     QLabel("종목 정보")
        self.info.setFont(self.font_lab_n)

        self.search = QLineEdit(self)                          # QlineEdit list

        self.list_s = QListWidget(self)                         # ListView and setting
        self.list_s.resize(300, 500)
        self.list_s.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.setListItem()                                      # Load saved Data..

        self.table_info_stock = QTableWidget(self)              # QTableWidget and setting
        self.table_info_stock.resize(300, 500)
        self.table_info_stock.setRowCount(24)
        self.table_info_stock.setColumnCount(2)
        self.table_info_stock.verticalHeader().setVisible(False)
        self.table_info_stock.horizontalHeader().setVisible(False)
        self.table_info_stock.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # add Item on Table
        self.setTableItem()                                     # 종목 선택할 때 마다 이거 호출하도록 할까?
        self.setItemColor()

        self.setter_Stocks = QPushButton("추가")                # Buttons list
        self.setter_Stocks.setFont(self.font_btn1_n)
        self.setter_Stocks.clicked.connect(self.addStocks)
        self.setter_Stocks.setIcon(QIcon('./Images/add.png'))
        self.remove_stocks = QPushButton("제거")
        self.remove_stocks.setFont(self.font_btn1_n)
        self.remove_stocks.setIcon(QIcon('./Images/remove.png'))
        self.remove_stocks.clicked.connect(self.removeStocks)
        self.load_stocks = QPushButton("불러오기")
        self.load_stocks.setFont(self.font_btn1_n)
        self.load_stocks.clicked.connect(self.setTableItem_re)
        self.setting = QPushButton("설정..")
        self.setting.setFont(self.font_btn1_n)
        self.setting.setIcon(QIcon('./Images/edit.png'))
        self.setting.clicked.connect(self.openSettingFrame)
        self.search_btn = QPushButton("검색")
        self.search_btn.setFont(self.font_btn1_n)

        self.window_news = QPushButton("관련 기사")
        self.window_news.setFont(self.font_btn1_n)
        self.window_news.clicked.connect(self.openInformationFrame)
        self.window_port = QPushButton("선택 종목 분석")
        self.window_port.setFont(self.font_btn1_n)
        self.window_port.clicked.connect(self.openRelatedarticlesFrame)
        
        self.frame_Relatedarticles = QDialog(self)              # QDialog list
        
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
        self.setWindowIcon(QIcon('images\SAS.png'))
        self.setWindowTitle("Stock Advisor System")
        self.move(300, 300)
        self.setFixedSize(1000, 800)

    def setListItem(self):                                      # 왼쪽 리스트에 Item을 채워넣음
        for l in ListItem:
            item = QListWidgetItem(self.list_s)
            item.setText(l.strip())
            self.list_s.addItem(item)

    def setTableItem(self):                                     # 오른쪽 Table에 아이템을 채워넣음
        #lm = LoadingMsg() <----- 로딩 창
        #lm.start()
        send_url = Scrapper.getURL(9, self.headStockCode)       # set item of main table
        mainSettingObject = Scrapper.URLcrawlingInfoObject(send_url)

        item = mainSettingObject.crawlingmainStockInfo(mainSettingObject.getResultOfSoup())
        item_title = item['r1']
        item_attribute_comp_previousday = item['r2']
        item_attribute_nv = item['r3']
        item_attribute = item['r4']
        item_attribute_t = item['r5']
        global setColor
        setColor = item['r6']

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

        #lm.flag = True

    def setTableItem_re(self):                                  # 오른쪽 Table의 아이템을 다른 종목으로 바꿈.
        try:
            data_ = self.list_s.currentItem().text()
            res = re.findall('\(([^)]+)', data_)
            self.headStockCode = res[0]
            self.setTableItem()
            self.setItemColor()
        except AttributeError:
            QMessageBox.warning(self, 'Warning', "종목을 선택해 주세요!", QMessageBox.Ok)
                    
    def setItemColor(self):
        if setColor == "red":
            self.table_info_stock.item(1, 1).setForeground(QBrush(Qt.red))
            self.table_info_stock.item(2, 1).setForeground(QBrush(Qt.red))
        elif setColor == "blue":
            self.table_info_stock.item(1, 1).setForeground(QBrush(Qt.blue))
            self.table_info_stock.item(2, 1).setForeground(QBrush(Qt.blue))
        else:
            self.table_info_stock.item(1, 1).setForeground(QBrush(Qt.gray))
            self.table_info_stock.item(2, 1).setForeground(QBrush(Qt.gray))

    def load_initData(self):                                    # 설정파일을 불러옴
        global head
        striphead = None

        print("load initData...")
        f = open("data/InitData.txt", 'r', encoding='UTF8')

        for line in f:
            if line != "head:\n":
                striphead = line.strip()
                break

        res = re.findall('\(([^)]+)', striphead)                # 괄호 안의 종목번호 추출
        self.headStockCode = res[0]                             # head로 설정된 종목 정보 세팅
        head = self.headStockCode

        for line in f:
            if line != "list:\n":
                stripline = line.strip()
                ListItem.append(stripline)

        f.close()

    def addStocks(self):                                        # add버튼을 누르면 종목을 추가하는 로직 실행
        text, ok = QInputDialog.getText(self, 'add', "[종목명(종목번호)] 형식으로 입력")

        if ok:
            f = open("./data/InitData.txt", "a", encoding='utf8')
            f.write("  "+text)

            item = QListWidgetItem(self.list_s)
            item.setText(text)
            self.list_s.addItem(item)

            f.close()

    def removeStocks(self):                                     # (미구현) remove버튼을 누르면 종목을 제거하는 로직 실행
        # 요구사항
        # - 파일에서 대상 삭제 후 재정렬해야함
        # - QListWidget에서 삭제 구현
        remove_commit = QMessageBox.question(self, 'Message', "삭제하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if remove_commit == QMessageBox.Yes:
            data_ = self.list_s.currentItem().text()
            with open("./data/InitData.txt", "r") as f:
                line = f.readlines()
            f = open("./data/InitData.txt", "a", encoding='utf8')
            '''
            for l in line:
                if line.strip() == data_:
                    f.writelines(line)
                    break
            '''        
            f.close()
            self.list_s.clear()
            self.load_initData()
            self.setListItem()

        else:
            return

    # 다이얼로그 오픈 함수
    def openSettingFrame(self):              # 설정창 열기
        frame_setting(self)

    def openInformationFrame(self):          # 관련기사 창 열기
        frame_MoreInformation(self)

    def openRelatedarticlesFrame(self):      # 설정창 열기
        frame_RelatedarticlesFrame(self)

    def closeEvent(self, event):
        cBox = QMessageBox.question(self, 'Message', "프로그램을 종료하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if cBox == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class frame_setting(QDialog):
    global ListItem

    def __init__(self, parent=frame_main):
        super(frame_setting, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.accept_b = QPushButton("확인")
        self.cancel_b = QPushButton("취소")

        self.op1 = QLabel("로드 파일 설정")
        self.op1.setToolTip("처음 프로그램이 실행되면서 불러올 종목을 지정합니다.")

        self.set1 = QComboBox(self)
        self.addset1()

        self.group_normal = QGroupBox("일반 설정")

        hbox = QHBoxLayout()
        hbox.addWidget(self.op1)
        hbox.addWidget(self.set1)
        hbox.addStretch(2)

        hbox_b = QHBoxLayout()
        hbox_b.addStretch(3)
        hbox_b.addWidget(self.accept_b)
        hbox_b.addWidget(self.cancel_b)

        self.group_normal.setLayout(hbox)

        vbox = QVBoxLayout()
        vbox.addWidget(self.group_normal)
        vbox.addStretch(3)
        vbox.addLayout(hbox_b)

        self.setLayout(vbox)
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowStaysOnTopHint)   # ^ : XOR 연산자
        self.setWindowIcon(QIcon('images\SAS.png'))
        self.setWindowTitle("Setting")
        self.move(300, 300)
        self.setFixedSize(400, 400)
        self.exec_()

    def addset1(self):
        for l in ListItem:
            self.set1.addItem(l)

class frame_MoreInformation(QDialog):                           # 뉴스피드를 띄운다.(웹 브라우저)
    def __init__(self, parent=frame_main):
        super(frame_MoreInformation, self).__init__(parent)
        self.initUI()

    def initUI(self):
        global head

        news = QWebEngineView()
        news.setUrl(QUrl(Scrapper.getURL(10, head)))
        
        form = QBoxLayout(QBoxLayout.LeftToRight, self) 
        form.addWidget(news)
        
        self.setLayout(form)
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon('images\SAS.png'))
        self.setWindowTitle("뉴스")
        self.move(300, 300)
        self.setFixedSize(800, 600)
        self.exec_()                                                    # 다이얼로그 활성화시 메인 창은 비활성화되는 특성을 가지고 있다.

class frame_RelatedarticlesFrame(QMainWindow, MoreInfo.Ui_MainWindow):  # MoreInfo.py 상속
    def __init__(self, parent=frame_main):
        super(frame_RelatedarticlesFrame, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setupUi(self)
        self.tableSetting()

        

        self.setWindowTitle("종목 상세 분석")
        self.show()

    def tableSetting(self):                                             # Table widget setting here
        # setting Horizontal's time result
        time_horizontal = {
            'Year-0':time.strftime('%Y', time.localtime(time.time())) + "/12\n(IFRS연결)",
            'Year-1':time.strftime('%Y', time.localtime(time.time()-31536000.0)) + "/12\n(IFRS연결)",
            'Year-2':time.strftime('%Y', time.localtime(time.time()-63072000.0)) + "/12\n(IFRS연결)",
            'Year-3':time.strftime('%Y', time.localtime(time.time()-94608000.0)) + "/12\n(IFRS연결)",
            'Year-4':time.strftime('%Y', time.localtime(time.time()-126144000.0)) + "/12\n(IFRS연결)"
        }
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem(time_horizontal['Year-4']))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem(time_horizontal['Year-3']))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem(time_horizontal['Year-2']))
        self.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem(time_horizontal['Year-1']))
        self.tableWidget.setHorizontalHeaderItem(4, QTableWidgetItem(time_horizontal['Year-0']))
        
        # Now setting table's attribute
        # 포괄손익계산서, 재무상태표, 현금흐름표 등
        catch_resultOfTable = Scrapper.URLcrawlingInfoObject.crawlingFinancialanalysis(self)
        print(catch_resultOfTable)

class LoadingMsg(QThread):
    def __init__(self, parent=None):
        QThread.__init__(parent)
        self.cond = QWaitCondition()
        self.flag = False

    def run(self):
        l = QDialog()
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("불러오는 중입니다..."))

        l.setLayout(vbox)
        l.setFixedSize(400, 300)
        l.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        l.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        l.setWindowFlag(Qt.WindowCloseButtonHint, False)
        l.setWindowTitle("불러오는 중")
        l.setWindowIcon(QIcon('images\SAS.png'))
        l.exec_()
        self.sleep(2000)
        self.terminate()
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = frame_main()
    print("create complete.")
    ex.show()
    sys.exit(app.exec_())