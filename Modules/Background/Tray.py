import sys
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QMessageBox, QApplication, QWidget
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        # 우클릭 메뉴
        menu = QMenu(parent)
        
        # 메뉴 요소들
        openAction = menu.addAction("열기")
        openAction.triggered.connect(self.open_action)

        setAction = menu.addAction("설정...")
        setAction.triggered.connect(self.set_action)

        line = menu.addSection("test")

        exitAction = menu.addAction("종료")
        exitAction.triggered.connect(self.exit_action)

        self.setContextMenu(menu)
        self.activated.connect(self.activation_reason)
        self.show()

    def activation_reason(self, index):
        if index == 2 :
           self.open_action()

    def trade_signal_action(self, code=None):
        self.showMessage(code+"매수 신호 발생", code+"에 대한 매수신호가 포착됬습니다.", 1, 10000)
        
    def open_action(self):
        if self.parent().isHidden():
            self.parent().show()
        else:
            return

    def set_action(self):
        try:
            self.parent().option_event()
        except AttributeError as e:
            print("실행불가!")

    def exit_action(self):
        wantExit = QMessageBox.question(self.parent(), '종료?', "프로그램을 종료하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if wantExit == QMessageBox.Yes:
            QCoreApplication.instance().quit()
        elif wantExit == QMessageBox.No:
            return

if __name__ == '__main__':
    on=r''
    app = QApplication(sys.argv)
    w = QWidget()
    trayIcon = SystemTrayIcon(QIcon('C:/Users/chess/Documents/projects/StockAdvisorSystem/Images/favicon.png'), w)
    trayIcon.showMessage("디버깅 모드", "StockAdvisor의 Tray 기능을 디버깅 모드로 실행중이며, 일부 기능이 정상적으로 작동되지 않을 수 있습니다.", 1, 10000)
    sys.exit(app.exec_())