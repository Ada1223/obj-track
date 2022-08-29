from collections import  deque  
import numpy as np  
#import imutils  
import cv2  
import time
import csv
import pandas as pd
#test git




#设定红色阈值，HSV空间  
redLower = np.array([170, 100, 100])
redUpper = np.array([179, 255, 255])
#初始化追踪点的列表
# 如果保存视频时只想显示64帧的轨迹,取消注释下面两行  
#mybuffer = 64
#pts = deque(maxlen=mybuffer)
#打开摄像头  
#camera = cv2.VideoCapture(0)
# 打开视频

video = cv2.VideoCapture('/usr/project/obj-track/test0824/10cm.mp4')

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

#保存全部轨迹
pts = [deque() for i in range(5)]
while True:  
    #读取帧  
    (ret, frame) = video.read()
    #cv2.imwrite('pic.png', frame[0])
    if not ret:
        print
        'Video is none!'
        break

    #frame = imutils.resize(frame, width=600)  
    #转到HSV空间  
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  
    #根据阈值构建掩膜  
    mask = cv2.inRange(hsv, redLower, redUpper)  
    #腐蚀操作
    mask = cv2.erode(mask, None, iterations=5)
    #膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点  
    mask = cv2.dilate(mask, None, iterations=5)
    #轮廓检测  
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  
    #初始化轮廓质心  
    center = None  
    #如果存在轮廓
    for i in range(len(cnts)):
        if len(cnts[i]) > 10:
            #找到面积最大的轮廓
            c = cnts[i]
            #确定面积最大的轮廓的外接圆
            ((x, y),radius) = cv2.minEnclosingCircle(c)

            #计算轮廓的矩
            M = cv2.moments(c)
            #计算质心
            center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
            rotatedRect = cv2.minAreaRect(c)  # 计算最小外接矩形
            #获取轮廓矩形的四个坐标点
            box = cv2.boxPoints(rotatedRect)
            cv2.rectangle(frame,(int(box[3][0]),int(box[3][1])),(int(box[1][0]),int(box[1][1])),(255,0,255),2)
            #     cv2.circle(frame, center, 1, (0, 0, 255), -1)
            #
            #     #把质心添加到pts中，并且是添加到列表左侧
            # pts[i].appendleft(center)
            if len(pts[i]) == 0:
                pts[i].appendleft(center)
            else:
                MIN = 1000
                N = 1
                for n in range(len(pts)):
                    try:
                        # print(pts[n][0])
                        min = abs(pts[n][0][1] -center[1])
                        # print(min)
                        if min < MIN:
                            MIN = min
                            N = n
                    except:
                        pass
                pts[N].appendleft(center)
        # print(pts[2])
        #遍历追踪点，分段画出轨迹
        for j in range(1, len(pts[i])):
            if pts[i][j - 1] is None or pts[i][j] is None:
                print('y')
                continue
            #计算所画小线段的粗细
            #thickness = int(np.sqrt(mybuffer / float(i + 1)) * 2.5)
            thickness = 2
            #画出小线段
            cv2.line(frame, pts[i][j - 1], pts[i][j], (0, i*50, i*20), thickness)
            #存储矩形坐标的值,后续需要用这个值进行真实尺寸的转化
            f = open('box.csv', 'w', encoding='utf-8', newline="")
            csv_write = csv.writer(f)
            e
            csv_write.writerow(box)

    d = pd.DataFrame(pts)
    d.to_csv('center.csv', index=False, mode='w', header=None)  # mode表示追加 在追加时会将列名也作为一行进行追加，故header隐藏表头（列名）
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow('Frame', frame)
    # if ret == True:
    #     # 将每一帧图像写入到输出文件中
    #     out.write(frame)
    #     print('video is processing')
    # else:
    #     break
    # print('video is done!')
    # #键盘检测，检测到esc键退出
    k = cv2.waitKey(1)&0xFF # the number in waitkey means wait x ms to
    if k == 27:
        break
#文件关闭
f.close
#摄像头释放  
video.release()
out.release()  
#销毁所有窗口
#cv2.waitKey(0)#anykey to stop the project
cv2.destroyAllWindows() 
