# Copyright (c) RVBUST, Inc - All rights reserved.
import PyRVC as RVC
import os
import numpy as np
import cv2
from Utils.Tools import *



class Camera:
    def connect(self):
        '''
        连接双目相机
        :return: 1 -- 成功，-1 -- 失败
        '''
        RVC.SystemInit()  # 初始化 RVC X system.
        # 搜索设备列表，取列表中第一个设备作为目标机器
        ret, devices = RVC.SystemListDevices(RVC.SystemListDeviceTypeEnum.All)
        if len(devices) == 0:
            print("找不到设备！！!")
            RVC.SystemShutdown()
            return -1
        self.device = devices[0]

        # 获取设备信息
        ret, self.info = self.device.GetDeviceInfo()
        print(self.info.name + "-" + self.info.sn)
        return 1

    def capture(self, mode):
        '''
        相机拍摄
        :param mode: [int], 0-坐相机，1-右相机，2-双相机
        :return:
        '''
        self.mode = mode
        if mode == 2:
            if not self.info.support_x2:
                print("Device does not support x2 function !")
                RVC.SystemShutdown()
                return -1
            # Create and Open
            self.x2 = RVC.X2.Create(self.device)
            ret = self.x2.Open()
            if ret and self.x2.IsValid():
                print("Camera is valid!")
            else:
                print("Camera is not valid!")
                RVC.X2.Destroy(self.x2)
                RVC.SystemShutdown()
                return -1

            # 打印第一个相机参数，打印曝光时间范围
            _, exp_range_min, exp_range_max = self.x2.GetExposureTimeRange()
            print("ExposureTime Range:[{}, {}]".format(exp_range_min, exp_range_max))

            # Capture
            ret = self.x2.Capture()
            if ret:
                print("Capture successed!")
            else:
                print("Capture failed!")
                print(RVC.GetLastErrorMessage())
                self.x2.Close()
                RVC.X2.Destroy(self.x2)
                RVC.SystemShutdown()
                return -1

            img = self.x2.GetImage(RVC.CameraID_Left)
            pm = self.x2.GetPointMap()      # 获取三维点云数据
        else:
            if mode == 0:
                self.x1 = RVC.X1.Create(self.device, RVC.CameraID_Left)     # 这里会创建一个MvSdkLog
            else:
                self.x1 = RVC.X1.Create(self.device, RVC.CameraID_Right)    # 这里会创建一个MvSdkLog
            ret = self.x1.Open()
            if ret and self.x1.IsValid():
                print("相机就绪!")
            else:
                print("相机未就绪！！!")
                RVC.X1.Destroy(self.x1)
                RVC.SystemShutdown()
                return -1

            # 打印第一个相机参数，打印曝光时间范围
            _, exp_range_min, exp_range_max = self.x1.GetExposureTimeRange()
            print("曝光时间范围:[{}, {}]".format(exp_range_min, exp_range_max))

            # 捕获图像
            ret = self.x1.Capture()
            if ret:
                print("拍摄成功!")
            else:
                print("拍摄失败！！！")
                print(RVC.GetLastErrorMessage())
                self.x1.Close()
                RVC.X1.Destroy(self.x1)
                RVC.SystemShutdown()
                return -1
            img = self.x1.GetImage()        # 获取图像
            pm = self.x1.GetPointMap()      # 获取三维点云数据

        # 创建数据保存目录
        save_address = "CameraData"         # 数据保存目录
        TryCreateDir(save_address)
        save_address += "/" + self.info.sn  # 数据保存目录/设备型号
        TryCreateDir(save_address)
        if mode == 0:
            save_address += "/x1-l"         # x1表示单目采集的数据
        elif mode == 1:
            save_address += "/x1-r"         # x1表示单目采集的数据
        else:
            save_address += "/x2"           # x1表示单目采集的数据
        TryCreateDir(save_address)


        pm.Save(save_address + "/pointmap.ply", RVC.PointMapUnitEnum.Millimeter, True)
        pm.SaveWithImage(save_address + "/pointmap_color.ply", img, RVC.PointMapUnitEnum.Millimeter, True)
        img.SaveImage(save_address + "/image.png")

        # numpy extension
        img_np = np.array(img, copy=False)
        pm_np = np.array(pm, copy=False).reshape(-1, 3)
        size = img_np.size

        return 1

    def check_args(self):
        if self.mode != 2:
            # Modify Capture Options and Capture
            options = RVC.X1_CaptureOptions()

            # Print Capture Options
            print("打印拍摄参数")

            str_capture_mode = ""
            if options.capture_mode == RVC.CaptureMode_Fast:
                str_capture_mode = "快速模式"
            elif options.capture_mode == RVC.CaptureMode_Normal:
                str_capture_mode = "标准模式"
            elif options.capture_mode == RVC.CaptureMode_Robust:
                str_capture_mode = "抗干扰模式"
            elif options.capture_mode == RVC.CaptureMode_Ultra:
                str_capture_mode = "高精度模式"
            print("拍摄模式--[capture_mode] = " + str_capture_mode)

            print("2D 曝光时间--[exposure_time_2d] = " + str(options.exposure_time_2d))
            print("2D 增益--[gain_2d] = " + str(options.gain_2d))
            print("2D Gamma--[gamma_2d] = " + str(options.gamma_2d))
            print("2D 拍摄是否使用光机--[use_projector_capturing_2d_image] = " + str(
                options.use_projector_capturing_2d_image))
            print("3D 曝光时间--[exposure_time_3d] = " + str(options.exposure_time_3d))
            print("3D 增益--[gain_3d] = " + str(options.gain_3d))
            print("3D Gamma--[gamma_3d] = " + str(options.gamma_3d))
            print("光强对比度阈值--[light_contrast_threshold] = " + str(options.light_contrast_threshold))
            print("投影亮度--[projector_brightness] = " + str(options.projector_brightness))

            print("HDR 次数--[hdr_exposure_times] = " + str(options.hdr_exposure_times))
            print("HDR 曝光(0,1,2)--[hdr_exposuretime_content_0] = " + str(options.GetHDRExposureTimeContent(0)))
            print("HDR 曝光(0,1,2)--[hdr_exposuretime_content_1] = " + str(options.GetHDRExposureTimeContent(1)))
            print("HDR 曝光(0,1,2)--[hdr_exposuretime_content_2] = " + str(options.GetHDRExposureTimeContent(2)))

            print("HDR 增益(0,1,2)--[hdr_hdr_gain_3d_0] = " + str(options.GetHDRGainContent(0)))
            print("HDR 增益(0,1,2)--[hdr_hdr_gain_3d_1] = " + str(options.GetHDRGainContent(1)))
            print("HDR 增益(0,1,2)--[hdr_hdr_gain_3d_2] = " + str(options.GetHDRGainContent(2)))

            print("HDR 扫描次数(0,1,2)--[hdr_scan_times_0] = " + str(options.GetHDRScanTimesContent(0)))
            print("HDR 扫描次数(0,1,2)--[hdr_scan_times_1] = " + str(options.GetHDRScanTimesContent(1)))
            print("HDR 扫描次数(0,1,2)--[hdr_scan_times_2] = " + str(options.GetHDRScanTimesContent(2)))

            print("HDR 投影亮度(0,1,2)--[hdr_projector_brightness_0] = " + str(options.GetHDRProjectorBrightnessContent(0)))
            print("HDR 投影亮度(0,1,2)--[hdr_projector_brightness_1] = " + str(options.GetHDRProjectorBrightnessContent(1)))
            print("HDR 投影亮度(0,1,2)--[hdr_projector_brightness_2] = " + str(options.GetHDRProjectorBrightnessContent(2)))

            print("置信度去噪阈值--[confidence_threshold] =" + str(options.confidence_threshold))
            print("聚类降噪距离阈值--[noise_removal_distance] =" + str(options.noise_removal_distance))
            print("聚类降噪有效点数阈值--[noise_removal_point_number] =" + str(options.noise_removal_point_number))
            str_smoothness = ""
            if options.smoothness == RVC.SmoothnessLevel_Off:
                str_smoothness = "关"
            elif options.smoothness == RVC.SmoothnessLevel_Weak:
                str_smoothness = "弱"
            elif options.smoothness == RVC.SmoothnessLevel_Normal:
                str_smoothness = "中"
            elif options.smoothness == RVC.SmoothnessLevel_Strong:
                str_smoothness = "强"
            print("平滑等级--[smoothness] =" + str(options.smoothness))
            print("下采样距离(m)--[downsample_distance] =" + str(options.downsample_distance))
            print("是否计算法向量--[calc_normal] =" + str(options.calc_normal))
            print("计算法向量距离--[calc_normal_radius] =" + str(options.calc_normal_radius))

            print("ROI(x,y,w,h)--[roi_x] =" + str(options.roi.x))
            print("ROI(x,y,w,h)--[roi_y] =" + str(options.roi.y))
            print("ROI(x,y,w,h)--[roi_w] =" + str(options.roi.width))
            print("ROI(x,y,w,h)--[roi_h] =" + str(options.roi.height))

            # G系列相机，扫描次数
            print("扫描次数[G系列相机]--[scan_times] =" + str(options.scan_times))

            # 新增算法参数，双边滤波
            print("z向截断最小值--[truncate_z_min] =" + str(options.truncate_z_min))
            print("z向截断最大值--[truncate_z_max] =" + str(options.truncate_z_max))
            print("双边滤波窗口大小--[bilateral_filter_kernal_size] =" + str(options.bilateral_filter_kernal_size))
            print("双边滤波深度分布--[bilateral_filter_depth_sigma] =" + str(options.bilateral_filter_depth_sigma))
            print("双边滤波空间分布--[bilateral_filter_space_sigma] =" + str(options.bilateral_filter_space_sigma))

            # Method 1, use default options and modify options
            # options = RVC.X1_CaptureOptions()
            # todo:modify options
            # ret = x1.Capture(options)

            # Method 2, load Options From Camera and modify options
            # ret,options = x1.LoadCaptureOptionParameters()
            # todo:modify options
            # ret = x1.Capture(options)

            # *********
            # Method 3, use the internal parameters of the camera.
            # We suggest adjusting the camera parameters By RVC Manager.
            # Then, when we use SDK, we directly use the parameters inside the camera.
            ret = self.x1.Capture()

            # Method 4 , Load Options From File and Capture.
            # If you need to capture multiple scenes, their parameters are different.
            # You can save these parameters as different configuration files  By RVC Manager and then import the files before capture.
            # ret = x1.LoadSettingFromFile("file.json")
            # ret = x1.Capture()

            if ret:
                print("RVC X Camera capture successed!")
            else:
                print("RVC X Camera capture failed!")
                print(RVC.GetLastErrorMessage())
                self.x1.Close()
                RVC.X1.Destroy(self.x1)
                RVC.SystemShutdown()
                return -1
        else:
            # Modify Capture Options and Capture
            options = RVC.X2_CaptureOptions()

            # Print Capture Options
            print("打印拍摄参数")

            str_capture_mode = ""
            if options.capture_mode == RVC.CaptureMode_Fast:
                str_capture_mode = "快速模式"
            elif options.capture_mode == RVC.CaptureMode_Normal:
                str_capture_mode = "标准模式"
            elif options.capture_mode == RVC.CaptureMode_Robust:
                str_capture_mode = "抗干扰模式"
            elif options.capture_mode == RVC.CaptureMode_Ultra:
                str_capture_mode = "高精度模式"
            print("拍摄模式--[capture_mode] = " + str_capture_mode)

            print("2D 曝光时间--[exposure_time_2d] = " + str(options.exposure_time_2d))
            print("2D 增益--[gain_2d] = " + str(options.gain_2d))
            print("2D Gamma--[gamma_2d] = " + str(options.gamma_2d))
            print("2D 拍摄是否使用光机--[use_projector_capturing_2d_image] = " + str(
                options.use_projector_capturing_2d_image))
            print("3D 曝光时间--[exposure_time_3d] = " + str(options.exposure_time_3d))
            print("3D 增益--[gain_3d] = " + str(options.gain_3d))
            print("3D Gamma--[gamma_3d] = " + str(options.gamma_3d))
            print("光强对比度阈值--[light_contrast_threshold] = " + str(options.light_contrast_threshold))
            print("投影亮度--[projector_brightness] = " + str(options.projector_brightness))

            print("HDR 次数--[hdr_exposure_times] = " + str(options.hdr_exposure_times))
            print("HDR 曝光(0,1,2)--[hdr_exposuretime_content_0] = " + str(options.GetHDRExposureTimeContent(0)))
            print("HDR 曝光(0,1,2)--[hdr_exposuretime_content_1] = " + str(options.GetHDRExposureTimeContent(1)))
            print("HDR 曝光(0,1,2)--[hdr_exposuretime_content_2] = " + str(options.GetHDRExposureTimeContent(2)))

            print("HDR 增益(0,1,2)--[hdr_hdr_gain_3d_0] = " + str(options.GetHDRGainContent(0)))
            print("HDR 增益(0,1,2)--[hdr_hdr_gain_3d_1] = " + str(options.GetHDRGainContent(1)))
            print("HDR 增益(0,1,2)--[hdr_hdr_gain_3d_2] = " + str(options.GetHDRGainContent(2)))

            print("HDR 投影亮度(0,1,2)--[hdr_projector_brightness_0] = " + str(
                options.GetHDRProjectorBrightnessContent(0)))
            print("HDR 投影亮度(0,1,2)--[hdr_projector_brightness_1] = " + str(
                options.GetHDRProjectorBrightnessContent(1)))
            print("HDR 投影亮度(0,1,2)--[hdr_projector_brightness_2] = " + str(
                options.GetHDRProjectorBrightnessContent(2)))

            print("置信度去噪阈值--[confidence_threshold] =" + str(options.confidence_threshold))
            print("聚类降噪距离阈值--[noise_removal_distance] =" + str(options.noise_removal_distance))
            print("聚类降噪有效点数阈值--[noise_removal_point_number] =" + str(options.noise_removal_point_number))
            str_smoothness = ""
            if options.smoothness == RVC.SmoothnessLevel_Off:
                str_smoothness = "关"
            elif options.smoothness == RVC.SmoothnessLevel_Weak:
                str_smoothness = "弱"
            elif options.smoothness == RVC.SmoothnessLevel_Normal:
                str_smoothness = "中"
            elif options.smoothness == RVC.SmoothnessLevel_Strong:
                str_smoothness = "强"
            print("平滑等级--[smoothness] =" + str(options.smoothness))
            print("下采样距离(m)--[downsample_distance] =" + str(options.downsample_distance))
            print("是否计算法向量--[calc_normal] =" + str(options.calc_normal))
            print("计算法向量距离--[calc_normal_radius] =" + str(options.calc_normal_radius))

            print("边缘去噪--[edge_noise_reduction_threshold] =" + str(options.edge_noise_reduction_threshold))

            # Method 1, use default options and modify options
            # options = RVC.X2_CaptureOptions()
            # todo:modify options
            # ret = x2.Capture(options)

            # Method 2, load Options From Camera and modify options
            # ret,options = x2.LoadCaptureOptionParameters()
            # todo:modify options
            # ret = x2.Capture(options)

            # *********
            # Method 3, use the internal parameters of the camera.
            # We suggest adjusting the camera parameters By RVC Manager.
            # Then, when we use SDK, we directly use the parameters inside the camera.
            ret = self.x2.Capture()

            # Method 4 , Load Options From File and Capture.
            # If you need to capture multiple scenes, their parameters are different.
            # You can save these parameters as different configuration files  By RVC Manager and then import the files before capture.
            # ret = x2.LoadSettingFromFile("file.json")
            # ret = x2.Capture()

            if ret:
                print("RVC X Camera capture successed!")
            else:
                print("RVC X Camera capture failed!")
                print(RVC.GetLastErrorMessage())
                self.x2.Close()
                RVC.X2.Destroy(self.x2)
                RVC.SystemShutdown()
                return -1

    def close(self):
        '''
        关闭双目
        :return:
        '''
        if self.mode == 2:
            self.x2.Close()
            RVC.X2.Destroy(self.x2)
            RVC.SystemShutdown()
        else:
            self.x1.Close()  # 关闭对象
            RVC.X1.Destroy(self.x1)  # 销毁对象
            RVC.SystemShutdown()  # 系统关机


if __name__ == "__main__":
    obj = Camera()
    obj.connect()
    obj.capture(1)
    obj.close()
