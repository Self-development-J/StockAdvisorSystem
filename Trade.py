#!/usr/bin/env python
# coding: utf-8

import sys, time
from PyQt5 import QtCore
from PyQt5.QAxContainer import QAxWidget
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QInputDialog, QLabel, QLineEdit, QListWidgetItem, QMessageBox, QPushButton, QTableWidgetItem, QTextEdit, QVBoxLayout
from PyQt5.QtGui import QBrush, QColor, QIcon
from PyQt5.QtCore import QThread

from Modules.Background.Tray import SystemTrayIcon

trade_class = uic.loadUiType("GUI/Qt/TradeWindow.ui")[0]

# 실시간 기능(미구현)
# checkBuyingTime : 매수 타이밍을 결정하기 위한 QThread 상속 클래스
# checkWhenTheSell : 매도 타이밍을 결정하기 위한 QThread 상속 클래스

class checkBuyingTime(QThread):
    test = 0

    def run(self):
        while self.test <= 10:
            print("작동중")
            time.sleep(1)
            self.test += 1
        print("종료")

class checkWhenTheSell(QThread):
    test = 0

    def run(self):
        while self.test <= 10:
            print("작동중")
            time.sleep(1)
            self.test += 1
        print("종료")

'''
변수명              기능                                    위젯 종류
sell_all_stock: 보유 주식 일괄 매도                         QPushButton
lookup_market:  장 조회                                    QPushButton 
account_box:    계좌 목록 보여줌                            QComboBox
holding_list:   해당 계좌에 보유중인 주식 목록과 상세 정보    QTableWidget
buy_sell_list:  매수/매도가 진행된 내역들을 표시함           QTextEdit
dep_res:        예수금 결과                                 QLabel
withdraw_res:   출금가능금액 결과                             QLabel
order_res:      주문가능금액 결과                            QLabel
cash_res:       현금미수금 결과                             QLabel
total_res:      현금미수금합계 결과                           QLabel
'''

