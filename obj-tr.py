import cv2
import numpy as np

color_dist = {'red': {'Lower': np.array([0, 25, 138]), 'Upper': np.array([19, 255, 255])},
              'light_red': {'Lower': np.array([178, 100, 136]), 'Upper': np.array([255, 255, 255])},
              'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
              'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
              'yellow': {'Lower': np.array([26, 43, 46]), 'Upper': np.array([34, 255, 255])},
              }
#调用摄像头
#cap = cv2.VideoCapture(0)
# 输入视频
cap = cv2.VideoCapture("/usr/project/obj-track/test0822/1.mp4")
cv2.namedWindow('camera', cv2.WINDOW_AUTOSIZE)

while True:
    # 读取视频帧，ret标志读取的结果，frame为读取到的视频帧图像
    ret, frame = cap.read()

    #gs_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    #cv2.imshow('gs_frame', gs_frame)# 高斯模糊
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)                 # 转化成HSV图像
    cv2.imshow('hsv-video',hsv)
    inRange_hsv = cv2.inRange(hsv, color_dist['red']['Lower'], color_dist['red']['Upper'])
    cv2.imshow('inrange_hsv', inRange_hsv)
    #寻找外部的点
    cnts = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    c = max(cnts, key=cv2.contourArea)
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box_list = box.tolist()
    #将点画在
    cv2.drawContours(frame, [np.int0(box)], -1, (0, 255, 255), 2)

    cv2.imshow('camera', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
            
cv2.destroyAllWindows()
