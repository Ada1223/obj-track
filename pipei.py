import cv2 #opencv读取的格式是BGR
import numpy as np
import matplotlib.pyplot as plt

img_rgb = cv2.imread('pip.png')
#img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread('tem2.png')
h, w = template.shape[:2]

res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.7
# 取匹配程度大于%80的坐标
loc = np.where(res >= threshold)
for pt in zip(*loc[::-1]):  # *号表示可选参数
    bottom_right = (pt[0] + w, pt[1] + h)
    cv2.rectangle(img_rgb, pt, bottom_right, (0, 255, 0), 2)

cv2.imshow('img_rgb', img_rgb)
cv2.waitKey(0)

cv2.destroyAllWindows()
