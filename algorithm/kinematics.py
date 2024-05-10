# -*- coding: utf-8 -*-
"""
@Time ： 2024/4/26 16:59
@Auth ： Ethan
@File ：kinematics.py
@IDE ：PyCharm
"""

import numpy as np
from scipy.linalg import logm

class DH:
    def __init__(self):
        self.DH_a1 = 0
        self.DH_a2 = -0.425
        self.DH_a3 = -0.39225
        self.DH_a4 = 0
        self.DH_a5 = 0
        self.DH_a6 = 0

        self.DH_d1 = 0.089159
        self.DH_d2 = 0
        self.DH_d3 = 0
        self.DH_d4 = 0.10915
        self.DH_d5 = 0.09465
        self.DH_d6 = 0.0823

        self.DH_alpha1 = 90
        self.DH_alpha2 = 0
        self.DH_alpha3 = 0
        self.DH_alpha4 = 90
        self.DH_alpha5 = -90
        self.DH_alpha6 = 0

        # 将alpha的角度转为弧度
        self.DH_alpha1 = self.angle_to_radian(self.DH_alpha1)
        self.DH_alpha2 = self.angle_to_radian(self.DH_alpha2)
        self.DH_alpha3 = self.angle_to_radian(self.DH_alpha3)
        self.DH_alpha4 = self.angle_to_radian(self.DH_alpha4)
        self.DH_alpha5 = self.angle_to_radian(self.DH_alpha5)
        self.DH_alpha6 = self.angle_to_radian(self.DH_alpha6)

    def angle_to_radian(self, angle: float, precision=6):
        '''
        角度 -> 弧度
        :param angle:       角度
        :param precision:   返回值的精度，默认保留6位小数
        :return:            float: 弧度
        '''
        angle = angle * np.pi / 180
        angle = round(angle, precision)
        return angle

    def radian_to_angle(self, radian: float, precision=6):
        '''
        弧度 -> 角度
        :param radian:      弧度
        :param precision:   返回值的精度，默认保留6位小数
        :return:            float: 角度
        '''
        radian = radian * 180 / np.pi
        radian = round(radian, precision)
        return radian

    def DH_T(self, theta: float, a: float, d: float, alpha: float):
        '''
        计算 i 到 i-1 的 T矩阵
        :param theta:   弧度值
        :param a:       DH参数
        :param d:       DH参数
        :param alpha:   DH参数，弧度值
        :return:        list: 二维矩阵
        '''
        ret = [[np.cos(theta), -np.sin(theta) * np.cos(alpha), np.sin(theta) * np.sin(alpha), a * np.cos(theta)],
               [np.sin(theta), np.cos(theta) * np.cos(alpha), -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
               [0, np.sin(alpha), np.cos(alpha), d],
               [0, 0, 0, 1]]
        ret = np.matrix(ret)
        return ret

    def RV_RM(self, p: list):
        '''
        将机械臂位姿转为正运动学所得的T矩阵
        :param p:   机械臂位姿 [x, y, z, rx, ry, rz]
        :return:    list: 正解T矩阵
        '''
        # 提取位置和旋转
        x, y, z, rx, ry, rz = p
        # 计算旋转矩阵
        theta = np.sqrt(rx ** 2 + ry ** 2 + rz ** 2)
        k = np.array([rx, ry, rz]) / theta

        K = np.array([[0, -k[2], k[1]],
                      [k[2], 0, -k[0]],
                      [-k[1], k[0], 0]])

        R = np.eye(3) + np.sin(theta) * K + (1 - np.cos(theta)) * (K @ K)

        # 构造变换矩阵 T
        T = np.eye(4)
        T[0:3, 0:3] = R
        T[:3, 3] = x, y, z
        return T

    def RM_RV(self, T):
        '''
        机械臂正运动学解得的T矩阵转为机械臂位姿
        :param T:   4*4的旋转矩阵
        :return:    list: 机械臂位姿 [x, y, x, rx, ry, rz]
        '''
        R = T[:3, :3]
        cos_theta = (np.trace(R) - 1) / 2.0
        theta = np.arccos(np.clip(cos_theta, -1.0, 1.0))
        r = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]]) / (2 * np.sin(theta))
        rotating = r * theta
        ret = [T[0,3], T[1,3], T[2,3], rotating[0], rotating[1], rotating[2]]
        return ret

    def DH_FK(self, theta: list, precision=6):
        '''
        正向运动学，6关节角度 -> T矩阵
        :param theta:       6关节角度值列表
        :param precision:   返回值保留精度，默认为6位小数
        :return:            list: pose  -> [x, y, z, rx, ry, rz]
                            list: T     -> 6关节的T矩阵
        '''
        # 用来接收角度所转的弧度值
        radian = [0, 0, 0, 0, 0, 0]

        # 角度转弧度
        for i in range(len(theta)):
            radian[i] = self.angle_to_radian(theta[i])

        # 求六个joint的T矩阵
        t1 = self.DH_T(radian[0], self.DH_a1, self.DH_d1, self.DH_alpha1)
        t2 = self.DH_T(radian[1], self.DH_a2, self.DH_d2, self.DH_alpha2)
        t3 = self.DH_T(radian[2], self.DH_a3, self.DH_d3, self.DH_alpha3)
        t4 = self.DH_T(radian[3], self.DH_a4, self.DH_d4, self.DH_alpha4)
        t5 = self.DH_T(radian[4], self.DH_a5, self.DH_d5, self.DH_alpha5)
        t6 = self.DH_T(radian[5], self.DH_a6, self.DH_d6, self.DH_alpha6)

        # 拼接6关节T矩阵
        T = np.dot(np.dot(np.dot(np.dot(np.dot(t1, t2), t3), t4), t5), t6)

        # 计算旋转矢量，用罗德里格斯参数（Rodrigues' parameters）的概念来将旋转矩阵转换为旋转矢量
        rotation_vector = logm(T[:3, :3])

        # 填充结果
        pose = [round((T[0, 3]), precision), round(T[1, 3], precision), round(T[2, 3], precision),
                round(np.real(rotation_vector[2, 1]), precision),       # 提取复数实部，保留指定位数的小数
                round(np.real(rotation_vector[0, 2]), precision),
                round(np.real(rotation_vector[1, 0]), precision),]

        return pose, T

    def DH_IK(self, T, angle=False, precision=6):
        '''
        逆向运动学，T矩阵 -> 6关节角度
        :param p:           机械臂当前位姿[x, y, z, rx, ry, rz]
        :param angle:       True -> 返回1个矩阵，解为弧度值
                            True -> 返回2个矩阵，第一个为弧度值，第二个为角度值
        :param precision:   返回值保留精度，默认为6位小数
        :return:            list: 1或2个矩阵，与angle参数有关
        '''

        # 创建结果的空矩阵
        ret = np.zeros((8, 6))

        # 解算theta1，2个解
        m = self.DH_d6 * T[1][2] - T[1][3]
        n = self.DH_d6 * T[0][2] - T[0][3]
        theta1_1 = np.arctan2(m, n) - np.arctan2(self.DH_d4, np.sqrt(m ** 2 + n ** 2 - self.DH_d4 ** 2))
        theta1_2 = np.arctan2(m, n) - np.arctan2(self.DH_d4, -np.sqrt(m ** 2 + n ** 2 - self.DH_d4 ** 2))
        ret[0:4][... ,0] = theta1_1
        ret[4:][..., 0] = theta1_2

        # 解算theta5，4个解
        theta5_1 = np.arccos(T[0][2] * np.sin(theta1_1) - T[1][2] * np.cos(theta1_1))
        theta5_2 = -np.arccos(T[0][2] * np.sin(theta1_1) - T[1][2] * np.cos(theta1_1))
        theta5_3 = np.arccos(T[0][2] * np.sin(theta1_2) - T[1][2] * np.cos(theta1_2))
        theta5_4 = -np.arccos(T[0][2] * np.sin(theta1_2) - T[1][2] * np.cos(theta1_2))
        ret[0:2][..., 4] = theta5_1
        ret[2:4][..., 4] = theta5_2
        ret[4:6][..., 4] = theta5_3
        ret[6:8][..., 4] = theta5_4

        # 解算theta6，4个解
        m1 = T[0][0] * np.sin(theta1_1) - T[1][0] * np.cos(theta1_1)
        n1 = T[0][1] * np.sin(theta1_1) - T[1][1] * np.cos(theta1_1)
        m2 = T[0][0] * np.sin(theta1_2) - T[1][0] * np.cos(theta1_2)
        n2 = T[0][1] * np.sin(theta1_2) - T[1][1] * np.cos(theta1_2)

        theta6_1 = np.arctan2(-n1 / np.sin(theta5_1), m1 / np.sin(theta5_1))
        theta6_2 = np.arctan2(-n1 / np.sin(theta5_2), m1 / np.sin(theta5_2))
        theta6_3 = np.arctan2(-n2 / np.sin(theta5_3), m2 / np.sin(theta5_3))
        theta6_4 = np.arctan2(-n2 / np.sin(theta5_4), m2 / np.sin(theta5_4))

        ret[0:2][..., 5] = theta6_1
        ret[2:4][..., 5] = theta6_2
        ret[4:6][..., 5] = theta6_3
        ret[6:8][..., 5] = theta6_4

        # 解算theta3，8个解
        m3 = self.DH_d5 * (np.sin(theta6_1) * (T[0][0] * np.cos(theta1_1) + T[1][0] * np.sin(theta1_1)) + np.cos(theta6_1) * (T[0][1] * np.cos(theta1_1) + T[1][1] * np.sin(theta1_1))) - self.DH_d6 * (T[0][2] * np.cos(theta1_1) + T[1][2] * np.sin(theta1_1)) + T[0][3] * np.cos(theta1_1) + T[1][3] * np.sin(theta1_1)
        n3 = T[2][3] - self.DH_d1 - T[2][2] * self.DH_d6 + self.DH_d5 * (T[2][1] * np.cos(theta6_1) + T[2][0] * np.sin(theta6_1))
        m4 = self.DH_d5 * (np.sin(theta6_2) * (T[0][0] * np.cos(theta1_1) + T[1][0] * np.sin(theta1_1)) + np.cos(theta6_2) * (T[0][1] * np.cos(theta1_1) + T[1][1] * np.sin(theta1_1))) - self.DH_d6 * (T[0][2] * np.cos(theta1_1) + T[1][2] * np.sin(theta1_1)) + T[0][3] * np.cos(theta1_1) + T[1][3] * np.sin(theta1_1)
        n4 = T[2][3] - self.DH_d1 - T[2][2] * self.DH_d6 + self.DH_d5 * (T[2][1] * np.cos(theta6_2) + T[2][0] * np.sin(theta6_2))
        m5 = self.DH_d5 * (np.sin(theta6_3) * (T[0][0] * np.cos(theta1_2) + T[1][0] * np.sin(theta1_2)) + np.cos(theta6_3) * (T[0][1] * np.cos(theta1_2) + T[1][1] * np.sin(theta1_2))) - self.DH_d6 * (T[0][2] * np.cos(theta1_2) + T[1][2] * np.sin(theta1_2)) + T[0][3] * np.cos(theta1_2) + T[1][3] * np.sin(theta1_2)
        n5 = T[2][3] - self.DH_d1 - T[2][2] * self.DH_d6 + self.DH_d5 * (T[2][1] * np.cos(theta6_3) + T[2][0] * np.sin(theta6_3))
        m6 = self.DH_d5 * (np.sin(theta6_4) * (T[0][0] * np.cos(theta1_2) + T[1][0] * np.sin(theta1_2)) + np.cos(theta6_4) * (T[0][1] * np.cos(theta1_2) + T[1][1] * np.sin(theta1_2))) - self.DH_d6 * (T[0][2] * np.cos(theta1_2) + T[1][2] * np.sin(theta1_2)) + T[0][3] * np.cos(theta1_2) + T[1][3] * np.sin(theta1_2)
        n6 = T[2][3] - self.DH_d1 - T[2][2] * self.DH_d6 + self.DH_d5 * (T[2][1] * np.cos(theta6_4) + T[2][0] * np.sin(theta6_4))

        theta3_1 = np.arccos((m3 ** 2 + n3 ** 2 - self.DH_a2 ** 2 - self.DH_a3 ** 2) / (2 * self.DH_a2 * self.DH_a3))
        theta3_2 = -np.arccos((m3 ** 2 + n3 ** 2 - self.DH_a2 ** 2 - self.DH_a3 ** 2) / (2 * self.DH_a2 * self.DH_a3))
        theta3_3 = np.arccos((m4 ** 2 + n4 ** 2 - self.DH_a2 ** 2 - self.DH_a3 ** 2) / (2 * self.DH_a2 * self.DH_a3))
        theta3_4 = -np.arccos((m4 ** 2 + n4 ** 2 - self.DH_a2 ** 2 - self.DH_a3 ** 2) / (2 * self.DH_a2 * self.DH_a3))
        theta3_5 = np.arccos((m5 ** 2 + n5 ** 2 - self.DH_a2 ** 2 - self.DH_a3 ** 2) / (2 * self.DH_a2 * self.DH_a3))
        theta3_6 = -np.arccos((m5 ** 2 + n5 ** 2 - self.DH_a2 ** 2 - self.DH_a3 ** 2) / (2 * self.DH_a2 * self.DH_a3))
        theta3_7 = np.arccos((m6 ** 2 + n6 ** 2 - self.DH_a2 ** 2 - self.DH_a3 ** 2) / (2 * self.DH_a2 * self.DH_a3))
        theta3_8 = -np.arccos((m6 ** 2 + n6 ** 2 - self.DH_a2 ** 2 - self.DH_a3 ** 2) / (2 * self.DH_a2 * self.DH_a3))

        ret[0][2] = theta3_1
        ret[1][2] = theta3_2
        ret[2][2] = theta3_3
        ret[3][2] = theta3_4
        ret[4][2] = theta3_5
        ret[5][2] = theta3_6
        ret[6][2] = theta3_7
        ret[7][2] = theta3_8

        # 解算theta2，8个解
        s1 = ((self.DH_a3 * np.cos(theta3_1) + self.DH_a2) * n3 - self.DH_a3 * np.sin(theta3_1) * m3) / (self.DH_a2 ** 2 + self.DH_a3 ** 2 + 2 * self.DH_a2 * self.DH_a3 * np.cos(theta3_1))
        c1 = (m3 + self.DH_a3 * np.sin(theta3_1) * s1) / (self.DH_a3 * np.cos(theta3_1) + self.DH_a2)
        s2 = ((self.DH_a3 * np.cos(theta3_2) + self.DH_a2) * n3 - self.DH_a3 * np.sin(theta3_2) * m3) / (self.DH_a2 ** 2 + self.DH_a3 ** 2 + 2 * self.DH_a2 * self.DH_a3 * np.cos(theta3_2))
        c2 = (m3 + self.DH_a3 * np.sin(theta3_2) * s2) / (self.DH_a3 * np.cos(theta3_2) + self.DH_a2)
        s3 = ((self.DH_a3 * np.cos(theta3_3) + self.DH_a2) * n4 - self.DH_a3 * np.sin(theta3_3) * m4) / (self.DH_a2 ** 2 + self.DH_a3 ** 2 + 2 * self.DH_a2 * self.DH_a3 * np.cos(theta3_3))
        c3 = (m4 + self.DH_a3 * np.sin(theta3_3) * s3) / (self.DH_a3 * np.cos(theta3_3) + self.DH_a2)
        s4 = ((self.DH_a3 * np.cos(theta3_4) + self.DH_a2) * n4 - self.DH_a3 * np.sin(theta3_4) * m4) / (self.DH_a2 ** 2 + self.DH_a3 ** 2 + 2 * self.DH_a2 * self.DH_a3 * np.cos(theta3_4))
        c4 = (m4 + self.DH_a3 * np.sin(theta3_4) * s4) / (self.DH_a3 * np.cos(theta3_4) + self.DH_a2)
        s5 = ((self.DH_a3 * np.cos(theta3_5) + self.DH_a2) * n5 - self.DH_a3 * np.sin(theta3_5) * m5) / (self.DH_a2 ** 2 + self.DH_a3 ** 2 + 2 * self.DH_a2 * self.DH_a3 * np.cos(theta3_5))
        c5 = (m5 + self.DH_a3 * np.sin(theta3_5) * s5) / (self.DH_a3 * np.cos(theta3_5) + self.DH_a2)
        s6 = ((self.DH_a3 * np.cos(theta3_6) + self.DH_a2) * n5 - self.DH_a3 * np.sin(theta3_6) * m5) / (self.DH_a2 ** 2 + self.DH_a3 ** 2 + 2 * self.DH_a2 * self.DH_a3 * np.cos(theta3_6))
        c6 = (m5 + self.DH_a3 * np.sin(theta3_6) * s6) / (self.DH_a3 * np.cos(theta3_6) + self.DH_a2)
        s7 = ((self.DH_a3 * np.cos(theta3_7) + self.DH_a2) * n6 - self.DH_a3 * np.sin(theta3_7) * m6) / (self.DH_a2 ** 2 + self.DH_a3 ** 2 + 2 * self.DH_a2 * self.DH_a3 * np.cos(theta3_7))
        c7 = (m6 + self.DH_a3 * np.sin(theta3_7) * s7) / (self.DH_a3 * np.cos(theta3_7) + self.DH_a2)
        s8 = ((self.DH_a3 * np.cos(theta3_8) + self.DH_a2) * n6 - self.DH_a3 * np.sin(theta3_8) * m6) / (self.DH_a2 ** 2 + self.DH_a3 ** 2 + 2 * self.DH_a2 * self.DH_a3 * np.cos(theta3_8))
        c8 = (m6 + self.DH_a3 * np.sin(theta3_8) * s8) / (self.DH_a3 * np.cos(theta3_8) + self.DH_a2)

        theta2_1 = np.arctan2(s1, c1)
        theta2_2 = np.arctan2(s2, c2)
        theta2_3 = np.arctan2(s3, c3)
        theta2_4 = np.arctan2(s4, c4)
        theta2_5 = np.arctan2(s5, c5)
        theta2_6 = np.arctan2(s6, c6)
        theta2_7 = np.arctan2(s7, c7)
        theta2_8 = np.arctan2(s8, c8)

        ret[0][1] = theta2_1
        ret[1][1] = theta2_2
        ret[2][1] = theta2_3
        ret[3][1] = theta2_4
        ret[4][1] = theta2_5
        ret[5][1] = theta2_6
        ret[6][1] = theta2_7
        ret[7][1] = theta2_8

        # 解算theta4，8个解
        theta4_1 = np.arctan2(-np.sin(ret[0][5]) * (T[0][0] * np.cos(ret[0][0]) + T[1][0] * np.sin(ret[0][0])) - np.cos(ret[0][5]) * (T[0][1] * np.cos(ret[0][0]) + T[1][1] * np.sin(ret[0][0])), T[2][1] * np.cos(ret[0][5]) + T[2][0] * np.sin(ret[0][5])) - ret[0][1] - ret[0][2]
        theta4_2 = np.arctan2(-np.sin(ret[1][5]) * (T[0][0] * np.cos(ret[1][0]) + T[1][0] * np.sin(ret[1][0])) - np.cos(ret[1][5]) * (T[0][1] * np.cos(ret[1][0]) + T[1][1] * np.sin(ret[1][0])), T[2][1] * np.cos(ret[1][5]) + T[2][0] * np.sin(ret[1][5])) - ret[1][1] - ret[1][2]
        theta4_3 = np.arctan2(-np.sin(ret[2][5]) * (T[0][0] * np.cos(ret[2][0]) + T[1][0] * np.sin(ret[2][0])) - np.cos(ret[2][5]) * (T[0][1] * np.cos(ret[2][0]) + T[1][1] * np.sin(ret[2][0])), T[2][1] * np.cos(ret[2][5]) + T[2][0] * np.sin(ret[2][5])) - ret[2][1] - ret[2][2]
        theta4_4 = np.arctan2(-np.sin(ret[3][5]) * (T[0][0] * np.cos(ret[3][0]) + T[1][0] * np.sin(ret[3][0])) - np.cos(ret[3][5]) * (T[0][1] * np.cos(ret[3][0]) + T[1][1] * np.sin(ret[3][0])), T[2][1] * np.cos(ret[3][5]) + T[2][0] * np.sin(ret[3][5])) - ret[3][1] - ret[3][2]
        theta4_5 = np.arctan2(-np.sin(ret[4][5]) * (T[0][0] * np.cos(ret[4][0]) + T[1][0] * np.sin(ret[4][0])) - np.cos(ret[4][5]) * (T[0][1] * np.cos(ret[4][0]) + T[1][1] * np.sin(ret[4][0])), T[2][1] * np.cos(ret[4][5]) + T[2][0] * np.sin(ret[4][5])) - ret[4][1] - ret[4][2]
        theta4_6 = np.arctan2(-np.sin(ret[5][5]) * (T[0][0] * np.cos(ret[5][0]) + T[1][0] * np.sin(ret[5][0])) - np.cos(ret[5][5]) * (T[0][1] * np.cos(ret[5][0]) + T[1][1] * np.sin(ret[5][0])), T[2][1] * np.cos(ret[5][5]) + T[2][0] * np.sin(ret[5][5])) - ret[5][1] - ret[5][2]
        theta4_7 = np.arctan2(-np.sin(ret[6][5]) * (T[0][0] * np.cos(ret[6][0]) + T[1][0] * np.sin(ret[6][0])) - np.cos(ret[6][5]) * (T[0][1] * np.cos(ret[6][0]) + T[1][1] * np.sin(ret[6][0])), T[2][1] * np.cos(ret[6][5]) + T[2][0] * np.sin(ret[6][5])) - ret[6][1] - ret[6][2]
        theta4_8 = np.arctan2(-np.sin(ret[7][5]) * (T[0][0] * np.cos(ret[7][0]) + T[1][0] * np.sin(ret[7][0])) - np.cos(ret[7][5]) * (T[0][1] * np.cos(ret[7][0]) + T[1][1] * np.sin(ret[7][0])), T[2][1] * np.cos(ret[7][5]) + T[2][0] * np.sin(ret[7][5])) - ret[7][1] - ret[7][2]

        ret[0][3] = theta4_1
        ret[1][3] = theta4_2
        ret[2][3] = theta4_3
        ret[3][3] = theta4_4
        ret[4][3] = theta4_5
        ret[5][3] = theta4_6
        ret[6][3] = theta4_7
        ret[7][3] = theta4_8
        if angle:
            return np.round(ret, decimals=precision), np.round(ret * 180 / np.pi, decimals=precision)
        else:
            return np.round(ret, decimals=precision), None


