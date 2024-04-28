# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(2375, 1188)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_16 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.widget_main = QWidget(self.centralwidget)
        self.widget_main.setObjectName(u"widget_main")
        self.verticalLayout_15 = QVBoxLayout(self.widget_main)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.widget_tittle = QWidget(self.widget_main)
        self.widget_tittle.setObjectName(u"widget_tittle")
        self.horizontalLayout_26 = QHBoxLayout(self.widget_tittle)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.lb_picture = QLabel(self.widget_tittle)
        self.lb_picture.setObjectName(u"lb_picture")

        self.horizontalLayout_25.addWidget(self.lb_picture)

        self.lb_content = QLabel(self.widget_tittle)
        self.lb_content.setObjectName(u"lb_content")

        self.horizontalLayout_25.addWidget(self.lb_content)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer)

        self.btn_min = QPushButton(self.widget_tittle)
        self.btn_min.setObjectName(u"btn_min")

        self.horizontalLayout_25.addWidget(self.btn_min)

        self.btn_max = QPushButton(self.widget_tittle)
        self.btn_max.setObjectName(u"btn_max")

        self.horizontalLayout_25.addWidget(self.btn_max)

        self.btn_close = QPushButton(self.widget_tittle)
        self.btn_close.setObjectName(u"btn_close")

        self.horizontalLayout_25.addWidget(self.btn_close)


        self.horizontalLayout_26.addLayout(self.horizontalLayout_25)


        self.verticalLayout_14.addWidget(self.widget_tittle)

        self.widget_menu = QWidget(self.widget_main)
        self.widget_menu.setObjectName(u"widget_menu")
        self.horizontalLayout_28 = QHBoxLayout(self.widget_menu)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.pushButton = QPushButton(self.widget_menu)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_27.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.widget_menu)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_27.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.widget_menu)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_27.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.widget_menu)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_27.addWidget(self.pushButton_4)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_27.addItem(self.horizontalSpacer_2)


        self.horizontalLayout_28.addLayout(self.horizontalLayout_27)


        self.verticalLayout_14.addWidget(self.widget_menu)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.widget_tools = QWidget(self.widget_main)
        self.widget_tools.setObjectName(u"widget_tools")
        self.verticalLayout_13 = QVBoxLayout(self.widget_tools)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.tabWidget = QTabWidget(self.widget_tools)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_12 = QVBoxLayout(self.tab)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.groupBox_2 = QGroupBox(self.tab)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_8.addWidget(self.label_8)

        self.le_joint1 = QLineEdit(self.groupBox_2)
        self.le_joint1.setObjectName(u"le_joint1")

        self.horizontalLayout_8.addWidget(self.le_joint1)

        self.label_19 = QLabel(self.groupBox_2)
        self.label_19.setObjectName(u"label_19")

        self.horizontalLayout_8.addWidget(self.label_19)

        self.horizontalLayout_8.setStretch(0, 1)
        self.horizontalLayout_8.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.sld_joint1 = QSlider(self.groupBox_2)
        self.sld_joint1.setObjectName(u"sld_joint1")
        self.sld_joint1.setOrientation(Qt.Horizontal)

        self.verticalLayout.addWidget(self.sld_joint1)


        self.verticalLayout_8.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_11.addWidget(self.label_11)

        self.le_joint2 = QLineEdit(self.groupBox_2)
        self.le_joint2.setObjectName(u"le_joint2")

        self.horizontalLayout_11.addWidget(self.le_joint2)

        self.label_20 = QLabel(self.groupBox_2)
        self.label_20.setObjectName(u"label_20")

        self.horizontalLayout_11.addWidget(self.label_20)

        self.horizontalLayout_11.setStretch(0, 1)
        self.horizontalLayout_11.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_11)

        self.sld_joint2 = QSlider(self.groupBox_2)
        self.sld_joint2.setObjectName(u"sld_joint2")
        self.sld_joint2.setOrientation(Qt.Horizontal)

        self.verticalLayout_2.addWidget(self.sld_joint2)


        self.verticalLayout_8.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_12 = QLabel(self.groupBox_2)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_12.addWidget(self.label_12)

        self.le_joint3 = QLineEdit(self.groupBox_2)
        self.le_joint3.setObjectName(u"le_joint3")

        self.horizontalLayout_12.addWidget(self.le_joint3)

        self.label_33 = QLabel(self.groupBox_2)
        self.label_33.setObjectName(u"label_33")

        self.horizontalLayout_12.addWidget(self.label_33)

        self.horizontalLayout_12.setStretch(0, 1)
        self.horizontalLayout_12.setStretch(1, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_12)

        self.sld_joint3 = QSlider(self.groupBox_2)
        self.sld_joint3.setObjectName(u"sld_joint3")
        self.sld_joint3.setOrientation(Qt.Horizontal)

        self.verticalLayout_3.addWidget(self.sld_joint3)


        self.verticalLayout_8.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_9.addWidget(self.label_9)

        self.le_joint4 = QLineEdit(self.groupBox_2)
        self.le_joint4.setObjectName(u"le_joint4")

        self.horizontalLayout_9.addWidget(self.le_joint4)

        self.label_46 = QLabel(self.groupBox_2)
        self.label_46.setObjectName(u"label_46")

        self.horizontalLayout_9.addWidget(self.label_46)

        self.horizontalLayout_9.setStretch(0, 1)
        self.horizontalLayout_9.setStretch(1, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_9)

        self.sld_joint4 = QSlider(self.groupBox_2)
        self.sld_joint4.setObjectName(u"sld_joint4")
        self.sld_joint4.setOrientation(Qt.Horizontal)

        self.verticalLayout_4.addWidget(self.sld_joint4)


        self.verticalLayout_8.addLayout(self.verticalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_7.addWidget(self.label_7)

        self.le_joint5 = QLineEdit(self.groupBox_2)
        self.le_joint5.setObjectName(u"le_joint5")

        self.horizontalLayout_7.addWidget(self.le_joint5)

        self.label_47 = QLabel(self.groupBox_2)
        self.label_47.setObjectName(u"label_47")

        self.horizontalLayout_7.addWidget(self.label_47)

        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        self.sld_joint5 = QSlider(self.groupBox_2)
        self.sld_joint5.setObjectName(u"sld_joint5")
        self.sld_joint5.setOrientation(Qt.Horizontal)

        self.verticalLayout_5.addWidget(self.sld_joint5)


        self.verticalLayout_8.addLayout(self.verticalLayout_5)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_10 = QLabel(self.groupBox_2)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_10.addWidget(self.label_10)

        self.le_joint6 = QLineEdit(self.groupBox_2)
        self.le_joint6.setObjectName(u"le_joint6")

        self.horizontalLayout_10.addWidget(self.le_joint6)

        self.label_48 = QLabel(self.groupBox_2)
        self.label_48.setObjectName(u"label_48")

        self.horizontalLayout_10.addWidget(self.label_48)

        self.horizontalLayout_10.setStretch(0, 1)
        self.horizontalLayout_10.setStretch(1, 1)

        self.verticalLayout_6.addLayout(self.horizontalLayout_10)

        self.sld_joint6 = QSlider(self.groupBox_2)
        self.sld_joint6.setObjectName(u"sld_joint6")
        self.sld_joint6.setOrientation(Qt.Horizontal)

        self.verticalLayout_6.addWidget(self.sld_joint6)


        self.verticalLayout_8.addLayout(self.verticalLayout_6)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer)


        self.verticalLayout_12.addWidget(self.groupBox_2)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout_13.addWidget(self.tabWidget)


        self.horizontalLayout_31.addWidget(self.widget_tools)

        self.widget_3D = QWidget(self.widget_main)
        self.widget_3D.setObjectName(u"widget_3D")
        self.horizontalLayout_30 = QHBoxLayout(self.widget_3D)
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.layout_3D = QHBoxLayout()
        self.layout_3D.setObjectName(u"layout_3D")

        self.horizontalLayout_30.addLayout(self.layout_3D)


        self.horizontalLayout_31.addWidget(self.widget_3D)

        self.widget_message = QWidget(self.widget_main)
        self.widget_message.setObjectName(u"widget_message")
        self.verticalLayout_11 = QVBoxLayout(self.widget_message)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.groupBox = QGroupBox(self.widget_message)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.le_x = QLineEdit(self.groupBox)
        self.le_x.setObjectName(u"le_x")

        self.horizontalLayout.addWidget(self.le_x)

        self.label_27 = QLabel(self.groupBox)
        self.label_27.setObjectName(u"label_27")

        self.horizontalLayout.addWidget(self.label_27)


        self.verticalLayout_7.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.le_y = QLineEdit(self.groupBox)
        self.le_y.setObjectName(u"le_y")

        self.horizontalLayout_2.addWidget(self.le_y)

        self.label_28 = QLabel(self.groupBox)
        self.label_28.setObjectName(u"label_28")

        self.horizontalLayout_2.addWidget(self.label_28)


        self.verticalLayout_7.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.le_z = QLineEdit(self.groupBox)
        self.le_z.setObjectName(u"le_z")

        self.horizontalLayout_3.addWidget(self.le_z)

        self.label_29 = QLabel(self.groupBox)
        self.label_29.setObjectName(u"label_29")

        self.horizontalLayout_3.addWidget(self.label_29)


        self.verticalLayout_7.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.le_rx = QLineEdit(self.groupBox)
        self.le_rx.setObjectName(u"le_rx")

        self.horizontalLayout_4.addWidget(self.le_rx)

        self.label_30 = QLabel(self.groupBox)
        self.label_30.setObjectName(u"label_30")

        self.horizontalLayout_4.addWidget(self.label_30)


        self.verticalLayout_7.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.le_ry = QLineEdit(self.groupBox)
        self.le_ry.setObjectName(u"le_ry")

        self.horizontalLayout_5.addWidget(self.le_ry)

        self.label_31 = QLabel(self.groupBox)
        self.label_31.setObjectName(u"label_31")

        self.horizontalLayout_5.addWidget(self.label_31)


        self.verticalLayout_7.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_6.addWidget(self.label_6)

        self.le_rz = QLineEdit(self.groupBox)
        self.le_rz.setObjectName(u"le_rz")

        self.horizontalLayout_6.addWidget(self.le_rz)

        self.label_32 = QLabel(self.groupBox)
        self.label_32.setObjectName(u"label_32")

        self.horizontalLayout_6.addWidget(self.label_32)


        self.verticalLayout_7.addLayout(self.horizontalLayout_6)


        self.verticalLayout_11.addWidget(self.groupBox)

        self.groupBox_3 = QGroupBox(self.widget_message)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_14 = QLabel(self.groupBox_3)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_14.addWidget(self.label_14)

        self.le_angle1 = QLineEdit(self.groupBox_3)
        self.le_angle1.setObjectName(u"le_angle1")

        self.horizontalLayout_14.addWidget(self.le_angle1)

        self.label_21 = QLabel(self.groupBox_3)
        self.label_21.setObjectName(u"label_21")

        self.horizontalLayout_14.addWidget(self.label_21)


        self.verticalLayout_9.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_17 = QLabel(self.groupBox_3)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_17.addWidget(self.label_17)

        self.le_angle2 = QLineEdit(self.groupBox_3)
        self.le_angle2.setObjectName(u"le_angle2")

        self.horizontalLayout_17.addWidget(self.le_angle2)

        self.label_22 = QLabel(self.groupBox_3)
        self.label_22.setObjectName(u"label_22")

        self.horizontalLayout_17.addWidget(self.label_22)


        self.verticalLayout_9.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_18 = QLabel(self.groupBox_3)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_18.addWidget(self.label_18)

        self.le_angle3 = QLineEdit(self.groupBox_3)
        self.le_angle3.setObjectName(u"le_angle3")

        self.horizontalLayout_18.addWidget(self.le_angle3)

        self.label_23 = QLabel(self.groupBox_3)
        self.label_23.setObjectName(u"label_23")

        self.horizontalLayout_18.addWidget(self.label_23)


        self.verticalLayout_9.addLayout(self.horizontalLayout_18)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_15 = QLabel(self.groupBox_3)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_15.addWidget(self.label_15)

        self.le_angle4 = QLineEdit(self.groupBox_3)
        self.le_angle4.setObjectName(u"le_angle4")

        self.horizontalLayout_15.addWidget(self.le_angle4)

        self.label_24 = QLabel(self.groupBox_3)
        self.label_24.setObjectName(u"label_24")

        self.horizontalLayout_15.addWidget(self.label_24)


        self.verticalLayout_9.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_13 = QLabel(self.groupBox_3)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_13.addWidget(self.label_13)

        self.le_angle5 = QLineEdit(self.groupBox_3)
        self.le_angle5.setObjectName(u"le_angle5")

        self.horizontalLayout_13.addWidget(self.le_angle5)

        self.label_25 = QLabel(self.groupBox_3)
        self.label_25.setObjectName(u"label_25")

        self.horizontalLayout_13.addWidget(self.label_25)


        self.verticalLayout_9.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_16 = QLabel(self.groupBox_3)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_16.addWidget(self.label_16)

        self.le_angle6 = QLineEdit(self.groupBox_3)
        self.le_angle6.setObjectName(u"le_angle6")

        self.horizontalLayout_16.addWidget(self.le_angle6)

        self.label_26 = QLabel(self.groupBox_3)
        self.label_26.setObjectName(u"label_26")

        self.horizontalLayout_16.addWidget(self.label_26)


        self.verticalLayout_9.addLayout(self.horizontalLayout_16)


        self.verticalLayout_11.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.widget_message)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_34 = QLabel(self.groupBox_4)
        self.label_34.setObjectName(u"label_34")

        self.horizontalLayout_19.addWidget(self.label_34)

        self.le_radian1 = QLineEdit(self.groupBox_4)
        self.le_radian1.setObjectName(u"le_radian1")

        self.horizontalLayout_19.addWidget(self.le_radian1)

        self.label_35 = QLabel(self.groupBox_4)
        self.label_35.setObjectName(u"label_35")

        self.horizontalLayout_19.addWidget(self.label_35)


        self.verticalLayout_10.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.label_42 = QLabel(self.groupBox_4)
        self.label_42.setObjectName(u"label_42")

        self.horizontalLayout_23.addWidget(self.label_42)

        self.le_radian2 = QLineEdit(self.groupBox_4)
        self.le_radian2.setObjectName(u"le_radian2")

        self.horizontalLayout_23.addWidget(self.le_radian2)

        self.label_43 = QLabel(self.groupBox_4)
        self.label_43.setObjectName(u"label_43")

        self.horizontalLayout_23.addWidget(self.label_43)


        self.verticalLayout_10.addLayout(self.horizontalLayout_23)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_36 = QLabel(self.groupBox_4)
        self.label_36.setObjectName(u"label_36")

        self.horizontalLayout_20.addWidget(self.label_36)

        self.le_radian3 = QLineEdit(self.groupBox_4)
        self.le_radian3.setObjectName(u"le_radian3")

        self.horizontalLayout_20.addWidget(self.le_radian3)

        self.label_37 = QLabel(self.groupBox_4)
        self.label_37.setObjectName(u"label_37")

        self.horizontalLayout_20.addWidget(self.label_37)


        self.verticalLayout_10.addLayout(self.horizontalLayout_20)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.label_40 = QLabel(self.groupBox_4)
        self.label_40.setObjectName(u"label_40")

        self.horizontalLayout_22.addWidget(self.label_40)

        self.le_radian4 = QLineEdit(self.groupBox_4)
        self.le_radian4.setObjectName(u"le_radian4")

        self.horizontalLayout_22.addWidget(self.le_radian4)

        self.label_41 = QLabel(self.groupBox_4)
        self.label_41.setObjectName(u"label_41")

        self.horizontalLayout_22.addWidget(self.label_41)


        self.verticalLayout_10.addLayout(self.horizontalLayout_22)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.label_38 = QLabel(self.groupBox_4)
        self.label_38.setObjectName(u"label_38")

        self.horizontalLayout_21.addWidget(self.label_38)

        self.le_radian5 = QLineEdit(self.groupBox_4)
        self.le_radian5.setObjectName(u"le_radian5")

        self.horizontalLayout_21.addWidget(self.le_radian5)

        self.label_39 = QLabel(self.groupBox_4)
        self.label_39.setObjectName(u"label_39")

        self.horizontalLayout_21.addWidget(self.label_39)


        self.verticalLayout_10.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.label_44 = QLabel(self.groupBox_4)
        self.label_44.setObjectName(u"label_44")

        self.horizontalLayout_24.addWidget(self.label_44)

        self.le_radian6 = QLineEdit(self.groupBox_4)
        self.le_radian6.setObjectName(u"le_radian6")

        self.horizontalLayout_24.addWidget(self.le_radian6)

        self.label_45 = QLabel(self.groupBox_4)
        self.label_45.setObjectName(u"label_45")

        self.horizontalLayout_24.addWidget(self.label_45)


        self.verticalLayout_10.addLayout(self.horizontalLayout_24)


        self.verticalLayout_11.addWidget(self.groupBox_4)


        self.horizontalLayout_31.addWidget(self.widget_message)

        self.horizontalLayout_31.setStretch(0, 2)
        self.horizontalLayout_31.setStretch(1, 15)
        self.horizontalLayout_31.setStretch(2, 1)

        self.verticalLayout_14.addLayout(self.horizontalLayout_31)


        self.verticalLayout_15.addLayout(self.verticalLayout_14)


        self.verticalLayout_16.addWidget(self.widget_main)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.lb_picture.setText(QCoreApplication.translate("MainWindow", u"PIC", None))
        self.lb_content.setText(QCoreApplication.translate("MainWindow", u"Content", None))
        self.btn_min.setText(QCoreApplication.translate("MainWindow", u"Min", None))
        self.btn_max.setText(QCoreApplication.translate("MainWindow", u"Max/Min", None))
        self.btn_close.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u673a\u68b0\u81c2\u6a21\u578b\u63a7\u5236", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"joint1", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"\u00b0", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"joint2", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"\u00b0", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"joint3", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"\u00b0", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"joint4", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"\u00b0", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"joint5", None))
        self.label_47.setText(QCoreApplication.translate("MainWindow", u"\u00b0", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"joint6", None))
        self.label_48.setText(QCoreApplication.translate("MainWindow", u"\u00b0", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"TCP-Pose", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"X ", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"m  ", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Y ", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"m  ", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Z ", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"m  ", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"RX", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"rad", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"RY", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"rad", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"RZ", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"rad", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Angle", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"J1", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"\u00b0 ", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"J2", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"\u00b0 ", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"J3", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"\u00b0 ", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"J4", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"\u00b0 ", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"J5", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"\u00b0 ", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"J6", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"\u00b0 ", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Radian", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"J1", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"rad", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"J2", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"rad", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"J3", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"rad", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"J4", None))
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"rad", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"J5", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"rad", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"J6", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"rad", None))
    # retranslateUi

