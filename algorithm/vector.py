# -*- coding: utf-8 -*-
"""
@Time ： 2024/4/26 17:07
@Auth ： Ethan
@File ：vector.py
@IDE ：PyCharm
"""

import trimesh
import numpy as np

class Vector:
    def generate_point(self, path, pos):
        '''
        读取点云文件，根据给定点云的位置，计算离该点最近的四个点并返回
        :param path:    点云文件路径
        :param pos:     所选中的点
        :return:        所选中的点 离该点最近的四个点
        '''
        D = trimesh.load_mesh(path)                                     # 读取点云文件
        point_cloud = D.vertices                                        # 获取点云文件数据
        given_point = np.array(point_cloud[pos])                        # 给定点的坐标，目前给的是数据中的第一个
        distances = np.linalg.norm(point_cloud - given_point, axis=1)   # 计算给定点与每个点的距离
        sorted_indices = np.argsort(distances)                          # 对距离进行排序，返回排序后的索引
        nearest_points_indices = sorted_indices[:4]                     # 选择距离最近的四个点
        nearest_points = point_cloud[nearest_points_indices]            # 获取最近的四个点的坐标
        return given_point, nearest_points

    def cal_vector(self, p1, p2, p3):
        '''
        根据空间中三个坐标点计算垂直于该平面的法向量
        :param p1: 第一个点
        :param p2: 第二个点
        :param p3: 第三个点
        :return:
        '''
        p1 = np.array(p1)                   # 定义四个空间坐标点
        p2 = np.array(p2)
        p3 = np.array(p3)
        l1 = p2 - p1                        # 使用三个点构建两个向量
        l2 = p3 - p1
        normal_vector = np.cross(l1, l2)    # 计算叉乘得到法向量
        return normal_vector

    def cal_wrist_position(self, T, v):
        '''
        垂直入射算法
        :param T:   正运动学解出的T矩阵
        :param v:   垂直的法向量
        :return:    返回更新后的T矩阵
        '''
        R = T[:3, :3]               # 旋转矩阵

        # 计算旋转轴和角度
        rotation_axis = np.cross(R[:, 2], v)
        rotation_axis /= np.linalg.norm(rotation_axis)
        rotation_angle = np.arccos(np.dot(R[:, 2], v) / (np.linalg.norm(R[:, 2]) * np.linalg.norm(v)))

        # 使用罗德里格斯旋转公式计算旋转矩阵
        K = np.array([
            [0, -rotation_axis[2], rotation_axis[1]],
            [rotation_axis[2], 0, -rotation_axis[0]],
            [-rotation_axis[1], rotation_axis[0], 0]
        ])
        rotation_matrix = np.eye(3) + np.sin(rotation_angle) * K + (1 - np.cos(rotation_angle)) * np.dot(K, K)

        # 得到最终的旋转矩阵
        final_rotation_matrix = np.dot(rotation_matrix, R)

        T[:3, :3] = final_rotation_matrix
        return T

    def generate_vector_line(self, normal_vector, point_on_line, num):
        '''
        根据法向量信息，生成一条直线
        :param normal_vector:   法向量信息
        :param point_on_line:   指定的一个基点，生成的直线将以其为中点
        :param num:             直线上点的数量
        :return:
        '''
        points = []
        direction_vector = normal_vector / np.linalg.norm(normal_vector)    # 将法向量转换为单位向量
        for i in range(-num // 2, num // 2, 1):
            points.append(point_on_line + i * direction_vector)             # 选择第二个点，沿着法向量方向移动一定距离
        points = np.array(points)
        return points

