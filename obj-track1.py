from collections import  deque  
import numpy as np  
#import imutils  
import cv2  
import time
import csv
import pandas as pd




# VideoCapture方法是cv2库提供的读取视频方法

#设定红色阈值，HSV空间  
redLower = np.array([100, 80, 46])
redUpper = np.array([124, 255, 255])
#yellowLower = np.array([26, 43, 46])
#yellowUpper = np.array([34, 255, 255])
#初始化追踪点的列表  
#mybuffer = 32
#pts = deque(maxlen=mybuffer)
pts = deque()
#打开摄像头  
#camera = cv2.VideoCapture(0)
#avcodec_parameters_to_context(vctx, ifmt->streams[video_index]->codecpar)
#print(args.path)
video = cv2.VideoCapture('./test@0815/old2.mp4')
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
    if not ret:
        print
        'No Camera'
        break
     
    #frame = imutils.resize(frame, width=600)  
    #转到HSV空间  
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  
    #根据阈值构建掩膜  
    mask = cv2.inRange(hsv, redLower, redUpper)  
    #腐蚀操作  
    mask = cv2.erode(mask, None, iterations=2)
    #膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点  
    mask = cv2.dilate(mask, None, iterations=2)
    #轮廓检测  
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  
    #初始化瓶盖圆形轮廓质心  
    center = None  
    #如果存在轮廓  
    if len(cnts) > 0:  
        #找到面积最大的轮廓  
        c = max(cnts, key = cv2.contourArea)  
        #确定面积最大的轮廓的外接圆  
        ((x, y),radius) = cv2.minEnclosingCircle(c)  
        
        #计算轮廓的矩  
        M = cv2.moments(c)  
        #计算质心  
        center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
        rotatedRect = cv2.minAreaRect(c)  # 计算最小外接矩形
        box = cv2.boxPoints(rotatedRect)
        box0 = box[0]
        box1 = box[1]
        box2 = box[2]
        box3 = box[3]

        #print(box)
        #只有当半径大于10时，才执行画图  
        if radius > 10:  
            #cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.rectangle(frame,(int(box3[0]),int(box3[1])),(int(box1[0]),int(box1[1])),(255,0,255),2)
            cv2.circle(frame, center, 1, (0, 0, 255), -1)

            #把质心添加到pts中，并且是添加到列表左侧  
            pts.appendleft(center) 
    #遍历追踪点，分段画出轨迹  
    for i in range(1, len(pts)):  
        if pts[i - 1] is None or pts[i] is None:  
            continue  
        #计算所画小线段的粗细  
        #thickness = int(np.sqrt(mybuffer / float(i + 1)) * 2.5)
        thickness = 2
        #画出小线段  

        #cv2.line(frame, pts[i - 1], pts[i], (0, 255, 0), thickness)
        cv2.line(frame, pts[i - 1], pts[i], (0, 255, 0), thickness)
        #存储center中心点的值
        f = open('box.csv', 'w', encoding='utf-8', newline="")
        
        csv_write = csv.writer(f)
        csv_write.writerow(box)
    d = pd.DataFrame(pts)
    d.to_csv('center2.csv', index=False, mode='w', header=None)  # mode表示追加 在追加时会将列名也作为一行进行追加，故header隐藏表头（列名）
    #res = cv2.bitwise_and(frame, frame, mask=mask)  
    cv2.imshow('Frame', frame)
    if ret == True:

        # 5.将每一帧图像写入到输出文件中
        out.write(frame)  #视频写入
    else:
        break  
    #键盘检测，检测到esc键退出  
    k = cv2.waitKey(5)&0xFF  
    if k == 27:  
        break  
#f.close
#摄像头释放  
video.release()
out.release()  
#销毁所有窗口  
cv2.destroyAllWindows() 
