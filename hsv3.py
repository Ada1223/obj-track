import numpy as np
import cv2
import time
import os
import uuid
''' Main Code From Here'''
cap = cv2.VideoCapture('./3.mp4')

#Creat directory
labels = ['HSVimage']
IMAGES_PATH = os.path.join('./','HSVProject')
if not os.path.exists(IMAGES_PATH):
    if os.name == 'posix':
        os.mkdir(IMAGES_PATH)
    if os.name == 'nt':
        os.mkdir(IMAGES_PATH)
for label in labels:
    path = os.path.join(IMAGES_PATH, label)
    if not os.path.exists(path):
        os.mkdir(path)
#Warmup
time.sleep(2)
def nothing(x):
    pass
#Create a window
cv2.namedWindow('image')
cv2.namedWindow("Frame", cv2.WINDOW_NORMAL) 
#create trackbar for color change
cv2.createTrackbar('HMin','image',0,179,nothing)
cv2.createTrackbar('SMin','image',0,255,nothing)
cv2.createTrackbar('VMin','image',0,255,nothing)
cv2.createTrackbar('HMax','image',0,179,nothing)
cv2.createTrackbar('SMax','image',0,255,nothing)
cv2.createTrackbar('VMax','image',0,255,nothing)
#Set default value for MAX HSV trackbar
cv2.setTrackbarPos('HMax','image',179)
cv2.setTrackbarPos('SMax','image',255)
cv2.setTrackbarPos('VMax','image',255)
#Initial check if HSV min/max value changes
hMin=sMin=vMin=hMax=sMax=vMax=0
phMin=psMin=pvMin=phMax=psMax=pvMax=0
#Take video
while True:
    ret, frame = cap.read()
    img=frame
    output=img
    #get current position of all trackbar
    hMin=cv2.getTrackbarPos('HMin','image')
    sMin=cv2.getTrackbarPos('SMin','image')
    vMin=cv2.getTrackbarPos('VMin','image')
    
    hMax=cv2.getTrackbarPos('HMax','image')
    sMax=cv2.getTrackbarPos('SMax','image')
    vMax=cv2.getTrackbarPos('VMax','image')
    
    #Set minimum and max HSV values to display
    lower=np.array([hMin,sMin,vMin])
    upper=np.array([hMax,sMax,vMax])
    
    #Create HSV Image and threshold into a range
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,lower,upper)
    output=cv2.bitwise_and(img,img,mask=mask)
    
    #Print if there is a change in HSV value
    if ((phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax)):
        print("(hMin = %d, sMin = %d, vMin = %d), (hMax = %d, sMax = %d, vMax = %d)" %(hMin,sMin,vMin,hMax,sMax,vMax))
        phMin = hMin
        psMin = sMin
        pvMin = vMin
        phMax = hMax
        psMax = sMax
        pvMax = vMax
        
    
    cv2.imshow("Frame",output)
    key =cv2.waitKey(1) & 0xFF
    #Break condition
    if key==ord("s"):
        label=labels[0]
        imgname = os.path.join(IMAGES_PATH,label,label+'.'+'{}.jpg'.format(str(uuid.uuid1())))
        cv2.imwrite(imgname, output)
        print('Collected images for {}'.format(label))
    if key==ord("q"):
        break
cap.release()
cv2.destroyAllWindows() 
