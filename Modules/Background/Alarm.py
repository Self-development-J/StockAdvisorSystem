import sys, time
import datetime
from PyQt5 import QtCore

class checkBuyingTime(QtCore.QThread):
    def run(self):
        while True:
            print("작동중")
            time.sleep(1)

if __name__ == '__main__':
    print(str(datetime.date.today().year))