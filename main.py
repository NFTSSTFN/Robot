# -*- coding: utf-8 -*-
"""
@Time ： 2024/4/25 17:26
@Auth ： Ethan
@File ：MainWindow.py
@IDE ：PyCharm
"""

from PySide2.QtWidgets import QApplication

from ui_control.MainWindow import MainWindow

class Main:
    def __init__(self):
        super(Main, self).__init__()
        self.Main = MainWindow()

    def check_license(self):
        '''
        检查许可
        :return:
        '''
        pass

    def display(self):
        self.Main.show()

if __name__ == '__main__':
    app = QApplication([])
    main = Main()
    main.display()
    app.exec_()












