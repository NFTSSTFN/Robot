# -*- coding: utf-8 -*-
"""
@Time ： 2024/4/26 17:22
@Auth ： Ethan
@File ：control_robot.py
@IDE ：PyCharm
"""
import numpy as np
from algorithm.kinematics import DH

class ControlRobot:

    def __init__(self, MainWin):
        self.MainWin = MainWin                                  # 接收MainWindow对象


    def joint_rotation(self, joint_num: int, angle: float):
        '''
        旋转UI界面上的机械臂模型
        :param joint_num:   关节序号
        :param angle:       旋转角度
        :return: None
        '''
        cur_rad = DH.radian_to_angle(self.MainWin.joint_angles[joint_num])     # 记录当前角度
