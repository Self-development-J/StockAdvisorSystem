import sys, datetime

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QIcon, QStandardItemModel

from PyQt5 import uic

form_class = uic.loadUiType("GUI/Qt/MoreInfo.ui")[0]

'''
변수명                                       기능                                    위젯 종류
more_info                                상세정보 + 종목명                          QLabel
type_fi_stat:                            재무제표 중류 선택                          QComboBox
stat_tab                                재무제표 상세항목이 담긴 표를 표시함          QTabWidget
tab_comprehensive_income_statement:      포괄손익계산서 탭                           QWidget
tab_financial_statement:                  재무상태표 탭                              QWidget
tab_cash_flow_statement:                현금흐름표 탭                                QWidget
table_comprehensive_income_statement:   포괄손익계산서 테이블
table_financial_statement:              재무상태표 테이블
table_cash_flow_statement:   포괄손익계산서 테이블
month_stat:                             연간 라디오버튼
year_stat:                              분기 라디오버튼
search:                                 검색 버튼                                       QPushButton
menubar:                                메뉴바                                        QMenuBar
menu_help:                                    '도움말'메뉴                               QComboBox
menu_file:                               '파일'메뉴                                 QTableWidget
statusBar:                              상태표시줄                                   QStatusBar
'''

class InfoWindow(QMainWindow, form_class):
    def __init__(self, parent=None, code=None):
        super(InfoWindow, self).__init__(parent)
        self.setupUi(self)
        
        if code == None:
            QMessageBox.critical(self, 'Warning', "종목정보를 가져올 수 없습니다! 다시 시도해주세요!", QMessageBox.Ok)
            self.close()
        self.more_info.setText("상세정보 항목("+code+")")

        self.setWindowIcon(QIcon("Images/favicon.png"))
        self.setFixedSize(self.size())
        self.search_stat_event()

        self.search.clicked.connect(self.search_stat_event)

    # Events
    def search_stat_event(self):
        # type1: 분기-0, 연도-1
        # type2: 주재무제표, IFRS(연결)-0, IFRS(별도)-1, GAAP(연결)-2, GAAP(별도)-3
        if self.month_stat.isChecked() == True:
            type1 = 0
        elif self.year_stat.isChecked() == True:
            type1 = 1
        else:
            type1 = 1

        if self.type_fi_stat.currentText() == "주재무제표" or self.stat_tab.currentText() == "IFRS(연결)":
            type2 = 0
        elif self.type_fi_stat.currentText() == "IFRS(별도)":
            type2 = 1
        elif self.type_fi_stat.currentText() == "GAAP(연결)":
            type2 = 2
        elif self.type_fi_stat.currentText() == "GAAP(별도)":
            type2 = 3
        else:
            type2 = 0

        # 이제 여기서 주어진 조건에 맞게 테이블header 세팅하는 메소드와 연결
        print(type1, type2)

    # Setting Table
    def table_year_setting(self):
        now = datetime.date.today().year

        column_header = [str(now-4)+"/12 (IFRS연결)", str(now-3)+"/12 (IFRS연결)", str(now-2)+"/12 (IFRS연결)", str(now-1)+"/12 (IFRS연결)", str(now)+"/12 (IFRS연결)"]

        self.table_comprehensive_income_statement.setHorizontalHeaderLabels(column_header)
        self.table_financial_statement.setHorizontalHeaderLabels(column_header)
        self.table_cash_flow_statement.setHorizontalHeaderLabels(column_header)

    def table_month_setting(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = InfoWindow(code="삼성전자(005930)")
    myWindow.show()
    sys.exit(app.exec_())
