# -*- coding: utf-8 -*-
"""
@Time ： 2024/5/10 10:37
@Auth ： Ethan
@File ：MessageBox.py
@IDE ：PyCharm
"""

from PySide2.QtWidgets import QWidget
from PySide2.QtCore import Qt, QPoint

from ui.ui_MessageBox import Ui_MessageBox

class MassageBox(QWidget, Ui_MessageBox):
    def __init__(self):
        super(MassageBox, self).__init__()
        self.setupUi(self)

        # 初始化该页面所需函数
        self.init_variable()                                            # 初始化页面所需变量
        self.init_ui_style()                                            # 初始化页面风格

        # 绑定按钮
        self.btn_close.clicked.connect(self.close)                      # 点击右上角按钮关闭界面
        self.btn_ok.clicked.connect(self.close)                         # 点击ok关闭界面

    def init_variable(self):
        '''
        初始化此页面所需的变量
        :return:    None
        '''
        self._move_drag = False

    def init_ui_style(self):
        '''
        初始化此页面页面风格
        :return:    None
        '''
        self.setWindowFlags(Qt.FramelessWindowHint)                     # 去掉由系统默认绘制的标题栏

        self.btn_close.setStyleSheet(u"font-family:\"Webdings\";\n")    # 设置符号字体
        self.btn_close.setText('r')                                     # r代表符号字体X

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.widget_tittle.setMouseTracking(True)                       # 设置标题栏鼠标追踪

    def show_message(self, msg1: str, msg2: str, block=False):
        '''
        弹出窗口，显示消息
        :param msg1:    标题栏显示的提示，简短的一句话
        :param msg2:    主体内容
        :param block:   是否阻塞主窗体
        :return:        None
        '''
        if block:
            self.lb_msg.setText(msg1)                       # 设置标题栏提示内容
            self.te_msg.setText(msg2)                       # 设置主体内容
            self.setWindowModality(Qt.ApplicationModal)     # 在该窗体未关闭时，禁用主窗口
            self.show()                                     # 显示该窗体
        else:
            self.lb_msg.setText(msg1)                       # 设置标题栏提示内容
            self.te_msg.setText(msg2)                       # 设置主体内容
            self.show()                                     # 显示该窗体



    def mousePressEvent(self, event):
        '''
        重写mousePressEvent函数，鼠标点击后，确定所点击的区域（拖拽只在固定区域生效）
        :param event:   QT事件
        :return:        None
        '''
        if (event.button() == Qt.LeftButton) and (event.y() < self.widget_tittle.height()):
            self._move_drag = True                                      # 鼠标左键点击标题栏区域
            self.move_DragPosition = event.globalPos() - self.pos()     # 获取界面需要移动到的位置
            event.accept()

    def mouseMoveEvent(self, event):
        '''
        重写mouseMoveEvent函数，调整页面整体位置
        :param event:   QT事件
        :return:        None
        '''
        # 当鼠标左键点击标题栏时，调整页面整体位置
        if Qt.LeftButton and self._move_drag:
            self.move(event.globalPos() - self.move_DragPosition)       # 标题栏调整窗口整体位置
            event.accept()

    def mouseReleaseEvent(self, event):
        '''
        重写mouseReleaseEvent函数，鼠标释放后，各控制变量复位
        :param event:   QT事件
        :return:        None
        '''
        self._move_drag = False                                         # 窗口整体拖动变量复位
