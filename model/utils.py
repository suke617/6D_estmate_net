import math
import numpy as np
from math import cos, sin
import cv2
# クォータニオンからオイラー角に変換する関数
def quat_to_euler(q):
    q=q[0]
    print(q)
    # q = [w, x, y, z]
    roll = math.atan2(2*(q[0]*q[1] + q[2]*q[3]), 1 - 2*(q[1]**2 + q[2]**2))
    pitch = math.asin(2*(q[0]*q[2] - q[3]*q[1]))
    yaw = math.atan2(2*(q[0]*q[3] + q[1]*q[2]), 1 - 2*(q[2]**2 + q[3]**2))
    return [math.degrees(roll), math.degrees(pitch), math.degrees(yaw)]

# オイラー角からクォータニオンに変換する関数
def euler_to_quat(euler):
    # euler = [roll, pitch, yaw]
    roll = math.radians(euler[0])
    pitch = math.radians(euler[1])
    yaw = math.radians(euler[2])
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    q = np.zeros(4)
    q[0] = cy * cr * cp + sy * sr * sp
    q[1] = cy * sr * cp - sy * cr * sp
    q[2] = cy * cr * sp + sy * sr * cp
    q[3] = sy * cr * cp - cy * sr * sp
    return q



def draw_axis(img, euler, tdx=None, tdy=None, size = 100):
    yaw, pitch, roll= euler
    print(yaw, pitch, roll)
    pitch = pitch * np.pi / 180
    yaw = -(yaw * np.pi / 180)
    roll = roll * np.pi / 180

    if tdx != None and tdy != None:
        tdx = tdx
        tdy = tdy
    else:
        height, width = img.shape[:2]
        tdx = width / 2
        tdy = height / 2

    # X-Axis pointing to right. drawn in red
    x1 = size * (cos(yaw) * cos(roll)) + tdx
    y1 = size * (cos(pitch) * sin(roll) + cos(roll) * sin(pitch) * sin(yaw)) + tdy

    # Y-Axis | drawn in green
    #        v
    x2 = size * (-cos(yaw) * sin(roll)) + tdx
    y2 = size * (cos(pitch) * cos(roll) - sin(pitch) * sin(yaw) * sin(roll)) + tdy

    # Z-Axis (out of the screen) drawn in blue
    x3 = size * (sin(yaw)) + tdx
    y3 = size * (-cos(yaw) * sin(pitch)) + tdy

    cv2.line(img, (int(tdx), int(tdy)), (int(x1),int(y1)),(0,0,255),4)
    cv2.line(img, (int(tdx), int(tdy)), (int(x2),int(y2)),(0,255,0),4)
    cv2.line(img, (int(tdx), int(tdy)), (int(x3),int(y3)),(255,0,0),4)
    return img