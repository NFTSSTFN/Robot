# -*- coding: utf-8 -*-
"""
@Time ： 2024/4/26 17:14
@Auth ： Ethan
@File ：dealply.py
@IDE ：PyCharm
"""

import trimesh
import numpy as np
import struct

class DealPLy:
    def deal_ply(self):
        with open('../data/pointmap.ply', 'rb') as f:
            a = f.readlines()
            data = a[8]

        points = []
        for i in range(0, len(data), 12):
            # print(binary_data[i:i + 12], len(binary_data[i:i + 12]))
            temp = []
            try:
                float_value = struct.unpack('fff', data[i:i + 12])
                if not np.isnan(float_value[0]):
                    temp.append(float_value[0])
                    temp.append(float_value[1])
                    temp.append(float_value[2])
                    points.append(temp)
            except Exception as e:
                pass
        print(np.array(points)[0:10])

    def deal_ply_fast(self):
        a = trimesh.load_mesh('../data/pointmap.ply')
        b = a.vertices[np.all(np.isfinite(a.vertices), axis=1)]
        c = trimesh.Trimesh(vertices=b)
        self.save_ply('../data/a.ply', c.vertices)

    def save_ply(self, file_path, vertices):
        num_vertices = len(vertices)

        with open(file_path, 'w') as file:
            file.write('ply\n')
            file.write('format ascii 1.0\n')
            file.write('element vertex %d\n' % num_vertices)
            file.write('property float x\n')
            file.write('property float y\n')
            file.write('property float z\n')
            file.write('end_header\n')

            for vertex in vertices:
                file.write('%f %f %f\n' % (vertex[0], vertex[1], vertex[2]))
