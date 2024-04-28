# -*- coding: utf-8 -*-
"""
@Time ： 2024/4/26 17:03
@Auth ： Ethan
@File ：UR5e.py
@IDE ：PyCharm
"""

import socket
import struct
import numpy as np

class UR5e:
    IP = "192.168.6.101"
    def __init__(self):
        # 创建套接字
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sk.connect((self.IP, 30003))
        # self.sk.connect((self.IP, 29999))

    def send_test(self):
        '''
        发送测试脚本，让机器人在两点之间一直移动
        :return: None
        '''

        data = '''
def aa():
    global u36335u28857_1_p=p[-.197374113827, .456635515434, .239763510108, .519323155645, -3.041692776212, -.160764931300]
    global u36335u28857_1_q=[4.817089080810547, -1.6204215488829554, 1.93193227449526, -1.9831730328001917, -1.5105860869037073, -3.368830982838766]
    global u36335u28857_2_p=p[.192933185509, .429668501251, .205517059326, 1.147386576548, 2.879895566718, .061746840311]
    global u36335u28857_2_q=[4.014283180236816, -1.6201702557005824, 2.0078185240374964, -2.009040971795553, -1.5950382391559046, -3.078739945088522]
    while (True):
        movej(get_inverse_kin(u36335u28857_1_p, qnear=u36335u28857_1_q), a=1.3962634015954636, v=1.0471975511965976)
        movej(get_inverse_kin(u36335u28857_2_p, qnear=u36335u28857_2_q), a=1.3962634015954636, v=1.0471975511965976)
    end
end
        '''
        self.sk.send(data.encode('utf8'))

    def send_script(self, file_path):
        '''
        发送机器人script脚本文件
        :param file_name: 文件路径
        :return: None
        '''

        data2 = ''
        with open('%s' % file_path, 'r', encoding='utf8') as f:
            for i in f.readlines():
                data2 += i
        self.sk.send(data2.encode('utf8'))

    def get_message(self):
        '''
        机械臂作为客户端，上位机作为服务器
        :return: None
        '''
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.bind(('192.168.1.55', 8000))
        sk.listen(1)
        conn, addr = sk.accept()        # 等待客户端连接请求
        while True:
            data = conn.recv(1024)
            print("接收消息:", addr, data)

            # 发送响应给客户端
            response = "(0,0,11,22,33,0)"
            conn.send(response.encode())

    def init_arm(self):
        '''
        初始化机械臂，只能在29999端口进行设置，并且有反馈
        :return: None
        '''

        data1 = 'power on'      # 开启机器人电源
        data2 = 'brake release' # 释放制动器
        data3 = 'power off'     # 关闭机器人电源
        data4 = 'shutdown'      # 关机

        self.sk.send(data4.encode('utf8'))
        self.sk.close()

    def parse_data(self):
        '''
        解析30003发送过来的数据
        :return:
        '''
        while True:
            res = self.sk.recv(2000)
            print('数据长度：', int.from_bytes(res[0:4], byteorder='big'))
            print('时间：', struct.unpack('>d', res[4:12])[0])
            print('目标关节位置：', struct.unpack('>d', res[12:20])[0],
                                  struct.unpack('>d', res[20:28])[0],
                                  struct.unpack('>d', res[28:36])[0],
                                  struct.unpack('>d', res[36:44])[0],
                                  struct.unpack('>d', res[44:52])[0],
                                  struct.unpack('>d', res[52:60])[0])

    def movej_pose(self, pose):
        '''
        根据位姿移动到指定点
        :param pose:    p[x, y, z, rx, ry, rz]
        :return:        None
        '''

        data = 'movej(get_inverse_kin(%s), a=0.2, v=0.2)\n' % pose
        self.sk.send(data.encode('utf8'))
        self.sk.close()

    def movej_radian(self, radian : list):
        '''
        根据弧度信息移动到指定点
        :param radian:    [r1, r2, r3, r4, r5, r6]
        :return:        None
        '''

        data = 'movej(%s, a=0.2, v=0.2)\n' % radian
        self.sk.send(data.encode('utf8'))
        self.sk.close()

    def movej_angle(self, angle : list):
        '''
        根据角度信息移动到指定点
        :param angle:   [a1, a2, a3, a4, a5, a6]
        :return:        None
        '''
        radian = []
        for i in angle:
            radian.append(i * np.pi / 180)

        data = 'movej(%s, a=0.2, v=0.2)\n' % radian
        self.sk.send(data.encode('utf8'))
        self.sk.close()

    def movel_pose(self, pose : list):
        '''
        根据位姿信息直线运动到指定点
        :param pose:    p[x, y, z, rx, ry, rz]
        :return:        None
        '''

        data = 'movel(%s, a=0.2, v=0.2)\n' % pose
        self.sk.send(data.encode('utf8'))
        self.sk.close()