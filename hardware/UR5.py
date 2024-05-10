# -*- coding: utf-8 -*-
"""
@Time ： 2024/4/26 17:03
@Auth ： Ethan
@File ：UR5.py
@IDE ：PyCharm
"""
import time
import socket
import struct
import threading
import numpy as np


class UR5(threading.Thread):
    def __init__(self, MainWin):
        super(UR5, self).__init__()
        self.MainWin = MainWin
        self.setDaemon(True)            # 设置为守护线程
        self.data = {}                  # 用来实时接收数据

    def connect(self):
        '''
        连接realtime-30003，Dashboard-29999端口
        :return: bool
        '''
        try:
            # 连接30003端口，用于接收数据，发送控制脚本
            self.sk30003 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sk30003.connect((self.MainWin.config["UR_IP"], 30003))

            # 连接29999端口，用于控制硬件
            self.sk29999 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sk29999.connect((self.MainWin.config["UR_IP"], 29999))
        except Exception as e:
            print(e)
            return False
        return True

    def close(self):
        '''
        关闭与UR5机械臂的连接
        :return: None
        '''
        self.sk29999.close()
        self.sk30003.close()

    def dashboard(self, instruct: str, type: str):
        '''
        执行DashBoard指令
        :param instruct:    指令名称
        :param type:        指令是否有返回值
        :return:            指令所需的返回值
        '''
        if type == "return":
            self.sk29999.send(instruct.encode('utf8'))
            res = self.sk29999.recv(2000)
            return res
        else:
            self.sk29999.send(instruct.encode('utf8'))
            return None

    def movej(self, args: list, type: str, a=0.2, v=0.2, t=0, r=0):
        '''
        移动至指定位置
        :param args:    目标点，[arg1, arg2, arg3, arg4, arg5, arg6]
        :param type:    数据类型：pose、angle、radian
        :param a:       主关节加速度，rad/s^2
        :param v:       主轴联合速度，rad/s
        :param t:       运动时间，s，该设置优先级大于a和v
        :param r:       混合半径，m
        :return:        None
        '''
        if type == "pose":
            data = 'movej(get_inverse_kin(p%s), a=%s, v=%s, t=%s, r=%s)\n' % (args, a, v, t, r)
        elif type == "radian":
            data = 'movej(%s, a=%s, v=%s, t=%s, r=%s)\n' % (args, a, v, t, r)
        else:
            radian = []
            for i in args:
                radian.append(i * np.pi / 180)
            data = 'movej(%s, a=%s, v=%s, t=%s, r=%s)\n' % (radian, a, v, t, r)
        self.sk30003.send(data.encode('utf8'))

    def movel(self, args: list, type: str, a=0.2, v=0.2, t=0, r=0):
        '''
        移动至指定位置，在工具空间中线性运动
        :param args:    目标点，[arg1, arg2, arg3, arg4, arg5, arg6]
        :param type:    数据类型：pose、angle、radian
        :param a:       主关节加速度，rad/s^2
        :param v:       主轴联合速度，rad/s
        :param t:       运动时间，s，该设置优先级大于a和v
        :param r:       混合半径，m
        :return:        None
        '''
        if type == "pose":
            data = 'movel(p%s, a=%s, v=%s, t=%s, r=%s)\n' % (args, a, v ,t, r)
        elif type == "radian":
            data = 'movel(get_forward_kin(%s), a=%s, v=%s, t=%s, r=%s)\n' % (args, a, v ,t, r)
        else:
            radian = []
            for i in args:
                radian.append(i * np.pi / 180)
            data = 'movel(get_forward_kin(%s), a=%s, v=%s, t=%s, r=%s)\n' % (radian, a, v ,t, r)
        self.sk30003.send(data.encode('utf8'))

    def movec(self, args1: list, args2: list, type: str, a=0.2, v=0.2, r=0, mode=0):
        '''
        以圆形的方式移动到指定位置，通过arg1，到达arg2，加速到v并以恒定的速度移动
        :param args1:   途径点，[arg1, arg2, arg3, arg4, arg5, arg6]
        :param args2:   终点，[arg1, arg2, arg3, arg4, arg5, arg6]
        :param type:    数据类型：pose、angle、radian
        :param a:       主关节加速度，rad/s^2
        :param v:       主轴联合速度，rad/s
        :param r:       混合半径，m
        :param mode:    0：无限制模式     1：保持于相对圆弧切线方向恒定
        :return:        None
        '''
        if type == "pose":
            data = 'movec(p%s, p%s, a=%s, v=%s, r=%s, mode=%s)\n' % (args1, args2, a, v, r, mode)
        elif type == 'radian':
            data = 'movec(get_forward_kin(%s), get_forward_kin(%s), a=%s, v=%s, r=%s, mode=%s)\n' % (
                args1, args2, a, v, r, mode)
        else:
            radian1 = []
            radian2 = []
            for i in range(6):
                radian1.append(args1[i] * np.pi / 180)
                radian2.append(args2[i] * np.pi / 180)
            data = 'movec(get_forward_kin(%s), get_forward_kin(%s), a=%s, v=%s, r=%s, mode=%s)\n' % (
                radian1, radian2, a, v, r, mode)
        self.sk30003.send(data.encode('utf8'))

    def movep(self, args: list, type: str, a=0.2, v=0.2, r=0):
        '''
        混合圆形并线性运动到指定位置，工具空间加速到v后恒定
        :param args:    目标点，[arg1, arg2, arg3, arg4, arg5, arg6]
        :param type:    数据类型：pose、angle、radian
        :param a:       主关节加速度，rad/s^2
        :param v:       主轴联合速度，rad/s
        :param r:       混合半径，m
        :return:        None
        '''

        if type == 'pose':
            data = 'movep(p%s, a=%s, v=%s, r=%s)\n' % (args, a, v, r)
        elif type == 'radian':
            data = 'movep(get_forward_kin(%s), a=%s, v=%s, r=%s)\n' % (args, a, v, r)
        else:
            radian = []
            for i in args:
                radian.append(i * np.pi / 180)
            data = 'movep(get_forward_kin(%s), a=%s, v=%s, r=%s)\n' % (radian, a, v, r)
        self.sk30003.send(data.encode('utf8'))

    def send_script(self, file_path: str):
        '''
        发送机器人script脚本文件
        :param:     file_name: 文件路径
        :return:    None
        '''
        data2 = ''
        with open('%s' % file_path, 'r', encoding='utf8') as f:
            for i in f.readlines():
                data2 += i
        self.sk30003.send(data2.encode('utf8'))

    def get_message(self):
        '''
        机械臂作为客户端，上位机作为服务器，该函数保留，供参考
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

    def run(self):
        '''
        解析30003发送过来的数据
        :return:
        '''
        while True:
            if self.MainWin.UR5_con_status:                         # UR5连接开启才接收数据
                res = self.sk30003.recv(2000)
                try:
                    self.data['总计数据长度'] = int.from_bytes(res[0:4], byteorder='big')
                    self.data['机器运行时长'] = struct.unpack('>d', res[4:12])[0]
                    self.data['目标关节位置'] = [struct.unpack('>d', res[12:20])[0],
                                                struct.unpack('>d', res[20:28])[0],
                                                struct.unpack('>d', res[28:36])[0],
                                                struct.unpack('>d', res[36:44])[0],
                                                struct.unpack('>d', res[44:52])[0],
                                                struct.unpack('>d', res[52:60])[0]]
                    self.data['目标关节速度'] = [struct.unpack('>d', res[60:68])[0],
                                                struct.unpack('>d', res[68:76])[0],
                                                struct.unpack('>d', res[76:84])[0],
                                                struct.unpack('>d', res[84:92])[0],
                                                struct.unpack('>d', res[92:100])[0],
                                                struct.unpack('>d', res[100:108])[0]]
                    self.data['目标关节加速度'] = [struct.unpack('>d', res[108:116])[0],
                                                struct.unpack('>d', res[116:124])[0],
                                                struct.unpack('>d', res[124:132])[0],
                                                struct.unpack('>d', res[132:140])[0],
                                                struct.unpack('>d', res[140:148])[0],
                                                struct.unpack('>d', res[148:156])[0]]
                    self.data['目标关节电流'] = [struct.unpack('>d', res[156:164])[0],
                                                struct.unpack('>d', res[164:172])[0],
                                                struct.unpack('>d', res[172:180])[0],
                                                struct.unpack('>d', res[180:188])[0],
                                                struct.unpack('>d', res[188:196])[0],
                                                struct.unpack('>d', res[196:204])[0]]
                    self.data['目标关节力矩'] = [struct.unpack('>d', res[204:212])[0],
                                                struct.unpack('>d', res[212:220])[0],
                                                struct.unpack('>d', res[220:228])[0],
                                                struct.unpack('>d', res[228:236])[0],
                                                struct.unpack('>d', res[236:244])[0],
                                                struct.unpack('>d', res[244:252])[0]]
                    self.data['实际关节位置'] = [struct.unpack('>d', res[252:260])[0],
                                                struct.unpack('>d', res[260:268])[0],
                                                struct.unpack('>d', res[268:276])[0],
                                                struct.unpack('>d', res[276:284])[0],
                                                struct.unpack('>d', res[284:292])[0],
                                                struct.unpack('>d', res[292:300])[0]]
                    self.data['实际关节速度'] = [struct.unpack('>d', res[300:308])[0],
                                                struct.unpack('>d', res[308:316])[0],
                                                struct.unpack('>d', res[316:324])[0],
                                                struct.unpack('>d', res[324:332])[0],
                                                struct.unpack('>d', res[332:340])[0],
                                                struct.unpack('>d', res[340:348])[0]]
                    self.data['实际关节电流'] = [struct.unpack('>d', res[348:356])[0],
                                                struct.unpack('>d', res[356:364])[0],
                                                struct.unpack('>d', res[364:372])[0],
                                                struct.unpack('>d', res[372:380])[0],
                                                struct.unpack('>d', res[380:388])[0],
                                                struct.unpack('>d', res[388:396])[0]]
                    self.data['关节联合电流'] = [struct.unpack('>d', res[396:404])[0],
                                                struct.unpack('>d', res[404:412])[0],
                                                struct.unpack('>d', res[412:420])[0],
                                                struct.unpack('>d', res[420:428])[0],
                                                struct.unpack('>d', res[428:436])[0],
                                                struct.unpack('>d', res[436:444])[0]]
                    self.data['工具矢量'] = [struct.unpack('>d', res[444:452])[0],
                                                struct.unpack('>d', res[452:460])[0],
                                                struct.unpack('>d', res[460:468])[0],
                                                struct.unpack('>d', res[468:476])[0],
                                                struct.unpack('>d', res[476:484])[0],
                                                struct.unpack('>d', res[484:492])[0]]
                    self.data['TCP实际速度'] = [struct.unpack('>d', res[492:500])[0],
                                                struct.unpack('>d', res[500:508])[0],
                                                struct.unpack('>d', res[508:516])[0],
                                                struct.unpack('>d', res[516:524])[0],
                                                struct.unpack('>d', res[524:532])[0],
                                                struct.unpack('>d', res[532:540])[0]]
                    self.data['TCP一般力'] = [struct.unpack('>d', res[540:548])[0],
                                                struct.unpack('>d', res[548:556])[0],
                                                struct.unpack('>d', res[556:564])[0],
                                                struct.unpack('>d', res[564:572])[0],
                                                struct.unpack('>d', res[572:580])[0],
                                                struct.unpack('>d', res[580:588])[0]]
                    self.data['工具目标矢量'] = [struct.unpack('>d', res[588:596])[0],
                                                struct.unpack('>d', res[596:604])[0],
                                                struct.unpack('>d', res[604:612])[0],
                                                struct.unpack('>d', res[612:620])[0],
                                                struct.unpack('>d', res[620:628])[0],
                                                struct.unpack('>d', res[628:636])[0]]
                    self.data['工具目标速度'] = [struct.unpack('>d', res[636:644])[0],
                                                struct.unpack('>d', res[644:652])[0],
                                                struct.unpack('>d', res[652:660])[0],
                                                struct.unpack('>d', res[660:668])[0],
                                                struct.unpack('>d', res[668:676])[0],
                                                struct.unpack('>d', res[676:684])[0]]
                    self.data['数字输入'] = int.from_bytes(res[684:692], byteorder='big')
                    self.data['电机温度'] = [struct.unpack('>d', res[692:700])[0],
                                                struct.unpack('>d', res[700:708])[0],
                                                struct.unpack('>d', res[708:716])[0],
                                                struct.unpack('>d', res[716:724])[0],
                                                struct.unpack('>d', res[724:732])[0],
                                                struct.unpack('>d', res[732:740])[0]]
                    self.data['控制器实时线程执行时间'] = struct.unpack('>d', res[740:748])[0]
                    self.data['UR软件测试值'] = struct.unpack('>d', res[748:756])[0]
                    self.data['机器人模式'] = struct.unpack('>d', res[756:764])[0]
                    self.data['关节模式'] = [struct.unpack('>d', res[764:772])[0],
                                                struct.unpack('>d', res[772:780])[0],
                                                struct.unpack('>d', res[780:788])[0],
                                                struct.unpack('>d', res[788:796])[0],
                                                struct.unpack('>d', res[796:804])[0],
                                                struct.unpack('>d', res[804:812])[0]]
                    self.data['安全模式'] = struct.unpack('>d', res[812:820])[0]
                    self.data['UR安全模式'] = [struct.unpack('>d', res[820:828])[0],
                                                struct.unpack('>d', res[828:836])[0],
                                                struct.unpack('>d', res[836:844])[0],
                                                struct.unpack('>d', res[844:852])[0],
                                                struct.unpack('>d', res[852:860])[0],
                                                struct.unpack('>d', res[860:868])[0]]
                    self.data['机器人工具加速度'] = [struct.unpack('>d', res[868:876])[0],
                                                struct.unpack('>d', res[876:884])[0],
                                                struct.unpack('>d', res[884:892])[0]]
                    self.data['UR机器人工具加速度'] = [struct.unpack('>d', res[892:900])[0],
                                                struct.unpack('>d', res[900:908])[0],
                                                struct.unpack('>d', res[908:916])[0],
                                                struct.unpack('>d', res[916:924])[0],
                                                struct.unpack('>d', res[924:932])[0],
                                                struct.unpack('>d', res[932:940])[0]]
                    self.data['轨迹限制器速度缩放'] = struct.unpack('>d', res[940:948])[0]
                    self.data['线性动量范数'] = struct.unpack('>d', res[948:956])[0]
                    self.data['UR线性动量范数'] = struct.unpack('>d', res[956:964])[0]
                    self.data['URS线性动量范数'] = struct.unpack('>d', res[964:972])[0]
                    self.data['主电压'] = struct.unpack('>d', res[972:980])[0]
                    self.data['机器人电压'] = struct.unpack('>d', res[980:988])[0]
                    self.data['机器人实际电压'] = struct.unpack('>d', res[988:996])[0]
                    self.data['关节实际电压'] = [struct.unpack('>d', res[996:1004])[0],
                                                struct.unpack('>d', res[1004:1012])[0],
                                                struct.unpack('>d', res[1012:1020])[0],
                                                struct.unpack('>d', res[1020:1028])[0],
                                                struct.unpack('>d', res[1028:1036])[0],
                                                struct.unpack('>d', res[1036:1044])[0]]
                    self.data['数字输出'] = struct.unpack('>d', res[1044:1052])[0]
                    self.data['程序状态'] = struct.unpack('>d', res[1052:1060])[0]
                    self.data['肘部位置'] = [struct.unpack('>d', res[1060:1068])[0],
                                                struct.unpack('>d', res[1068:1076])[0],
                                                struct.unpack('>d', res[1076:1084])[0]]
                    self.data['肘部速度'] = [struct.unpack('>d', res[1084:1092])[0],
                                                struct.unpack('>d', res[1092:1100])[0],
                                                struct.unpack('>d', res[1100:1108])[0]]
                    self.data['安全状态'] = struct.unpack('>d', res[1108:1116])[0]
                    self.data['UR安全状态1'] = struct.unpack('>d', res[1116:1124])[0]
                    self.data['UR安全状态2'] = struct.unpack('>d', res[1124:1132])[0]
                    self.data['UR安全状态3'] = struct.unpack('>d', res[1132:1140])[0]
                    # print('总计长度', self.data['总计数据长度'], '\t\t实际接收：', len(res))
                    self.MainWin.data30003 = self.data              # 将接收到的准确数据转移
                except Exception as e:
                    # print(e, '=======', self.data['总计数据长度'])
                    pass
            else:
                time.sleep(0.5)

