import os
import numpy as np
import matplotlib.pyplot as plt
import cv2


def AdjustGamma(img, gamma=1.0):
    """
    adjust image brightness by gamma value
    """
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0)**invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")

    return cv2.LUT(img, table)


def CreateCircleObjs(m_type='A4'):
    if m_type == 'A2':
        length = 0.08
    elif m_type == 'A3':
        length = 0.056
    elif m_type == 'A4':
        length = 0.04
    elif m_type == 'A5':
        length = 0.028
    elif m_type == 'A6':
        length = 0.02
    elif m_type == 'A7':
        length = 0.014
    elif m_type == 'A8':
        length = 0.01
    elif m_type == 'A9':
        length = 0.007
    elif m_type == 'A10':
        length = 0.0048
    else:
        length = 0.04

    pattern_rows = 4
    pattern_cols = 11

    objp = np.zeros((pattern_cols*pattern_rows, 3))
    for i in range(pattern_cols):
        for j in range(pattern_rows):
            objp[pattern_rows * i + j] = (i * length / 2,
                                          length * j + 0.5 * length * (i % 2), 0)

    return objp


def DetectCVCircle(frame):
    """
    Detect circle center in 2D image
    """

    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.filterByCircularity = True
    params.filterByConvexity = False
    params.filterByInertia = True
    params.filterByColor = True
    params.minArea = 100
    params.maxArea = 10000
    params.minCircularity = 0.6
    params.minInertiaRatio = 0.01
    params.minRepeatability = 6
    params.minDistBetweenBlobs = 1

    params.minThreshold = 10
    params.maxThreshold = 250
    params.thresholdStep = 3
    params.blobColor = 255

    detector = cv2.SimpleBlobDetector_create(params)

    frame_show = frame.copy()
    pattern_rows = 4
    pattern_cols = 11

    ret, pts = cv2.findCirclesGrid(frame_show, (pattern_rows, pattern_cols),
                                   flags=(cv2.CALIB_CB_ASYMMETRIC_GRID),
                                   blobDetector=detector)
    cv2.drawChessboardCorners(
        frame_show, (pattern_rows, pattern_cols), pts, pts is not None)
    '''
    # You can enable code below to show detected pattern
    # If detect pattern failed, please adjust detect params above or adjust gamma.
    # For Details please see OpenCV documentation



    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.imshow('image', frame_show)
    cv2.waitKey(-1)
    cv2.destroyAllWindows()
    '''
    save_dir = "Data"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    cv2.imwrite("{}/detect.png".format(save_dir), frame_show)

    return ret, pts


def CentersPcd(centers, pcd, img):
    """
    Locate circle centers in point cloud
    """
    index = []
    centers_pcd = []

    for i in range(len(centers)):
        if (centers[i, 0] - int(centers[i, 0]) > 0.5
                and centers[i, 0] + 0.5 < img.shape[1]) or centers[i, 0] < 0.5:
            x1 = int(centers[i, 0])
            x2 = int(centers[i, 0] + 1)
        else:
            x1 = int(centers[i, 0] - 1)
            x2 = int(centers[i, 0])
        if (centers[i, 1] - int(centers[i, 1]) > 0.5
                and centers[i, 1] + 0.5 < img.shape[0]) or centers[i, 1] < 0.5:
            y1 = int(centers[i, 1])
            y2 = int(centers[i, 1] + 1)
        else:
            y1 = int(centers[i, 1] - 1)
            y2 = int(centers[i, 1])
        index_bilinear = []
        index_bilinear.append(y1 * img.shape[1] + x1)
        index_bilinear.append(y1 * img.shape[1] + x2)
        index_bilinear.append(y2 * img.shape[1] + x1)
        index_bilinear.append(y2 * img.shape[1] + x2)
        index_bilinear.append(centers[i, 0] - x1)
        index_bilinear.append(centers[i, 1] - y1)

        index.append(index_bilinear)
    # for i in range(index.shape[0] - 1):
    for i in range(len(index)):
        each_pattern_idx = index[i]
        upper_left_point = pcd[int(each_pattern_idx[0])]
        upper_right_point = pcd[int(each_pattern_idx[1])]
        lower_left_point = pcd[int(each_pattern_idx[2])]
        lower_right_point = pcd[int(each_pattern_idx[3])]
        weight_x = each_pattern_idx[4]
        weight_y = each_pattern_idx[5]
        bilinear_val = upper_left_point * (1 - weight_x) * (1 - weight_y) + \
            upper_right_point * weight_x * (1 - weight_y) + \
            lower_left_point * (1 - weight_x) * weight_y + \
            lower_right_point * weight_x * weight_y
        centers_pcd.append(bilinear_val.tolist())
    centers_pcd = np.array(centers_pcd)
    return centers_pcd


def FindRigidTransform(A, B):
    """
    Find rigid transform between two corrsponding point set
    """
    if len(A) != len(B) or len(A) < 3:
        return None, None

    N = A.shape[0]  # total points

    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)

    AA = A - np.tile(centroid_A, (N, 1))
    BB = B - np.tile(centroid_B, (N, 1))

    H = np.matmul(np.transpose(AA), BB)

    U, S, Vt = np.linalg.svd(H)

    R = np.matmul(Vt.T, U.T)

    if np.linalg.det(R) < 0:
        print("Reflection detected")
        Vt[2, :] *= -1
        R = np.matmul(Vt.T, U.T)

    T = -np.matmul(R, centroid_A) + centroid_B

    return R, T