class TradeWindow(QDialog, trade_class):
    connect = None

    def __init__(self, parent=None, connect=None, tray=None):
        super(TradeWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon("Images/favicon.png"))
        self.setFixedSize(self.size())

        # connect & tray
        self.connect = connect
        self.connect.OnReceiveTrData.connect(self.recieve_data)
        self.connect.OnReceiveChejanData.connect(self.receive_chejan_data)

        self.tray = tray

        self.init_account()
        self.sell_all_stock.clicked.connect(self.event_sell_stock)
        self.account_box.currentIndexChanged.connect(self.event_change_account)

    # Events
    def event_buy_stock(self):
        print("주식을 매수함: ")

    def event_sell_stock(self):
        print("주식을 매도함: ")

    def event_change_account(self):
        try:
            if self.account_box.currentText() == "(종목 선택)":
                self.holding_list.clear()
            else:
                # ↓사용안함
                # text, ok = QInputDialog.getText(self, 'password', "계좌 비밀번호를 입력하세요.", QLineEdit.Password)

                if True:
                    try:
                        self.connect.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_box.currentText())
                        call = self.connect.dynamicCall("CommRqData(QString, QString, int, QString)", "opw00001_req", "opw00001", 0, "2000")
                        
                        if call == '0' or call == 0:
                            self.buy_sell_list.append("계좌 조회: "+self.account_box.currentText())
                        else:
                            print(call)

                        # 계좌평가 및 잔고내역 요청
                        self.connect.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_box.currentText())
                        self.connect.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", 00)
                        self.connect.dynamicCall("SetInputValue(QString, QString)", "조회구분", 2)

                        call2 = self.connect.dynamicCall("CommRqData(QString, QString, int, QString)", "opw00018_req", "opw00018", 0, "2000")

                        if call2 == '0' or call2 == 0:
                            self.buy_sell_list.append("계좌 수익률 정보 조회: "+self.account_box.currentText())
                        else:
                            print(call)

                    except AttributeError as e:
                        QMessageBox.warning(self, 'Warning', "종목을 선택해 주세요!", QMessageBox.Ok)

        except Exception as e:
            print(e.args)
            print("change_account_event 동작오류!")

    # reciever
    def receive_chejan_data(self, gubun, item_cnt, fid_list):
        pass
        
    def recieve_data(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        try:
            if err_code == None:
                print("오류!", err_code)
                return

            if rqname == "opw00001_req":
                # 현재 일부만 사용중
                result = []

                res = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "예수금")
                res2 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "주식증거금현금")
                res3 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "수익증권증거금현금")
                res4 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "익일수익증권매도정산대금")
                res5 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "해외주식원화대용설정금")
                res6 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "신용보증금현금")
                res7 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "신용담보금현금")
                res8 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "추가담보금현금")
                res9 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "기타증거금")
                res10 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "미수확보금")
                res11 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "공매도대금")
                res12 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "신용설정평가금")
                res13 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "수표입금액")
                res14 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "기타수표입금액")
                res15 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "신용담보재사용")
                res16 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "코넥스기본예탁금")
                res17 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "ELW예탁평가금")
                res18 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "신용대주권리예정금액")
                res19 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "생계형가입금액")
                res20 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "생계형입금가능금액")
                res21 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "대용금평가금액(합계)")
                res22 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "잔고대용평가금액")
                res23 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "위탁대응잔고평가금액")
                res24 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "수익증권대용평가금액")
                res25 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "위탁증거금대용")
                res26 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "신용보증금대용")
                res27 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "신용담보금대용")
                res28 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "추가담보금대용")
                res29 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "권리대용금")
                res30 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "출금가능금액")
                res31 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "랩출금가능금액")
                res32 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "주문가능금액")
                res33 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "수익증권매수가능금액")
                res34 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "20%종목주문가능금액")
                res35 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "30%종목주문가능금액")
                res36 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "40%종목주문가능금액")
                res37 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "100%종목주문가능금액")
                res38 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "현금미수금")
                res39 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "현금미수연체료")
                res40 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "현금미수금합계")
                res41 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "신용이자미납")
                res42 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "신용이자미납연체료")
                res43 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "신용이자미수금합계")
                res44 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "기타대여금")
                res45 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "기타대여금연체료")
                res46 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "기타대여금합계")
                res47 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "미상환융자금")
                res48 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "융자금합계")
                res49 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "대주금합계")
                res50 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "신용담보비율")
                res51 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "중도이용료")
                res52 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "최소주문가능금액")
                res53 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "대출총평가금액")
                res54 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "예탁담보대출잔고")
                res55 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "d+1추정예수금")
                res56 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "d+1매도매수정산금")
                res57 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "d+1매수정산금")
                res58 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "d+1미수변제소요금")
                res59 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "d+1출금가능금액")
                res60 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "d+1추정예수금")
                res61 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "d+2매도매수정산금")
                res62 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "d+2매수정산금")
                res63 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "d+2미수변제소요금")
                res64 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "d+2출금가능금액")
                res65 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "출력건수")
                res66 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "통화코드")
                res67 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "외화예수금")
                res68 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "원화대용평가금")
                res69 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "해외주식증거금")
                res70 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "출금가능금액")
                res71 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "주문가능금액")

                result.append(res.lstrip("0"))
                result.append(res30.lstrip("0"))
                result.append(res32.lstrip("0"))
                result.append(res38.lstrip("0"))
                result.append(res40.lstrip("0"))

                # 받아온 결과에 0밖에 없어서 아무것도 출력이 안되는경우, 0을 대신 setText한다.
                setting = []

                for r in range(0, 5):
                    if result[r] == "" or result[r] == None:
                        setting.append("0")
                    else:
                        setting.append(result[r])

                self.dep_res.setText(setting[0])
                self.withdraw_res.setText(setting[1])
                self.order_res.setText(setting[2])
                self.cash_res.setText(setting[3])
                self.total_res.setText(setting[4])

            elif rqname == "opw00004_req":
                print("미구현: "+rqname)

            elif rqname == "opt00081_req":
                print("미구현: "+rqname)
            
            # 계좌수익률 요청
            elif rqname == "opw00018_req":
                # total_purchase = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "총매입금액")
                # total_evaluation = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "총평가금액")
                # total_valuation_gain_or_loss = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "총평가손익금액")
                # total_return = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "총수익률")
                # estimated_deposited_assets = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "추정예탁자산")
                # total_loan = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "총대출금")
                # total_loan_amount = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "총융자금액")
                # total_loan_amount2 = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "총대주금액")
                num = self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "조회건수")

                # print("총매입금액: "+total_purchase)
                # print("총평가금액: "+total_evaluation)
                # print("총평가손익금액: "+total_valuation_gain_or_loss)
                # print("총수익률(%): "+total_return)
                # print("추정예탁자산: "+estimated_deposited_assets)
                # print("총대출금: "+total_loan)
                # print("총융자금액: "+total_loan_amount)
                # print("총대주금액: "+total_loan_amount2)
                # print("조회건수: "+num)
                # print("---------------------------------------------------------------------------------")

                # 조회건수를 통한 반복 횟수 지정
                num_res = int(num.lstrip("0"))

                for i in range(0, num_res):
                    '''
                    종목번호: res
                    종목명: res2
                    평가손익: res3
                    수익률(%): res4
                    매입가: res5
                    전일종가: res6
                    보유수량: res7
                    매매가능수량: res8
                    현재가: res9
                    전일매수수량: res10
                    전일매도수량: res11
                    금일매수수량: res12
                    금일매도수량: res13
                    매입금액: res14
                    매입수수료: res15
                    평가금액: res16
                    평가수수료: res17
                    세금: res18
                    수수료합: res19
                    보유비중(%): res20
                    신용구분: res21
                    신용구분명: res22
                    대출일: res23
                    '''
                    result = []

                    result.append(self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "종목번호"))
                    result.append(self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "종목명"))
                    result.append(self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "평가손익"))
                    result.append(self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "수익률(%)"))
                    result.append(self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "매입가"))
                    result.append(self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "전일종가"))
                    result.append(self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "보유수량"))
                    result.append(self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "매매가능수량"))
                    result.append(self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "현재가"))
                    result.append(self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "전일매수수량"))
                    result.append(self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "전일매도수량"))
                    result.append(self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "금일매수수량"))
                    result.append(self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "금일매도수량"))
                    result.append(self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "매입금액"))
                    result.append(self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "매입수수료"))
                    result.append(self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "평가금액"))
                    result.append(self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "평가수수료"))
                    result.append(self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "세금"))
                    result.append(self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "수수료합"))
                    result.append(self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "보유비중(%)"))
                    result.append(self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "신용구분"))
                    result.append(self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "신용구분명"))
                    result.append(self.connect.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "대출일"))

                    setting = []

                    for j in range(0, len(result)):
                        if '+' in result[j]:
                            tmp = QTableWidgetItem("▲"+result[j].lstrip("+").lstrip("0"))
                            tmp.setForeground(QBrush(QColor(255, 0, 0)))
                            setting.append(tmp)
                        elif '-' in result[j]:
                            tmp = QTableWidgetItem("▼"+result[j].lstrip("-").lstrip("0"))
                            tmp.setForeground(QBrush(QColor(0, 0, 255)))
                            setting.append(tmp)
                        else:
                            tmp = QTableWidgetItem(result[j].lstrip("+").lstrip("-").lstrip("0"))
                            tmp.setForeground(QBrush(QColor(0, 0, 0)))
                            setting.append(tmp)

                    self.holding_list.setItem(i, 0, setting[1])
                    self.holding_list.setItem(i, 1, setting[2])
                    self.holding_list.setItem(i, 2, setting[3])
                    self.holding_list.setItem(i, 3, setting[6])
                    self.holding_list.setItem(i, 4, setting[4])
                    self.holding_list.setItem(i, 5, setting[8])
                    self.holding_list.setItem(i, 6, setting[13])
                    self.holding_list.setItem(i, 7, setting[15])
                    self.holding_list.setItem(i, 8, setting[14])
                    self.holding_list.setItem(i, 9, setting[16])
                    self.holding_list.setItem(i, 10, setting[18])
                    self.holding_list.setItem(i, 11, setting[17])

        except AttributeError as e:
            print(e.args)
            print("recieveData 오류!")

    # init
    def init_account(self):
        account = self.connect.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
        res = account.rstrip(';')
        hog = self.connect.dynamicCall("GetLoginInfo(QString)", "ACCOUNT_CNT")
        user_id = self.connect.dynamicCall("GetLoginInfo(QString)", "USER_ID")
        user_name = self.connect.dynamicCall("GetLoginInfo(QString)", "USER_NAME")

        self.account_box.addItem("(종목 선택)")
        self.account_box.addItem(res)

        self.buy_sell_list.append("현재 사용자: "+user_name+"("+user_id+")")


