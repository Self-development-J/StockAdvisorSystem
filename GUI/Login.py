# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_loginFrame(object):
    def setupUi(self, loginFrame):
        loginFrame.setObjectName("loginFrame")
        loginFrame.resize(320, 160)
        self.horizontalLayoutWidget = QtWidgets.QWidget(loginFrame)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 321, 161))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.Title = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("휴먼둥근헤드라인")
        font.setPointSize(12)
        self.Title.setFont(font)
        self.Title.setObjectName("Title")
        self.verticalLayout.addWidget(self.Title)
        self.lab1 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lab1.setObjectName("lab1")
        self.verticalLayout.addWidget(self.lab1)
        self.lab2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lab2.setObjectName("lab2")
        self.verticalLayout.addWidget(self.lab2)
        self.lab3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lab3.setObjectName("lab3")
        self.verticalLayout.addWidget(self.lab3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.loginBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.loginBtn.setObjectName("loginBtn")
        self.verticalLayout.addWidget(self.loginBtn)
        self.exitBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.exitBtn.setObjectName("exitBtn")
        self.verticalLayout.addWidget(self.exitBtn)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)

        self.retranslateUi(loginFrame)
        QtCore.QMetaObject.connectSlotsByName(loginFrame)

    def retranslateUi(self, loginFrame):
        _translate = QtCore.QCoreApplication.translate
        loginFrame.setWindowTitle(_translate("loginFrame", "StockAdvisor"))
        self.Title.setText(_translate("loginFrame", "StockAdvisor ver_0.1a"))
        self.lab1.setText(_translate("loginFrame", "API제공 증권사: 키움증권"))
        self.lab2.setText(_translate("loginFrame", "제작자: 이웃집 J"))
        self.lab3.setText(_translate("loginFrame", "(※아직 제작중에 있는 프로그램입니다.)"))
        self.loginBtn.setText(_translate("loginFrame", "로그인"))
        self.exitBtn.setText(_translate("loginFrame", "종료"))