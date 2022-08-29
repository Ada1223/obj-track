from collections import  deque  
import numpy as np  
#import imutils  
import cv2  
import time
import csv
import pandas as pd

# VideoCapture方法是cv2库提供的读取视频方法

#设定红色阈值，HSV空间
redLower = np.array([170, 100, 100])  
redUpper = np.array([179, 255, 255])
yellowLower = np.array([26, 43, 46])
yellowUpper = np.array([34, 255, 255])
blueLower = np.array([100,43,46])
blueUpper = np.array([124,255,255])
#初始化追踪点的列表  
#mybuffer = 64
#pts = deque(maxlen=mybuffer)
pts1 = deque()
pts2 = deque()
#打开摄像头  
#camera = cv2.VideoCapture(0)  
video = cv2.VideoCapture('/usr/project/obj-track/test@0815/aftcut/old1.mp4')
#定义保存视频的参数
   # 设置需要保存视频的格式“MP4” 
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # 设置视频帧频
fps = video.get(cv2.CAP_PROP_FPS)
    # 设置视频大小
size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
#输出视频
out = cv2.VideoWriter('out.mp4',fourcc,fps,size) 
#等待两秒  
time.sleep(2)  
#遍历每一帧，检测红色标记  
while True:  
    #读取帧  
    (ret, frame) = video.read()  
    #判断是否成功打开摄像头  
     
    #frame = imutils.resize(frame, width=600)  
    #转到HSV空间  
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  
    #根据阈值构建掩膜  
    mask3 = cv2.inRange(hsv, redLower, redUpper)
    mask2 = cv2.inRange(hsv, yellowLower, yellowUpper)
    mask1 = cv2.inRange(hsv,blueLower,blueUpper)
    #腐蚀操作  
    mask1 = cv2.erode(mask1, None, iterations=2)
    mask2 = cv2.erode(mask2, None, iterations=2)
    mask3 = cv2.erode(mask3, None, iterations=2)
    #膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点  
    mask1 = cv2.dilate(mask1, None, iterations=2)
    mask2 = cv2.dilate(mask2, None, iterations=2)
    mask3 = cv2.dilate(mask3, None, iterations=2)
    #轮廓检测  
    cnts1 = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnts2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnts3 = cv2.findContours(mask3.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    #初始化瓶盖圆形轮廓质心  
    center1 = None
    center2 = None
    center3 = None
    #如果存在轮廓  
    if len(cnts1) > 0:
        #找到面积最大的轮廓  
        c1 = max(cnts1, key = cv2.contourArea)
        c2 = max(cnts2, key=cv2.contourArea)
        #确定面积最大的轮廓的外接圆  
        ((x1, y1),radius) = cv2.minEnclosingCircle(c1)
        ((x2, y2), radius) = cv2.minEnclosingCircle(c2)
        
        #计算轮廓的矩  
        M1 = cv2.moments(c1)
        M2 = cv2.moments(c2)
        #计算质心1
        center1 = (int(M1["m10"]/M1["m00"]), int(M1["m01"]/M1["m00"]))
        center2 = (int(M2["m10"] / M2["m00"]), int(M2["m01"] / M2["m00"]))
        # 计算最小外接矩形1
        rotatedRect1 = cv2.minAreaRect(c1)
        box1 = cv2.boxPoints(rotatedRect1)
        box10 = box1[0]
        box11 = box1[1]
        box12 = box1[2]
        box13 = box1[3]
        # 计算最小外接矩形2
        rotatedRect2 = cv2.minAreaRect(c2)
        box2 = cv2.boxPoints(rotatedRect2)
        box20 = box2[0]
        box21 = box2[1]
        box22 = box2[2]
        box23 = box2[3]
        continue

        #print(box)
        #只有当半径大于10时，才执行画图  
        if radius > 10:
            #cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.rectangle(frame,(int(box13[0]),int(box13[1])),(int(box11[0]),int(box11[1])),(255,0,255),2)
            cv2.circle(frame, center1, 1, (0, 0, 255), -1)
            cv2.rectangle(frame, (int(box23[0]), int(box23[1])), (int(box21[0]), int(box21[1])), (255, 0, 255), 2)
            cv2.circle(frame, center2, 1, (0, 0, 255), -1)
            #把质心添加到pts中，并且是添加到列表左侧  
            pts1.appendleft(center1)
            pts2.appendleft(center2)
            continue
    #遍历追踪点，分段画出轨迹  
    for i in range(1, len(pts1)), j in range(1, len(pts2)):
        #计算所画小线段的粗细  
        #thickness = int(np.sqrt(mybuffer / float(i + 1)) * 2.5)
        thickness = 2
        #画出小线段
        cv2.line(frame, pts1[i - 1], pts1[i], (0, 255, 0), thickness)
        cv2.line(frame, pts2[j - 1], pts2[j], (0, 255, 0), thickness)
        #存储center中心点的值
        f1 = open('box1.csv', 'w', encoding='utf-8', newline="")
        csv_write = csv.writer(f1)
        csv_write.writerow(box1)
        d = pd.DataFrame(pts1)
        d.to_csv('center1.csv', index=False, mode='w', header=None)  # mode表示追加 在追加时会将列名也作为一行进行追加，故header隐藏表头（列名）
        # 存储center中心点的值
        f2 = open('box2.csv', 'w', encoding='utf-8', newline="")
        csv_write = csv.writer(f2)
        csv_write.writerow(box2)
    d = pd.DataFrame(pts2)
    d.to_csv('center2.csv', index=False, mode='w', header=None)

    if ret == True:

        # 5.将每一帧图像写入到输出文件中
        out.write(frame)  #视频写入
    else:
        break
    #键盘检测，检测到esc键退出
    k = cv2.waitKey(5)&0xFF
    if k == 27:
        break

f.close
#摄像头释放  
video.release()
out.release()  
#销毁所有窗口  
cv2.destroyAllWindows() 