def Transformation(points, transform):
    """ 

    Transform points 

    """
    points = np.concatenate((points, np.ones(len(points)).reshape(-1, 1)),
                            axis=1)

    points_ = transform.dot(points.T).T

    return points_[:, :3]


def Visualization(pcd, T):
    from RVBUST import Vis
    view = Vis.View('View')
    view.Point(pcd.flatten(), 1, (0.4, 0.4, 0.4))
    view.Axes(T.flatten(), 1, 1)  # rgb represents x,y,z
    input('Wait')


def GetCaliBoardPose(img, pcd, gamma=2.5, m_type='A4'):
    """
    Get Cali board pose
    """

    img = AdjustGamma(img, gamma)
    ret, centers = DetectCVCircle(img)
    if not ret:
        print("detect cali board failed, please adjust gamma or exposure time")
        return None

    centers_ = np.reshape(centers, (-1, 2))
    centers_pcd = CentersPcd(centers_, pcd, img)

    obj_ref = CreateCircleObjs(m_type)
    # Remove Nan in point clouds
    centers_pcd_ = centers_pcd[~np.isnan(centers_pcd[:, 0])]
    obj_ref_ = obj_ref[~np.isnan(centers_pcd[:, 0])]
    print("{} points used to calculate transformation".format(
        centers_pcd_.shape[0]))

    # T_3d is the caliborad pose based on camera coordinate
    T_3d = np.eye(4)
    R, t = FindRigidTransform(obj_ref_,
                              centers_pcd_)
    if R is None:
        print("detect cali board failed, not enough valid point. please adjust cali board position")
        return None
    T_3d[:3, :3] = R
    T_3d[:3, 3] = t

    # Transform the point cloud to cali board coordinate
    point_in_caliboard_coordinate = Transformation(pcd, np.linalg.inv(T_3d))

    '''
    # You can enable code below for visualization.

    Visualization(pcd, T_3d)

    '''
    return T_3d


def CalcAccuracy(img, pcd, gamma=2.5, m_type='A4'):

    img = AdjustGamma(img, gamma)
    ret, centers = DetectCVCircle(img)
    if not ret:
        print("detect cali board failed, please adjust gamma or exposure time")
        return False, None

    centers_ = np.reshape(centers, (-1, 2))
    centers_pcd = CentersPcd(centers_, pcd, img)

    obj_ref  = CreateCircleObjs(m_type)
    true_distance = np.linalg.norm(obj_ref[1] - obj_ref[0]) 

    """ 
    Select circle centers to calculate euclidean distance. As an example, 
    * The calibration board we use is a 4x11 pattern(4 rows and 11 columns).
    * The variable target_center_ids given below represents the corresponding id of that
        center, so that we can calculate the farthest distance between the four pairs of
        centers. For example. [1, 41] means distance between the first circle center of the first row.
        and the last circle center of the first row.
    
    Variables : 
    * target_center_ids : circle center id pairs to calculate distance. 
    * target_center_length : actual length between target centers.
    """
    target_center_ids = [[0, 40], [1, 41], [2, 42], [3, 43]]
    target_center_length = true_distance * 5
    estimated_distance = np.asarray([np.linalg.norm(
            centers_pcd[center_ids[0]] - centers_pcd[center_ids[1]]) for center_ids in target_center_ids])
    error_meter = estimated_distance - target_center_length
    error_mm = error_meter * 1000

    return True, error_mm


def PlotError(err_list):

    if 0 == len(err_list):
        print("no data!")
        return

    m_x = np.arange(0, len(err_list))
    m_y = np.asarray(err_list)
    ave_err = np.round(np.mean(m_y), 4)
    print("average error: {} mm".format(ave_err))

    plt.plot(m_x, m_y, label="ave_err/" + str(ave_err), color='r')

    for j in range(len(err_list)):
        m_x_ = np.array([m_x[j], m_x[j]]).astype(dtype=str)
        m_y_ = np.array([0, m_y[j]])
        plt.plot(m_x_, m_y_, linestyle=":")

    plt.legend(loc='upper right', fontsize=10)
    plt.xlim([0, np.max(m_x)])

    plt.xlabel("num", fontsize=20)
    plt.ylabel("err [mm]", fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    plt.show()


if __name__ == "__main__":
    import open3d as o3d
    from IPython import embed

    w, h = 1920, 1200
    pattern_type = "A5"

    # pointcloud should save in unit m with color
    pcd_o3d = o3d.io.read_point_cloud(
        "/home/rvbust/Downloads/pointcloud.ply", remove_nan_points=False)
    pm_m = np.asarray(pcd_o3d.points)
    if pm_m.shape[0] != w * h:
        print(f"wrong size, wh=({w}, {h}), pm_m.shape={pm_m.shape}")
    image = (np.asarray(
        pcd_o3d.colors) * 255).reshape((h, w, 3)).astype(np.uint8)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, error_list_mm = CalcAccuracy(image,
                                      pm_m,
                                      gamma=1,
                                      m_type=pattern_type)
    print(f"error_list_mm: {error_list_mm}")
    print(
        f"mean error (mm): {np.mean(error_list_mm)}, max error (mm): {np.max(error_list_mm)}")
    embed()
