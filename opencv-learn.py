import numpy as np
import matplotlib.pyplot as plt
import cv2

video = cv2.VideoCapture('/usr/project/obj-track/test0822/1.mp4')
while True:
    #读取帧
    (ret, frame) = video.read()
    if not ret:
        print
        'Video is none!'
        break
    #ret,dst =cv2.threshold(src,thresh,maxval,type)
    #src:input img
    #dst:output img
    #thresh:yytyt ret ret  ddddtgni
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret,thresh1 =cv2.threshold(frame,170,179,cv2.THRESH_BINARY)
    ret,thresh2 = cv2.threshold(frame,127,255,cv2.THRESH_BINARY_INV)
    ret,thresh3 = cv2.threshold(frame,127,255,cv2.THRESH_TRUNC)
    ret,thresh4 = cv2.threshold(frame,127,255,cv2.THRESH_TOZERO)
    ret,thresh5 = cv2.threshold(frame,127,255,cv2.THRESH_TOZERO_INV)

    titles =['original image','binary','binary_inv','trunc','thresh_trunc','thresh_tozero_inv']
    images =[frame,thresh1,thresh2,thresh3,thresh4,thresh5]

    for i in range(6):
        plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])
    plt.show()
    k = cv2.waitKey(1) & 0xFF  # the number in waitkey means wait x ms to
    if k == 27:
        break
cv2.destroyAllWindows()