# 모듈 동작 테스트를 위해 사용되는 클래스. 사용시 주석을 풀고 사용
# class TradeTestCaller(QDialog):
#     connect = None
    
#     is_login_access = False

#     def __init__(self, parent=None):
#         super(TradeTestCaller, self).__init__(parent)
#         self.init_UI()
#         # self.init_background()

#     def init_UI(self):
#         self.lab = QLabel("테스트를 위한 로그인 윈도우")

#         self.login = QPushButton("로그인")
#         self.login.clicked.connect(self.init_API)
#         self.check = QPushButton("확인")
#         self.login.clicked.connect(self.chk_login)

#         vbox = QVBoxLayout()
#         vbox.addWidget(self.lab)
#         vbox.addWidget(self.login)
#         vbox.addWidget(self.check)

#         self.setLayout(vbox)
#         self.setWindowTitle("사용자 정보")
#         self.setWindowModality(QtCore.Qt.ApplicationModal)
#         self.resize(300, 200)

#     def init_background(self):
#         self.alarm_buy = checkBuyingTime()
#         self.alarm_buy.start()

#     def init_API(self):
#         try:
#             self.connect = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
#             self.connect.dynamicCall("CommConnect()")
#         except AttributeError as e:
#             QMessageBox.critical(self, 'Program execution error!', "실행에 실패했습니다! 32비트 가상환경을 설정 후 실행해 주세요!", QMessageBox.Ok)
#             exit(-10)

#     def chk_login(self):
#         self.connect.OnEventConnect.connect(self.event_connect)

#     def event_connect(self, err_code):
#         if err_code == 0:
#             print("로그인 성공")
#             window = TradeWindow(connect=self.connect)
#             window.exec_()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     myWindow = TradeTestCaller()
#     myWindow.show()
#     sys.exit(app.exec_())
