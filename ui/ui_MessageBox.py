# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MessageBox.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MessageBox(object):
    def setupUi(self, MessageBox):
        if not MessageBox.objectName():
            MessageBox.setObjectName(u"MessageBox")
        MessageBox.resize(461, 182)
        self.verticalLayout_5 = QVBoxLayout(MessageBox)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.widget_tittle = QWidget(MessageBox)
        self.widget_tittle.setObjectName(u"widget_tittle")
        self.verticalLayout_3 = QVBoxLayout(self.widget_tittle)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lb_msg = QLabel(self.widget_tittle)
        self.lb_msg.setObjectName(u"lb_msg")

        self.horizontalLayout.addWidget(self.lb_msg)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_close = QPushButton(self.widget_tittle)
        self.btn_close.setObjectName(u"btn_close")

        self.horizontalLayout.addWidget(self.btn_close)


        self.verticalLayout_3.addLayout(self.horizontalLayout)


        self.verticalLayout_4.addWidget(self.widget_tittle)

        self.widget_main = QWidget(MessageBox)
        self.widget_main.setObjectName(u"widget_main")
        self.verticalLayout_2 = QVBoxLayout(self.widget_main)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.te_msg = QTextEdit(self.widget_main)
        self.te_msg.setObjectName(u"te_msg")

        self.verticalLayout.addWidget(self.te_msg)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.btn_ok = QPushButton(self.widget_main)
        self.btn_ok.setObjectName(u"btn_ok")

        self.horizontalLayout_3.addWidget(self.btn_ok)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.verticalLayout.setStretch(0, 8)
        self.verticalLayout.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.verticalLayout_4.addWidget(self.widget_main)

        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(1, 8)

        self.verticalLayout_5.addLayout(self.verticalLayout_4)


        self.retranslateUi(MessageBox)

        QMetaObject.connectSlotsByName(MessageBox)
    # setupUi

    def retranslateUi(self, MessageBox):
        MessageBox.setWindowTitle(QCoreApplication.translate("MessageBox", u"Form", None))
        self.lb_msg.setText(QCoreApplication.translate("MessageBox", u"Robot", None))
        self.btn_close.setText("")
        self.btn_ok.setText(QCoreApplication.translate("MessageBox", u"OK", None))
    # retranslateUi

