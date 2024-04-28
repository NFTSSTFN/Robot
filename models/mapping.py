# -*- coding: utf-8 -*-
"""
@Time ： 2024/4/26 11:32
@Auth ： Ethan
@File ：mapping.py
@IDE ：PyCharm
"""

# 模型映射到颜色
robot_mesh_color = {
    # 蓝色
    (104 / 255, 132 / 255, 147 / 255): ["UR5 - 24105_Support.step-1 34311_Support.step-1.STL",
                                        "UR5 - 24105_Support.step-1 34311_Support.step-2.STL",
                                        "UR5 - 24105_Support.step-1 34311_Support.step-3.STL",
                                        "UR5 - 24105_Support.step-1 34111_Support.step-1.STL",
                                        "UR5 - 24105_Support.step-1 34111_Support.step-2.STL",
                                        "UR5 - 24105_Support.step-1 34111_Support.step-3.STL"],
    # 灰色
    (155 / 255, 158 / 255, 166 / 255): ["UR5 - 24105_Support.step-1 31001_Support.step-1.STL",
                                        "UR5 - 24105_Support.step-1 31008_Support.step-1.STL",
                                        "UR5 - 24105_Support.step-1 31101_Support.step-1.STL",
                                        "UR5 - 24105_Support.step-1 31101_Support.step-2.STL",
                                        "UR5 - 24105_Support.step-1 31101_Support.step-3.STL",
                                        "UR5 - 24105_Support.step-1 31105_Support.step-1.STL",
                                        'UR5 - 24105_Support.step-1 31106_Support.step-1.STL',
                                        "UR5 - 24105_Support.step-1 31132_Support.step-1.STL",
                                        "UR5 - 24105_Support.step-1 31132_Support.step-2.STL",
                                        "UR5 - 24105_Support.step-1 31301_Support.step-1.STL",
                                        "UR5 - 24105_Support.step-1 31301_Support.step-2.STL",
                                        "UR5 - 24105_Support.step-1 31301_Support.step-3.STL",
                                        "UR5 - 24105_Support.step-1 31305_Support.step-1.STL",
                                        "UR5 - 24105_Support.step-1 31320_Support.step-1.STL"],
    # 黑色
    (32 / 255, 32 / 255, 33 / 255): ["UR5 - 24105_Support.step-1 33316_Support.step-1.STL",
                                     "UR5 - 24105_Support.step-1 33316_Support.step-2.STL",
                                     "UR5 - 24105_Support.step-1 33316_Support.step-3.STL",
                                     "UR5 - 24105_Support.step-1 33303_Support.step-1.STL",
                                     "UR5 - 24105_Support.step-1 33303_Support.step-2.STL",
                                     "UR5 - 24105_Support.step-1 33303_Support.step-3.STL",
                                     "UR5 - 24105_Support.step-1 31362_Support.step-1.STL",
                                     "UR5 - 24105_Support.step-1 31362_Support.step-2.STL",
                                     "UR5 - 24105_Support.step-1 31362_Support.step-3.STL",
                                     "UR5 - 24105_Support.step-1 33103_Support.step-1.STL",
                                     "UR5 - 24105_Support.step-1 33103_Support.step-2.STL",
                                     "UR5 - 24105_Support.step-1 33103_Support.step-3.STL",
                                     "UR5 - 24105_Support.step-1 33115_Support.step-1.STL",
                                     "UR5 - 24105_Support.step-1 33116_Support.step-1.STL",
                                     "UR5 - 24105_Support.step-1 33116_Support.step-2.STL",
                                     "UR5 - 24105_Support.step-1 33116_Support.step-3.STL", ]
}

# 模型映射到旋转轴
# key为旋转轴
# val里面的val为轴变动的时候需要旋转的模型
robot_mesh_joint = {
    # 底座
    "base": [
        "UR5 - 24105_Support.step-1 31320_Support.step-1.STL"
    ],
    # 第一个轴点
    "joint1": ["UR5 - 24105_Support.step-1 31301_Support.step-1.STL",
               "UR5 - 24105_Support.step-1 31362_Support.step-3.STL",
               "UR5 - 24105_Support.step-1 33303_Support.step-1.STL",
               "UR5 - 24105_Support.step-1 33316_Support.step-3.STL",
               "UR5 - 24105_Support.step-1 34311_Support.step-1.STL",
               ],
    # 第二个轴点
    "joint2": ["UR5 - 24105_Support.step-1 31301_Support.step-2.STL",
               "UR5 - 24105_Support.step-1 31301_Support.step-3.STL",
               "UR5 - 24105_Support.step-1 31305_Support.step-1.STL",
               "UR5 - 24105_Support.step-1 31362_Support.step-2.STL",
               "UR5 - 24105_Support.step-1 31362_Support.step-2.STL",
               "UR5 - 24105_Support.step-1 33303_Support.step-2.STL",
               "UR5 - 24105_Support.step-1 33316_Support.step-1.STL",
               "UR5 - 24105_Support.step-1 34311_Support.step-2.STL",
               "UR5 - 24105_Support.step-1 34311_Support.step-3.STL"
               ],
    # 第三个轴点
    "joint3": ["UR5 - 24105_Support.step-1 31001_Support.step-1.STL",
               "UR5 - 24105_Support.step-1 31101_Support.step-1.STL",
               "UR5 - 24105_Support.step-1 31105_Support.step-1.STL",
               "UR5 - 24105_Support.step-1 31106_Support.step-1.STL",
               "UR5 - 24105_Support.step-1 31132_Support.step-1.STL",
               "UR5 - 24105_Support.step-1 31362_Support.step-1.STL",
               "UR5 - 24105_Support.step-1 33115_Support.step-1.STL",
               "UR5 - 24105_Support.step-1 33303_Support.step-3.STL",
               "UR5 - 24105_Support.step-1 33316_Support.step-2.STL",
               "UR5 - 24105_Support.step-1 34111_Support.step-1.STL",

               ],
    # 第四个轴点
    "joint4": ["UR5 - 24105_Support.step-1 31101_Support.step-2.STL",
               "UR5 - 24105_Support.step-1 31132_Support.step-2.STL",
               "UR5 - 24105_Support.step-1 33103_Support.step-1.STL",
               "UR5 - 24105_Support.step-1 33116_Support.step-3.STL",
               "UR5 - 24105_Support.step-1 34111_Support.step-2.STL",
               ],
    # 第五个轴点
    "joint5": ["UR5 - 24105_Support.step-1 31101_Support.step-3.STL",
               "UR5 - 24105_Support.step-1 33103_Support.step-2.STL",
               "UR5 - 24105_Support.step-1 33116_Support.step-2.STL",
               "UR5 - 24105_Support.step-1 34111_Support.step-3.STL",

               ],
    # 第六个轴点
    "joint6": ["UR5 - 24105_Support.step-1 31008_Support.step-1.STL",
               "UR5 - 24105_Support.step-1 33103_Support.step-3.STL",
               "UR5 - 24105_Support.step-1 33116_Support.step-1.STL",

               ]
}







