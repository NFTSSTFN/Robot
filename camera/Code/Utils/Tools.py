import PyRVC as RVC
import os

# Create a directory.color
def TryCreateDir(d):
    if not os.path.exists(d):
        os.makedirs(d)


def SavePointMapWithNormal(pm, normal, p_sz, save_path):
    with open(save_path, "w") as f:
        f.write("{}".format("ply"))
        f.write("\n{}".format("format ascii 1.0"))
        f.write("\n{}".format("comment Created by Rvbust, Inc"))
        f.write("\nelement vertex {}".format(p_sz))
        f.write("\n{}".format("property float x"))
        f.write("\n{}".format("property float y"))
        f.write("\n{}".format("property float z"))
        f.write("\n{}".format("property float nx"))
        f.write("\n{}".format("property float ny"))
        f.write("\n{}".format("property float nz"))
        f.write("\n{}\n".format("end_header"))
        for i in range(p_sz):
            f.write(
                "{} {} {} {} {} {}\n".format(
                    pm[i, 0],
                    pm[i, 1],
                    pm[i, 2],
                    normal[i, 0],
                    normal[i, 1],
                    normal[i, 2],
                )
            )
    f.close()
    return


def SavePointMap(pm, p_sz, save_path):
    with open(save_path, "w") as f:
        f.write("{}".format("ply"))
        f.write("\n{}".format("format ascii 1.0"))
        f.write("\n{}".format("comment Created by Rvbust, Inc"))
        f.write("\nelement vertex {}".format(p_sz))
        f.write("\n{}".format("property float x"))
        f.write("\n{}".format("property float y"))
        f.write("\n{}".format("property float z"))
        f.write("\n{}\n".format("end_header"))
        for i in range(p_sz):
            f.write("{} {} {}\n".format(pm[i, 0], pm[i, 1], pm[i, 2]))
    f.close()
    return


# Save PointMap to pm_path.
def SavePlyFile(pm_path, pm, image):
    width = pm.GetSize().width
    height = pm.GetSize().height
    pm_num = width * height
    pm_ptr = np.array(pm, copy=False).reshape((-1, 3))
    image_ptr = np.array(image, copy=False)
    if image.GetType() == RVC.ImageTypeEnum.Mono8:
        tmp = image_ptr.copy().flatten()
        image_ptr = np.zeros((height * width, 3))
        image_ptr[:, 0] = tmp
        image_ptr[:, 1] = tmp
        image_ptr[:, 2] = tmp
    else:
        image_ptr = image_ptr.reshape(-1, 3)
        if image.GetType() == RVC.ImageTypeEnum.BGR8:
            image_ptr[:, [0, 2]] = image_ptr[:, [2, 0]]
    data = np.concatenate((pm_ptr, image_ptr), axis=1)
    np.savetxt(pm_path, data, fmt="%f %f %f %d %d %d")
    with open(pm_path, "r+") as f:
        old = f.read()
        f.seek(0)
        f.write("{}".format("ply"))
        f.write("\n{}".format("format ascii 1.0"))
        f.write("\n{}".format("comment Created by Rvbust, Inc"))
        f.write("\nelement vertex {}".format(pm_num))
        f.write("\n{}".format("property float x"))
        f.write("\n{}".format("property float y"))
        f.write("\n{}".format("property float z"))
        f.write("\n{}".format("property uchar red"))
        f.write("\n{}".format("property uchar green"))
        f.write("\n{}".format("property uchar blue"))
        f.write("\n{}\n".format("end_header"))
        f.write(old)
    f.close()
    return


def PrintCaptureOptionX1(x1):
    print("x1.calc_normal =", x1.calc_normal)
    print("x1.transform_to_camera =", x1.transform_to_camera)
    print("x1.filter_range =", x1.filter_range)
    print("x1.phase_filter_range =", x1.phase_filter_range)
    print("x1.projector_brightness =", x1.projector_brightness)
    print("x1.exposure_time_2d =", x1.exposure_time_2d)
    print("x1.exposure_time_3d =", x1.exposure_time_3d)
    print("x1.gain_2d =", x1.gain_2d)
    print("x1.gain_3d =", x1.gain_3d)
    print("x1.hdr_exposure_times =", x1.hdr_exposure_times)
    print("x1.hdr_exposure_times[1] =", x1.GetHDRExposureTimeContent(1))
    print("x1.hdr_exposure_times[2] =", x1.GetHDRExposureTimeContent(2))
    print("x1.hdr_exposure_times[3] =", x1.GetHDRExposureTimeContent(3))
    print("x1.calc_normal_radius =", x1.calc_normal_radius)
    print("x1.gamma_2d =", x1.gamma_2d)
    print("x1.gamma_3d =", x1.gamma_3d)
    print("x1.use_projector_capturing_2d_image =", x1.use_projector_capturing_2d_image)
    print("x1.smoothness =", x1.smoothness)
    print("x1.downsample_distance =", x1.downsample_distance)


def PrintCaptureOptionX2(x2):
    print("x2.transform_to_camera =", x2.transform_to_camera)
    print("x2.projector_brightness =", x2.projector_brightness)
    print("x2.calc_normal =", x2.calc_normal)
    print("x2.calc_normal_radius =", x2.calc_normal_radius)
    print("x2.light_contrast_threshold =", x2.light_contrast_threshold)
    print("x2.edge_noise_reduction_threshold =", x2.edge_noise_reduction_threshold)
    print("x2.exposure_time_2d =", x2.exposure_time_2d)
    print("x2.exposure_time_3d =", x2.exposure_time_3d)
    print("x2.gain_2d =", x2.gain_2d)
    print("x2.gain_3d =", x2.gain_3d)
    print("x2.hdr_exposure_times =", x2.hdr_exposure_times)
    print("x2.hdr_exposure_times[1] =", x2.GetHDRExposureTimeContent(1))
    print("x2.hdr_exposure_times[2] =", x2.GetHDRExposureTimeContent(2))
    print("x2.hdr_exposure_times[3] =", x2.GetHDRExposureTimeContent(3))
    print("x2.gamma_2d =", x2.gamma_2d)
    print("x2.gamma_3d =", x2.gamma_3d)
    print("x2.projector_color =", x2.projector_color)
    print("x2.use_projector_capturing_2d_image =", x2.use_projector_capturing_2d_image)
    print("x2.smoothness =", x2.smoothness)
    print("x2.downsample_distance =", x2.downsample_distance)


def Truncate(pc, xr=[-5, 5], yr=[-5, 5], zr=[-5, 5]):
    """crop point cloud by range

    Args:
        pc (ndarray): N x 3 point clouds
        xr (list, optional): Defaults to [-5, 5].
        yr (list, optional): Defaults to [-5, 5].
        zr (list, optional): Defaults to [-5, 5].
    """

    def TruncateOne(pc, c, r):
        return np.logical_and(pc[:, c] > r[0], pc[:, c] < r[1])

    xb = TruncateOne(pc, 0, xr)
    yb = TruncateOne(pc, 1, yr)
    zb = TruncateOne(pc, 2, zr)

    return pc[np.logical_and(np.logical_and(xb, yb), zb)]


def RemoveNan(points):
    """remove nan value of point clouds

    Args:
        points (ndarray): N x 3 point clouds

    Returns:
        [ndarray]: N x 3 point clouds
    """
    find_index = ~np.isnan(points[:, 0])

    return points[find_index]
