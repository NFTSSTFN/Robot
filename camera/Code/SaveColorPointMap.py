# Copyright (c) RVBUST, Inc - All rights reserved.
import PyRVC as RVC
import os
import numpy as np
import cv2
from Utils.Tools import *


def App():

    # Initialize RVC X system.
    RVC.SystemInit()

    # Choose RVC X Camera type (USB, GigE or All)
    opt = RVC.SystemListDeviceTypeEnum.All

    # Scan all RVC X Camera devices.
    ret, devices = RVC.SystemListDevices(opt)
    print("RVC X Camera devices number:%d" % len(devices))

    # Find whether any RVC X Camera is connected or not.
    if len(devices) == 0:
        print("Can not find any RVC X Camera!")
        RVC.SystemShutdown()
        return 1
    print("devices size = %d" % len(devices))

    # Create a RVC X Camera and choose use left side camera.
    x = RVC.X1.Create(devices[0], RVC.CameraID_Left)

    # Test RVC X Camera is valid or not.
    if x.IsValid() == True:
        print("RVC X Camera is valid!")
    else:
        print("RVC X Camera is not valid!")
        RVC.X1.Destroy(x)
        RVC.SystemShutdown()
        return 1
    
    #PrintCaptureMode(devices[0])

    # Open RVC X Camera.
    ret1 = x.Open()

    # Test RVC X Camera is opened or not.
    if ret1 and x.IsOpen() == True:
        print("RVC X Camera is opened!")
    else:
        print("RVC X Camera is not opened!")
        RVC.X1.Destroy(x)
        RVC.SystemShutdown()
        return 1
    
    # Print ExposureTime Range
    _, exp_range_min, exp_range_max = x.GetExposureTimeRange()
    print("ExposureTime Range:[{}, {}]".format(exp_range_min, exp_range_max))

    # Capture a point map and a image.
    ret2 = x.Capture()

    # Create saving address of image and point map.
    save_address = "Data"
    TryCreateDir(save_address)

    if ret2 == True:
        print("RVC X Camera capture successed!")

        # Get image data.
        image = x.GetImage()

        # Get point map data (m).
        pm = x.GetPointMap()
        pm_path = "Data/test.ply"
        pm.SaveWithImage(pm_path, image, RVC.PointMapUnitEnum.Millimeter)
        print("save color point map to file:%s" % pm_path)
    else:
        print("RVC X Camera capture failed!")
        print(RVC.GetLastErrorMessage())
        x.Close()
        RVC.X1.Destroy(x)
        RVC.SystemShutdown()
        return 1

    # Close RVC X Camera.
    x.Close()

    # Destroy RVC X Camera.
    RVC.X1.Destroy(x)

    # Shutdown RVC X System.
    RVC.SystemShutdown()

    return 0


if __name__ == "__main__":
    App()
