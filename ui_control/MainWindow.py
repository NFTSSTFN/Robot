# -*- coding: utf-8 -*-
"""
@Time ： 2024/4/25 17:26
@Auth ： Ethan
@File ：MainWindow.py
@IDE ：PyCharm
"""

from PySide2.QtWidgets import QMainWindow
from pyvistaqt import QtInteractor
import pyvista as pv
import numpy as np
import os, sys

from ui.ui_MainWindow import Ui_MainWindow
import models.mapping as mp






class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.init_constant()
        self.init_variable()
        self.init_ui_style()
        self.load_UR5_models()

    def init_constant(self):
        ''' 初始化系统所需的常量 '''
        self.BASE_DIR = os.path.dirname(sys.argv[0])    # 获取项目工作的根目录
        self.plotter = QtInteractor(self)               # pyvista的窗体，负责渲染机械臂、点云模型
        self.robot_joint_mesh = {}                      # 储存机械臂各个关节的模型

    def init_variable(self):
        ''' 初始化系统所需的变量 '''

        # 定义机械臂6个关节的旋转轴，是以向量形式表示的，最后一个值没用，只是为了正常参与矩阵运算而加的
        self.robot_joint_vector = {
            1: np.matrix([[0], [0], [1], [1]]),
            2: np.matrix([[0], [0], [1], [1]]),
            3: np.matrix([[0], [0], [1], [1]]),
            4: np.matrix([[0], [0], [1], [1]]),
            5: np.matrix([[0], [0], [1], [1]]),
            6: np.matrix([[0], [0], [1], [1]]),
        }
        self.joint_angles = np.array([0., 0., 0., 0., 0., 0.])    # 初始化机械臂各个轴的角度


    def init_ui_style(self):
        ''' 初始化主页面UI样式 '''
        self.plotter.set_background('black')        # 设置窗体为黑色
        self.layout_3D.addWidget(self.plotter)      # 将窗体嵌入主页面的layout当中
        self.plotter.show_grid()                    # 显示三维空间中网格形式的坐标轴
        self.plotter.show_axes()                    # 显示三维空间中坐标系

        # self.plotter.enable_point_picking(callback=self.on_point_pick, show_message=False)  # 开启窗体点选功能
        # self.plotter.enable_cell_picking()          # 矩形选择
        # self.plotter.enable_path_picking()          # 连线选择
        floor = pv.Plane(center=(0, 0, 0), direction=(0, 0, 1), i_size=2000, j_size=2000)   # 创建一个平面网格
        self.plotter.add_mesh(floor)                # 添加平面至三维窗体


    def load_UR5_models(self):
        '''
        加载UR5模型，
        :return:
        '''
        index = 0                                                       # 用来把机械臂6个关节给分组
        mesh_color = (0, 0, 0)                                          # 预定义零部件颜色，之后用于上色
        offset_x, offset_y = 0, 0                                       # 模型整体的偏移量，通过偏移让模型整体位于三维坐标系正中心

        # 遍历各个关节的模型组
        for joint in mp.robot_mesh_joint:
            group = pv.MultiBlock()                                     # 为每个关节都建立一个组
            # 根据关节找出关节下面所有的零件
            for part in mp.robot_mesh_joint[joint]:
                path = self.BASE_DIR + '/models/UR5/' + part            # 关节中各个零件的路径

                # 给关节中的各个零部件上色
                for color in mp.robot_mesh_color:
                    if part in mp.robot_mesh_color[color]:
                        mesh_color = color
                        break

                mesh = pv.read(path)                                    # 读取模型文件
                mesh.rotate_y(90, inplace=True)                         # 因为模型是平躺的，将所有关节旋转90°立起来
                mesh.rotate_z(180, inplace=True)                        # 旋转各个关节，让其与UR5机械臂初始姿态对应
                mesh.translate([0, 0, 1065], inplace=True)              # 将模型三轴位置都移动至原点



                # 获取基座正中心位置，以此为基准，通过偏移让模型整体都位于三维坐标系的中心位置
                if joint == 'base':
                    center = mesh.center
                    offset_x = -center[0]
                    offset_y = -center[1]
                mesh.translate([offset_x, offset_y, 0], inplace=True)   # 通过偏移量让各个部件处于三维坐标系正中心
                self.plotter.add_mesh(mesh, color=mesh_color, smooth_shading=True)      # 添加模型文件，给定颜色，平滑渲染

            self.robot_joint_mesh[index] = group                        # 添加关节组至字典，方便后续控制其旋转
            index += 1