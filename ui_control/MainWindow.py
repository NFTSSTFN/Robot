# -*- coding: utf-8 -*-
"""
@Time ： 2024/4/25 17:26
@Auth ： Ethan
@File ：MainWindow.py
@IDE ：PyCharm
"""
from PySide2.QtWidgets import QMainWindow, QButtonGroup, QWidget
from PySide2.QtCore import Qt, QPoint, QTimer
from PySide2.QtGui import QIcon
from pyvistaqt import QtInteractor
import pyvista as pv
import numpy as np
import os, sys, json
import multiprocessing
import time

from ui.ui_MainWindow import Ui_MainWindow
from sys_threading.control_robot import ControlRobot
from ui_control.MessageBox import MassageBox
from hardware.UR5 import UR5, Test
import models.mapping as mp


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # 初始化所需函数
        self.init_constant()                                        # 初始化系统常量
        self.init_variable()                                        # 初始化系统变量
        self.init_ui_style()                                        # 初始化界面风格
        self.load_UR5_models()                                      # 读取UR5模型
        self.CR = ControlRobot(self)                                # 初始化机械臂模型控制类
        self.CR.joint_rotation(2, self.joint_angles[1])             # 初始化UR5模型位姿
        self.update_sim_info()                                      # 根据初始化后的UR5位姿，刷新界面显示的值
        self.UR5 = UR5(self.config, self.data30003, self.UR5_event, self.UR5_process_control)  # UR5实机操控函数
        self.MSG = MassageBox()                                     # 重写的MessageBox窗体

        # 绑定系统界面最小化、最大化/正常化、关闭的按钮信号槽
        self.btn_min.clicked.connect(self.window_minimize)          # 系统最小化至任务栏
        self.btn_max.clicked.connect(self.window_max_or_nor)        # 系统最大化、正常化
        self.btn_close.clicked.connect(self.window_close)           # 系统关闭

        # 绑定菜单栏按钮信号槽
        self.btn_1.clicked.connect(lambda: self.test1(1, 30))       # 菜单栏按钮
        self.btn_2.clicked.connect(lambda: self.test1(2, 30))
        self.btn_3.clicked.connect(lambda: self.test1(3, 30))
        self.btn_4.clicked.connect(lambda: self.test1(4, 30))
        self.btn_5.clicked.connect(lambda: self.test1(5, 30))
        self.btn_6.clicked.connect(lambda: self.test1(6, 30))

        # 绑定仿真控制中Slider滑块信号
        self.sld_joint1.sliderReleased.connect(lambda: self.control_robot_angle(1, int(self.sld_joint1.value()), 'sld'))
        self.sld_joint2.sliderReleased.connect(lambda: self.control_robot_angle(2, int(self.sld_joint2.value()), 'sld'))
        self.sld_joint3.sliderReleased.connect(lambda: self.control_robot_angle(3, int(self.sld_joint3.value()), 'sld'))
        self.sld_joint4.sliderReleased.connect(lambda: self.control_robot_angle(4, int(self.sld_joint4.value()), 'sld'))
        self.sld_joint5.sliderReleased.connect(lambda: self.control_robot_angle(5, int(self.sld_joint5.value()), 'sld'))
        self.sld_joint6.sliderReleased.connect(lambda: self.control_robot_angle(6, int(self.sld_joint6.value()), 'sld'))

        # 绑定仿真控制中QLineEdit机械臂角度控制信号
        self.le_joint1.editingFinished.connect(lambda: self.control_robot_angle(1, float(self.le_joint1.text()), 'le'))
        self.le_joint2.editingFinished.connect(lambda: self.control_robot_angle(2, float(self.le_joint2.text()), 'le'))
        self.le_joint3.editingFinished.connect(lambda: self.control_robot_angle(3, float(self.le_joint3.text()), 'le'))
        self.le_joint4.editingFinished.connect(lambda: self.control_robot_angle(4, float(self.le_joint4.text()), 'le'))
        self.le_joint5.editingFinished.connect(lambda: self.control_robot_angle(5, float(self.le_joint5.text()), 'le'))
        self.le_joint6.editingFinished.connect(lambda: self.control_robot_angle(6, float(self.le_joint6.text()), 'le'))

        # 绑定实机控制按钮
        self.rbtn_con.toggled.connect(self.connect_UR5)             # 连接UR5机械臂

    def test1(self, joint, angle):
        self.CR.joint_rotation(joint, angle)

    def control_robot_angle(self, joint: int, angle: float, trigger: str):
        '''
        接收Slider控件传来的变更信号，控制机械臂模型转动
        :param joint:       需要转动的关节
        :param angle:       需要转动的角度，需要先与保留精度做运算
        :param trigger:     函数触发方式
        :return:            None
        '''
        if trigger == 'sld':
            angle = angle * self.sld_pre                # 修正角度的精度
        self.CR.joint_rotation(joint, angle)            # 转动机械臂模型
        self.update_sim_info()                          # 更新机械臂角度、弧度、TCP位姿信息

    def init_constant(self):
        '''
        初始化系统所需常量
        :return:    None
        '''
        self.BASE_DIR = os.path.dirname(sys.argv[0])                    # 获取项目工作的根目录
        self.plotter = QtInteractor(self)                               # pyvista的窗体，负责渲染机械臂、点云模型
        self.robot_joint_mesh = {}                                      # 储存机械臂各个关节的模型

        # 读取系统默认配置文件，储存在self.config中
        with open('static/config.json', 'r', encoding='utf8') as json_file:
            self.config = json.load(json_file)

        # 因为QSlider只能设置整数，此处需要根据angle保留的小数位数来确定QSlider的大小
        self.sld_pre = 10 ** -self.config['jt_angle_pre']

        # 初始化界面刷新频率计时器，与UR5连接时，刷新界面数据、机械臂模型
        self.timer = QTimer()                                           # 初始化Qtimer定时器，用来刷新UR5实机数据
        self.timer.setInterval(self.config["refresh_rate"])             # 设置刷新频率，单位ms
        self.timer.timeout.connect(self.UR5_updata)                     # 刷新机械臂状态、显示数据

    def init_variable(self):
        '''
        初始化系统所需变量
        :return:    None
        '''
        # UR5机械臂连接
        self.UR5_process_start_status = False                           # 判断UR5数据接收进程是否被开启
        self.UR5_event = multiprocessing.Event()                        # 事件决定进程状态（正常、休眠）

        os.environ["QT_API"] = "PySide2"                                # 设置Qt的绑定库为PySide2,不然会有报错提示
        # 定义数据接收进程共享字典
        manager = multiprocessing.Manager()                             # 进程管理器
        self.data30003 = manager.dict()                                 # 创建共享字典对象

        # 定义数据接收进程控制状态
        manager = multiprocessing.Manager()                             # 进程管理器
        self.UR5_process_control = manager.dict()                       # 创建共享字典对象
        self.UR5_process_control['Process_flag'] = False                # UR5进程开关，控制进程状态

        # 点击窗口边上，拉伸/缩小窗口所用变量，点击标题栏，移动整个窗体
        self._move_drag = False                                         # 标题栏
        self._corner_drag = False                                       # 右下角
        self._bottom_drag = False                                       # 底部
        self._right_drag = False                                        # 右边

        # 定义机械臂6个关节的旋转轴，是以向量形式表示的，最后一个值没用，只是为了正常参与矩阵运算而加的
        self.robot_joint_vector = {
            1: np.matrix([[0], [0], [1], [1]]),
            2: np.matrix([[0], [0], [1], [1]]),
            3: np.matrix([[0], [0], [1], [1]]),
            4: np.matrix([[0], [0], [1], [1]]),
            5: np.matrix([[0], [0], [1], [1]]),
            6: np.matrix([[0], [0], [1], [1]]),
        }
        self.joint_angles = np.array([0., -90., 0., -90., 0., 0.])      # 初始化机械臂(模型)各个关节的角度，里面储存角度值
        self.joint_radians = np.array([0., 0., 0., 0., 0., 0.])         # 初始化机械臂(模型)各个关节的弧度，里面储存弧度值
        self.joint_angles_real = np.array([0., 0., 0., 0., 0., 0.])     # 初始化机械臂(实机)各个关节的角度，里面储存角度值
        self.joint_radians_real = np.array([0., 0., 0., 0., 0., 0.])    # 初始化机械臂(实机)各个关节的弧度，里面储存弧度值
        self.TCP_pose = np.array([0., 0., 0., 0., 0., 0.])              # 初始化机械臂TCP位姿

    def init_ui_style(self):
        '''
        初始化主页面UI样式
        :return:    None
        '''
        self.plotter.set_background('black')            # 设置三维窗体背景为黑色
        self.layout_3D.addWidget(self.plotter)          # 将窗体嵌入主页面的layout当中
        self.plotter.show_grid()                        # 显示三维空间中网格形式的坐标轴
        self.plotter.show_axes()                        # 显示三维空间中坐标系

        # self.plotter.enable_point_picking(callback=self.on_point_pick, show_message=False)  # 开启窗体点选功能
        # self.plotter.enable_cell_picking()          # 矩形选择
        # self.plotter.enable_path_picking()          # 连线选择
        floor = pv.Plane(center=(0, 0, 0), direction=(0, 0, 1), i_size=2000, j_size=2000)   # 创建一个平面网格
        self.plotter.add_mesh(floor)                    # 添加平面至三维窗体

        # 设置6个关节Slider的显示范围，每个关节的精度
        self.sld_joint1.setRange(self.config['jt_sld_limit'][0][0] / self.sld_pre,
                                 self.config['jt_sld_limit'][0][1] / self.sld_pre)
        self.sld_joint2.setRange(self.config['jt_sld_limit'][1][0] / self.sld_pre,
                                 self.config['jt_sld_limit'][1][1] / self.sld_pre)
        self.sld_joint3.setRange(self.config['jt_sld_limit'][2][0] / self.sld_pre,
                                 self.config['jt_sld_limit'][2][1] / self.sld_pre)
        self.sld_joint4.setRange(self.config['jt_sld_limit'][3][0] / self.sld_pre,
                                 self.config['jt_sld_limit'][3][1] / self.sld_pre)
        self.sld_joint5.setRange(self.config['jt_sld_limit'][4][0] / self.sld_pre,
                                 self.config['jt_sld_limit'][4][1] / self.sld_pre)
        self.sld_joint6.setRange(self.config['jt_sld_limit'][5][0] / self.sld_pre,
                                 self.config['jt_sld_limit'][5][1] / self.sld_pre)

        # 设置所有文本框显示居中
        self.le_x.setAlignment(Qt.AlignCenter)
        self.le_y.setAlignment(Qt.AlignCenter)
        self.le_z.setAlignment(Qt.AlignCenter)
        self.le_rx.setAlignment(Qt.AlignCenter)
        self.le_ry.setAlignment(Qt.AlignCenter)
        self.le_rz.setAlignment(Qt.AlignCenter)
        self.le_joint1.setAlignment(Qt.AlignCenter)
        self.le_joint2.setAlignment(Qt.AlignCenter)
        self.le_joint3.setAlignment(Qt.AlignCenter)
        self.le_joint4.setAlignment(Qt.AlignCenter)
        self.le_joint5.setAlignment(Qt.AlignCenter)
        self.le_joint6.setAlignment(Qt.AlignCenter)
        self.le_radian1.setAlignment(Qt.AlignCenter)
        self.le_radian2.setAlignment(Qt.AlignCenter)
        self.le_radian3.setAlignment(Qt.AlignCenter)
        self.le_radian4.setAlignment(Qt.AlignCenter)
        self.le_radian5.setAlignment(Qt.AlignCenter)
        self.le_radian6.setAlignment(Qt.AlignCenter)
        self.le_angle1.setAlignment(Qt.AlignCenter)
        self.le_angle2.setAlignment(Qt.AlignCenter)
        self.le_angle3.setAlignment(Qt.AlignCenter)
        self.le_angle4.setAlignment(Qt.AlignCenter)
        self.le_angle5.setAlignment(Qt.AlignCenter)
        self.le_angle6.setAlignment(Qt.AlignCenter)
        self.le_runtime.setAlignment(Qt.AlignCenter)                    # 运行时间按钮

        # 设置文本框最大最小宽度
        self.le_x.setFixedWidth(85)
        self.le_y.setFixedWidth(85)
        self.le_z.setFixedWidth(85)
        self.le_rx.setFixedWidth(85)
        self.le_ry.setFixedWidth(85)
        self.le_rz.setFixedWidth(85)
        self.le_radian1.setFixedWidth(85)
        self.le_radian2.setFixedWidth(85)
        self.le_radian3.setFixedWidth(85)
        self.le_radian4.setFixedWidth(85)
        self.le_radian5.setFixedWidth(85)
        self.le_radian6.setFixedWidth(85)
        self.le_angle1.setFixedWidth(85)
        self.le_angle2.setFixedWidth(85)
        self.le_angle3.setFixedWidth(85)
        self.le_angle4.setFixedWidth(85)
        self.le_angle5.setFixedWidth(85)
        self.le_angle6.setFixedWidth(85)

        # 将主页面右侧三栏文本框数据设置为只显示
        self.le_x.setReadOnly(True)
        self.le_y.setReadOnly(True)
        self.le_z.setReadOnly(True)
        self.le_rx.setReadOnly(True)
        self.le_ry.setReadOnly(True)
        self.le_rz.setReadOnly(True)
        self.le_radian1.setReadOnly(True)
        self.le_radian2.setReadOnly(True)
        self.le_radian3.setReadOnly(True)
        self.le_radian4.setReadOnly(True)
        self.le_radian5.setReadOnly(True)
        self.le_radian6.setReadOnly(True)
        self.le_angle1.setReadOnly(True)
        self.le_angle2.setReadOnly(True)
        self.le_angle3.setReadOnly(True)
        self.le_angle4.setReadOnly(True)
        self.le_angle5.setReadOnly(True)
        self.le_angle6.setReadOnly(True)
        self.le_runtime.setReadOnly(True)                               # 机械臂运行时间

        # 设置机械臂IO的checkbox为只读
        self.chk_DI0.setDisabled(True)
        self.chk_DI1.setDisabled(True)
        self.chk_DI2.setDisabled(True)
        self.chk_DI3.setDisabled(True)
        self.chk_DI4.setDisabled(True)
        self.chk_DI5.setDisabled(True)
        self.chk_DI6.setDisabled(True)
        self.chk_DI7.setDisabled(True)
        self.chk_DO0.setDisabled(True)
        self.chk_DO1.setDisabled(True)
        self.chk_DO2.setDisabled(True)
        self.chk_DO3.setDisabled(True)
        self.chk_DO4.setDisabled(True)
        self.chk_DO5.setDisabled(True)
        self.chk_DO6.setDisabled(True)
        self.chk_DO7.setDisabled(True)

        # 设置系统关闭、最大/最小/正常化的显示图标
        self.btn_min.setStyleSheet(u"font-family:\"Webdings\";\n")      # 这是一种符号字体，有对照表，0表现为_
        self.btn_max.setStyleSheet(u"font-family:\"Webdings\";\n")      # 1表现为最大化，2表现为正常化
        self.btn_close.setStyleSheet(u"font-family:\"Webdings\";\n")    # r表现为X
        self.btn_min.setText('0')
        self.btn_max.setText('1')
        self.btn_close.setText('r')

        # 设置鼠标追踪，为了配合重写的界面伸缩功能（目前效果和MainWindow自带的一样）
        self.setWindowFlags(Qt.FramelessWindowHint)                     # 去除MainWindow标题栏
        self.setCentralWidget(self.widget_background)                   # 设置MainWindow主窗体（不然鼠标追踪不生效）
        self.setMouseTracking(True)                                     # 设置主窗体（MainWindow）鼠标追踪
        self.widget_background.setMouseTracking(True)                   # 设置主窗体（background）鼠标追踪
        self.widget_tittle.setMouseTracking(True)                       # 设置标题栏鼠标追踪
        self.widget_main.setMouseTracking(True)                         # 设置主要内容窗体鼠标追踪
        self.widget_menu.setMouseTracking(True)                         # 设置菜单栏鼠标追踪
        self.widget_statusbar.setMouseTracking(True)                    # 设置状态栏鼠标追踪

        # 设置各个窗体的Margin
        self.centralwidget.layout().setContentsMargins(0, 0, 0, 0)      # 左、上、右、下
        self.centralwidget.layout().setSpacing(0)
        self.widget_background.layout().setContentsMargins(0, 0, 0, 0)
        self.widget_background.layout().setSpacing(0)
        self.widget_main.layout().setContentsMargins(0, 0, 11, 0)
        self.widget_main.layout().setSpacing(0)
        self.widget_3D.layout().setContentsMargins(0, 11, 0, 11)
        self.widget_3D.layout().setSpacing(0)


        # #6e6b6e       暗沉灰
        # #747780       高亮灰
        # #3c3f41       浅黑
        # #2b2b2b       深黑
        # #0abcd0       高亮淡蓝
        # 设置界面样式
        self.setStyleSheet('''
                /* 界面设置背景颜色 */
                *{font-family:微软雅黑; font-size:15px; color:white;}
                #widget_background{background-color:qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                                stop:0 #3c3f41,  
                                                stop:1 #2b2b2b);;}
                #widget_menu{border-top:0.5px solid #6e6b6e;}
                #widget_main{border-bottom:0.5px solid #6e6b6e;
                            border-top:0.5px solid #6e6b6e;}
        
                
                /* 修饰所有QLineEdit */
                QWidget QLineEdit{border:1px solid #666666; background-color:#7d7d7d; border-radius:2px}
                
                /* 修饰QGroupBox */
                QGroupBox{border:2px solid #444444; margin-top:20px;}
                QGroupBox::title{subcontrol-origin:margin; margin-top:-5px}
                QGroupBox QGroupBox::title{subcontrol-position:top center;}
                
                /* 修饰QGroupBox下QLabel */
                QGroupBox QLabel{font-family:楷体; font-size:15px; color:white;}
                
                /* 修饰QGroupBox下的QCheckBox */
                QGroupBox QCheckBox{border:0px solid;}
                QGroupBox QCheckBox::indicator:checked 
                {
                    width: 20px;
                    height: 20px;
                    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, 
                                                stop:0 #0abcd0,  
                                                stop:0.8 #45474d, 
                                                stop:0.85 #45474d, 
                                                stop:1 #0abcd0);
                    border: 1px solid #45474d;
                    border-radius: 10px;
                }
                QGroupBox QCheckBox::indicator:unchecked{width: 20px;height: 20px;border-radius: 10px;
                                                    background-color: #7d7d7d; border: 1px solid #666666;}
                
                /* 修饰tab页的主体 */
                QTabWidget::pane {background: transparent; border: 5px;}

                /* 修饰tab页表头 */
                QTabBar::tab { background: transparent;
                padding-left: 0px;                                          /*这句决定了标签到文字的距离*/
                padding-right: 0px;
                padding-top: 10px;
                padding-bottom: 10px;
                }
                
                /* 修饰tab页选中时样式 */
                QTabBar::tab:selected, QTabBar::tab:hover {background: #3c3f41; border-right: 2px solid #0abcd0;}
                
                /* 修饰widget下的QPushButton按钮样式 */
                #widget_tittle QPushButton{border:1px; width:50px; height:50px; border-radius:10px}
                #widget_tittle QPushButton:hover {background: #7d7d7d;}
                #widget_tittle QPushButton:pressed{background: #7d7d7d; border-bottom: 2px solid #0abcd0;}
                
                /* QPushButton按钮样式 */
                #widget_menu QPushButton{border:1px; width:80px; height:50px}
                #widget_menu QPushButton:hover {background: #7d7d7d;}
                #widget_menu QPushButton:pressed{background: #7d7d7d; border-bottom: 2px solid #0abcd0;}
             
                /* QRadioButton按钮样式 */
                QRadioButton{background: transparent; border: none;}
                QRadioButton::indicator:checked 
                {
                    width: 20px;
                    height: 20px;
                    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, 
                                                stop:0 #0abcd0,  
                                                stop:0.8 #45474d, 
                                                stop:0.85 #45474d, 
                                                stop:1 #0abcd0);
                    border: 1px solid #45474d;
                    border-radius: 10px;
                }
                QRadioButton::indicator:unchecked{width: 20px;height: 20px;border-radius: 10px;
                                                    background-color: #7d7d7d; border: 1px solid #666666;}
                
                /* 修饰QGroupBox下的QPushButton */
                QGroupBox QPushButton{border:1px; width:50px; height:50px; border-radius:10px}
                QGroupBox QPushButton:hover {background: #7d7d7d;}
                QGroupBox QPushButton:pressed{background: #7d7d7d; border-bottom: 2px solid #0abcd0;}
        ''')

    def load_UR5_models(self):
        '''
        加载UR5模型，并指定初始的位姿样式
        :return:    None
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
                    mesh.rotate_z(-45, center, inplace=True)

                mesh.translate([offset_x, offset_y, 0], inplace=True)               # 通过偏移量让各个部件处于三维坐标系正中心

                self.plotter.add_mesh(mesh, color=mesh_color, smooth_shading=True)  # 添加模型文件，给定颜色，平滑渲染
                group.append(mesh)                                                  # 添加模型进组
            self.robot_joint_mesh[index] = group                                    # 添加关节组至字典，方便后续控制其旋转
            index += 1

    def connect_UR5(self):
        '''
        连接UR5机械臂
        :return:    bool
        '''
        if self.rbtn_con.isChecked():                                                       # 按钮被选中
            ret = self.UR5.connect_30003()                                                  # 尝试连接，初始化socket
            if not ret:                                                                     # 连接失败
                self.MSG.show_message('连接异常', '请检查IP地址、并保证网络通畅', block=True)      # 弹窗提示
                self.rbtn_con.setChecked(False)                                             # 更改按钮为未选中状态
                self.UR5_event.set()                                                        # 数据接收进程休眠
                self.enable_sim_ctl()                                                       # 开启仿真操作权限
                self.timer.stop()                                                           # 关闭刷新定时器
            else:
                self.disable_sim_ctl()                                                      # 禁用仿真操作权限
                if not self.UR5_process_start_status:                                       # 进程未开启，开启进程
                    self.UR5_process_control['Process_flag'] = True                         # 开启进程循环
                    self.UR5.start()                                                        # 启用UR5数据接收进程
                    self.UR5_process_start_status = True                                    # 数据接收线程开启标志
                    self.UR5.connect_29999()                                                # 连接Dashboard端口
                else:
                    self.UR5_event.clear()                                                  # 进程已开启，开启接收事件就行
                self.timer.start()                                                          # 启用界面刷新定时器
        else:                                                                               # 断开连接
            self.UR5_event.set()                                                            # 数据接收进程工作
            self.enable_sim_ctl()                                                           # 开启仿真操作权限
            self.timer.stop()                                                               # 停止刷新定时器

    def UR5_updata(self):
        '''
        实时刷新UR5机械臂模型、界面显示实际数据
        :return:
        '''
        self.joint_radians_real = np.array(self.data30003['实际关节位置'])                    # 接收实机关节弧度
        self.joint_angles_real = np.array(self.joint_radians_real) / np.pi * 180            # 实机弧度转为实机角度

        # 根据接收到的实机数据，转动模型至指定位置
        for i in range(6):
            self.CR.joint_rotation(i+1, self.joint_angles_real[i])                          # 转动关节
        self.update_sim_info()                                                              # 刷新UR5数据
        self.update_UR5_info()                                                              # 刷新UR5其他数据
        pass

    def update_sim_info(self):
        '''
        更新界面显示的械臂的角度、弧度、位姿显示信息，共5处
        :return:    None
        '''
        # 刷新界面右侧TCP显示信息
        self.le_x.setText(str(round(self.TCP_pose[0], self.config['jt_TCP_pre'])))
        self.le_y.setText(str(round(self.TCP_pose[1], self.config['jt_TCP_pre'])))
        self.le_z.setText(str(round(self.TCP_pose[2], self.config['jt_TCP_pre'])))
        self.le_rx.setText(str(round(self.TCP_pose[3], self.config['jt_TCP_pre'])))
        self.le_ry.setText(str(round(self.TCP_pose[4], self.config['jt_TCP_pre'])))
        self.le_rz.setText(str(round(self.TCP_pose[5], self.config['jt_TCP_pre'])))

        # 刷新界面右侧角度信息
        self.le_angle1.setText(str(round(self.joint_angles[0], self.config['jt_angle_pre'])))
        self.le_angle2.setText(str(round(self.joint_angles[1], self.config['jt_angle_pre'])))
        self.le_angle3.setText(str(round(self.joint_angles[2], self.config['jt_angle_pre'])))
        self.le_angle4.setText(str(round(self.joint_angles[3], self.config['jt_angle_pre'])))
        self.le_angle5.setText(str(round(self.joint_angles[4], self.config['jt_angle_pre'])))
        self.le_angle6.setText(str(round(self.joint_angles[5], self.config['jt_angle_pre'])))

        # 刷新界面右侧弧度信息
        self.le_radian1.setText(str(round(self.joint_radians[0], self.config['jt_radian_pre'])))
        self.le_radian2.setText(str(round(self.joint_radians[1], self.config['jt_radian_pre'])))
        self.le_radian3.setText(str(round(self.joint_radians[2], self.config['jt_radian_pre'])))
        self.le_radian4.setText(str(round(self.joint_radians[3], self.config['jt_radian_pre'])))
        self.le_radian5.setText(str(round(self.joint_radians[4], self.config['jt_radian_pre'])))
        self.le_radian6.setText(str(round(self.joint_radians[5], self.config['jt_radian_pre'])))

        # 刷新界面左侧角度信息
        self.le_joint1.setText(str(round(self.joint_angles[0], self.config['jt_angle_pre'])))
        self.le_joint2.setText(str(round(self.joint_angles[1], self.config['jt_angle_pre'])))
        self.le_joint3.setText(str(round(self.joint_angles[2], self.config['jt_angle_pre'])))
        self.le_joint4.setText(str(round(self.joint_angles[3], self.config['jt_angle_pre'])))
        self.le_joint5.setText(str(round(self.joint_angles[4], self.config['jt_angle_pre'])))
        self.le_joint6.setText(str(round(self.joint_angles[5], self.config['jt_angle_pre'])))

        # 刷新界面左侧Slider信息
        self.sld_joint1.setValue((self.joint_angles[0] / self.sld_pre))
        self.sld_joint2.setValue((self.joint_angles[1] / self.sld_pre))
        self.sld_joint3.setValue((self.joint_angles[2] / self.sld_pre))
        self.sld_joint4.setValue((self.joint_angles[3] / self.sld_pre))
        self.sld_joint5.setValue((self.joint_angles[4] / self.sld_pre))
        self.sld_joint6.setValue((self.joint_angles[5] / self.sld_pre))

    def update_UR5_info(self):
        '''
        刷新接收到的UR5实机数据
        :return:
        '''
        DI = bin(256 | self.data30003['数字输入'])[3:]                                           # 处理数字输入值,1-开启，0-关闭
        DO = bin(256 | self.data30003['数字输出'])[3:]                                           # 处理数字输出值,1-开启，0-关闭

        # 刷新机器运行时长
        hours = int(self.data30003['机器运行时长'] // 3600)                                   # 计算小时
        minutes = int((self.data30003['机器运行时长'] % 3600) // 60 )                         # 计算分钟
        seconds = int(self.data30003['机器运行时长'] % 60)                                    # 计算秒
        self.le_runtime.setText('%s: %s: %s' % (hours, minutes, seconds))                   # 显示机械臂运行时间

        # 刷新界面数据
        if DI[7] == '1':
            self.chk_DI0.setChecked(True)
        else:
            self.chk_DI0.setChecked(False)
        if DI[6] == '1':
            self.chk_DI1.setChecked(True)
        else:
            self.chk_DI1.setChecked(False)
        if DI[5] == '1':
            self.chk_DI2.setChecked(True)
        else:
            self.chk_DI2.setChecked(False)
        if DI[4] == '1':
            self.chk_DI3.setChecked(True)
        else:
            self.chk_DI3.setChecked(False)
        if DI[3] == '1':
            self.chk_DI4.setChecked(True)
        else:
            self.chk_DI4.setChecked(False)
        if DI[2] == '1':
            self.chk_DI5.setChecked(True)
        else:
            self.chk_DI5.setChecked(False)
        if DI[1] == '1':
            self.chk_DI6.setChecked(True)
        else:
            self.chk_DI6.setChecked(False)
        if DI[0] == '1':
            self.chk_DI7.setChecked(True)
        else:
            self.chk_DI7.setChecked(False)

        if DO[7] == '1':
            self.chk_DO0.setChecked(True)
        else:
            self.chk_DO0.setChecked(False)
        if DO[6] == '1':
            self.chk_DO1.setChecked(True)
        else:
            self.chk_DO1.setChecked(False)
        if DO[5] == '1':
            self.chk_DO2.setChecked(True)
        else:
            self.chk_DO2.setChecked(False)
        if DO[4] == '1':
            self.chk_DO3.setChecked(True)
        else:
            self.chk_DO3.setChecked(False)
        if DO[3] == '1':
            self.chk_DO4.setChecked(True)
        else:
            self.chk_DO4.setChecked(False)
        if DO[2] == '1':
            self.chk_DO5.setChecked(True)
        else:
            self.chk_DO5.setChecked(False)
        if DO[1] == '1':
            self.chk_DO6.setChecked(True)
        else:
            self.chk_DO6.setChecked(False)
        if DO[0] == '1':
            self.chk_DO7.setChecked(True)
        else:
            self.chk_DO7.setChecked(False)

    def disable_sim_ctl(self):
        '''
        在实机连接时，禁用所有仿真界面操控按钮
        :return:    None
        '''
        # 禁用角度控制文本框
        self.le_joint1.setReadOnly(True)
        self.le_joint2.setReadOnly(True)
        self.le_joint3.setReadOnly(True)
        self.le_joint4.setReadOnly(True)
        self.le_joint5.setReadOnly(True)
        self.le_joint6.setReadOnly(True)

        # 禁用角度控制Slider
        self.sld_joint1.setDisabled(True)
        self.sld_joint2.setDisabled(True)
        self.sld_joint3.setDisabled(True)
        self.sld_joint4.setDisabled(True)
        self.sld_joint5.setDisabled(True)
        self.sld_joint6.setDisabled(True)

    def enable_sim_ctl(self):
        '''
        在实机连接结束后，启用所有仿真界面操控按钮
        :return:
        '''
        # 启用角度控制文本框
        self.le_joint1.setReadOnly(False)
        self.le_joint2.setReadOnly(False)
        self.le_joint3.setReadOnly(False)
        self.le_joint4.setReadOnly(False)
        self.le_joint5.setReadOnly(False)
        self.le_joint6.setReadOnly(False)

        # 启用角度控制Slider
        self.sld_joint1.setDisabled(False)
        self.sld_joint2.setDisabled(False)
        self.sld_joint3.setDisabled(False)
        self.sld_joint4.setDisabled(False)
        self.sld_joint5.setDisabled(False)
        self.sld_joint6.setDisabled(False)

    def window_minimize(self):
        '''
        主界面最小化至任务栏
        :return:    None
        '''
        self.showMinimized()                                    # 主界面最小化

    def window_max_or_nor(self):
        '''
        主界面最大化/正常化，设置的1和2是因为使用的是符号字体
        :return:    None
        '''
        if self.isMaximized():
            self.showNormal()                                   # 主界面正常化
            self.btn_max.setText('1')                           # 设置显示图标
        else:
            self.showMaximized()                                # 主界面最大化
            self.btn_max.setText('2')                           # 设置图标

    def window_close(self):
        '''
        关闭系统，及所有子页面
        :return:    None
        '''
        self.UR5_process_control['Process_flag'] = False            # 关闭进程循环，结束数据接收进程
        if self.UR5_process_start_status:
            self.UR5.close_29999()                                  # 关闭DashBoard端口
        time.sleep(0.2)                                             # 给0.2s的延时，确保进程正确关闭
        self.close()                                                # 关闭系统页面

    def mousePressEvent(self, event):
        '''
        重写mousePressEvent函数，鼠标点击后，确定所点击的区域（拖拽只在固定区域生效）
        :param event:   QT事件
        :return:        None
        '''
        if (event.button() == Qt.LeftButton) and (event.pos() in self._corner_rect):
            self._corner_drag = True                                    # 鼠标左键点击右下角边界区域
            event.accept()                                              # 告诉系统该事件已被处理，无需调用其他函数
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._right_rect):
            self._right_drag = True                                     # 鼠标左键点击右侧边界区域
            event.accept()                                              # 告诉系统该事件已被处理，无需调用其他函数
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._bottom_rect):
            self._bottom_drag = True                                    # 鼠标左键点击下侧边界区域
            event.accept()                                              # 告诉系统该事件已被处理，无需调用其他函数
        elif (event.button() == Qt.LeftButton) and (event.y() < self.widget_tittle.height()):
            self._move_drag = True              # 鼠标左键点击标题栏区域
            self.move_DragPosition = event.globalPos() - self.pos()     # 获取界面需要移动到的位置
            event.accept()

    def mouseMoveEvent(self, event):
        '''
        重写mouseMoveEvent函数，调整系统整体边界范围，实现鼠标拖放缩放窗口大小，并改变在各个区域的鼠标光标样式
        :param event:   QT事件
        :return:        None
        '''
        # 设置鼠标光标样式
        if event.pos() in self._corner_rect:
            self.setCursor(Qt.SizeFDiagCursor)                          # 如果光标在右下角，设置为右下角拉伸样式
            event.accept()
        elif event.pos() in self._bottom_rect:
            self.setCursor(Qt.SizeVerCursor)                            # 如果光标在底部，设置为垂直光标样式
            event.accept()
        elif event.pos() in self._right_rect:
            self.setCursor(Qt.SizeHorCursor)                            # 如果光标在右侧，设置为水平光标样式
            event.accept()
        else:
            self.setCursor(Qt.ArrowCursor)                              # 如果在其他区域，设置为默认样式

        # 当鼠标左键点击右下、底部、右侧时调整窗口大小，点击标题栏时调整系统整体位置
        if Qt.LeftButton and self._right_drag:
            self.resize(event.pos().x(), self.height())                 # 右侧调整窗口宽度
            event.accept()
        elif Qt.LeftButton and self._bottom_drag:

            self.resize(self.width(), event.pos().y())                  # 底部调整窗口高度
            event.accept()
        elif Qt.LeftButton and self._corner_drag:
            self.resize(event.pos().x(), event.pos().y())               # 右下角同时调整高度和宽度
            event.accept()
        elif Qt.LeftButton and self._move_drag:
            self.move(event.globalPos() - self.move_DragPosition)       # 标题栏调整窗口整体位置
            event.accept()

    def mouseReleaseEvent(self, event):
        '''
        重写mouseReleaseEvent函数，鼠标释放后，各控制变量复位
        :param event:   QT事件
        :return:        None
        '''
        self._move_drag = False                                         # 窗口整体拖动变量复位
        self._corner_drag = False                                       # 右下角调整大小变量复位
        self._bottom_drag = False                                       # 底部调整大小变量复位
        self._right_drag = False                                        # 右侧调整大小变量复位

    def resizeEvent(self, event):
        '''
        重写resizeEvent函数，生成界面范围，用于mouseMoveEvent更改界面大小
        :param event:   QT事件
        :return:        None
        '''
        # 设置右侧追踪边界范围，宽度：5px，高度：整边追踪（留了100px给右下角）
        self._right_rect = [QPoint(x, y) for x in range(self.width()-7, self.width())
                            for y in range(100, self.height()-20)]

        # 设置底部追踪边界范围，宽度：整边追踪（留了100px给右下角），高度：8px
        self._bottom_rect = [QPoint(x, y) for x in range(0, self.width()-100)
                             for y in range(self.height()-8, self.height())]

        # 设置右下角追踪，20 * 20 px的正方形
        self._corner_rect = [QPoint(x, y) for x in range(self.width()-20, self.width())
                             for y in range(self.height()-20, self.height())]

