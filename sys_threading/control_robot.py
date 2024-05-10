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
        self.DH = DH()                                          # 初始化DH算法


    def joint_rotation(self, joint_num: int, angle: float):
        '''
        旋转UI界面上的机械臂模型
        :param joint_num:   关节序号 1~6
        :param angle:       旋转角度(需要达到的角度)
        :return: None
        '''
        cur_rad = self.MainWin.joint_angles[joint_num-1]                                    # 记录当前角度
        self.MainWin.joint_angles[joint_num-1] = angle                                      # 更新改变后的角度

        for i in range(6):
            self.MainWin.joint_radians[i] = self.MainWin.joint_angles[i] * np.pi / 180      # 更新改变后的弧度

        self.MainWin.TCP_pose = self.DH.DH_FK(self.MainWin.joint_angles)[0]                 # 更新TCP位姿

        self.joint_vector(self.MainWin.joint_radians)                                       # 计算各个关节需要旋转的角度

        # 刷新模型角度
        for key in range(joint_num, 7):
            for mesh in self.MainWin.robot_joint_mesh[key]:
                if joint_num == 1:
                    rotation_center = self.MainWin.robot_joint_mesh[joint_num-1][0].center      # 获取模型旋转中心点
                    axis = [self.MainWin.robot_joint_vector[1][0, 0],                           # 计算模型旋转法向量
                            self.MainWin.robot_joint_vector[1][1, 0],
                            self.MainWin.robot_joint_vector[1][2, 0]]
                    mesh.rotate_vector(axis, angle - cur_rad, rotation_center, inplace=True)    # 通过法向量、中心点旋转模型
                elif joint_num == 2:
                    rotation_center = self.MainWin.robot_joint_mesh[joint_num-1][0].center
                    axis = [self.MainWin.robot_joint_vector[2][0, 0],
                            self.MainWin.robot_joint_vector[2][1, 0],
                            self.MainWin.robot_joint_vector[2][2, 0]]
                    mesh.rotate_vector(axis, angle - cur_rad, rotation_center, inplace=True)
                elif joint_num == 3:
                    rotation_center = self.MainWin.robot_joint_mesh[joint_num-1][-1].center
                    axis = [self.MainWin.robot_joint_vector[3][0, 0],
                            self.MainWin.robot_joint_vector[3][1, 0],
                            self.MainWin.robot_joint_vector[3][2, 0]]
                    mesh.rotate_vector(axis, angle - cur_rad, rotation_center, inplace=True)
                elif joint_num == 4:
                    rotation_center = self.MainWin.robot_joint_mesh[joint_num-1][-1].center
                    axis = [self.MainWin.robot_joint_vector[4][0, 0],
                            self.MainWin.robot_joint_vector[4][1, 0],
                            self.MainWin.robot_joint_vector[4][2, 0]]
                    mesh.rotate_vector(axis, angle - cur_rad, rotation_center, inplace=True)
                elif joint_num == 5:
                    rotation_center = self.MainWin.robot_joint_mesh[joint_num-1][-1].center
                    axis = [self.MainWin.robot_joint_vector[5][0, 0],
                            self.MainWin.robot_joint_vector[5][1, 0],
                            self.MainWin.robot_joint_vector[5][2, 0]]
                    mesh.rotate_vector(axis, angle - cur_rad, rotation_center, inplace=True)
                elif joint_num == 6:
                    rotation_center = self.MainWin.robot_joint_mesh[joint_num][0].center
                    axis = [self.MainWin.robot_joint_vector[6][0, 0],
                            self.MainWin.robot_joint_vector[6][1, 0],
                            self.MainWin.robot_joint_vector[6][2, 0]]
                    mesh.rotate_vector(axis, angle - cur_rad, rotation_center, inplace=True)

    def joint_vector(self, joint):
        '''
        用DH旋转矩阵，计算各个关节旋转所需的vector
        算法：R*V=V，旋转矩阵 * 法向量 = 旋转后的法向量，可以理解为对法向量V进行旋转
        :param joint_num:   机械臂6轴的弧度列表
        :return:            None
        '''
        vec = np.matrix([[0], [0], [1], [1]])               # 初始化Z轴单位向量

        # 计算joint1旋转向量
        T01 = self.DH.DH_T(joint[0], 0, 0, self.DH.DH_alpha1)
        self.MainWin.robot_joint_vector[2] = T01 * vec

        # 计算joint2旋转向量
        T12 = self.DH.DH_T(joint[1], 0, 0, self.DH.DH_alpha2)
        self.MainWin.robot_joint_vector[3] = T01 * T12 * vec

        # 计算joint3旋转向量
        T23 = self.DH.DH_T(joint[2], 0, 0, self.DH.DH_alpha3)
        self.MainWin.robot_joint_vector[4] = T01 * T12 * T23 * vec

        # 计算joint4旋转向量
        T34 = self.DH.DH_T(joint[3], 0, 0, self.DH.DH_alpha4)
        self.MainWin.robot_joint_vector[5] = T01 * T12 * T23 * T34 * vec

        # 计算joint5旋转向量
        T45 = self.DH.DH_T(joint[4], 0, 0, self.DH.DH_alpha5)
        self.MainWin.robot_joint_vector[6] = T01 * T12 * T23 * T34 * T45 * vec



