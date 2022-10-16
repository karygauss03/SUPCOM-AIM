import cv2
import imutils
from skimage.filters import threshold_local
from transformer import four_point_transform
import numpy as np

img_path = 'JIP01b.jpg'
big_img = cv2.imread(img_path)
cv2.imshow('org img',big_img)
cv2.waitKey(0)


ratio = big_img.shape[0] / 500.0
org = big_img.copy()
img = imutils.resize(big_img, height = 500)
cv2.imshow('resizing',img)
cv2.waitKey(0)


gray_img = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY)
blur_img = cv2.GaussianBlur(gray_img,(5,5),0)
edged_img = cv2.Canny(blur_img,75,200)
cv2.imshow('edged',edged_img)
cv2.waitKey(0)


cnts,_ = cv2.findContours(edged_img.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts,key=cv2.contourArea,reverse=True)[:5]
for c in cnts:
    peri = cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,0.02*peri,True)
    if len(approx)==4:
        doc = approx
        break
        
        
p=[]
for d in doc:
    tuple_point = tuple(d[0])
    cv2.circle(img,tuple_point,3,(0,0,255),4)
    p.append(tuple_point)
cv2.imshow('Corner points detected',img)
cv2.waitKey(0)


warped = four_point_transform(org, doc.reshape(4, 2) * ratio)
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
cv2.imshow("Warped", imutils.resize(warped, height = 650))
cv2.waitKey(0)


T = threshold_local(warped, 11, offset = 10, method = "gaussian")
warped = (warped > T).astype("uint8") * 255
cv2.imshow("Scanned", imutils.resize(warped, height = 650))
cv2.waitKey(0)
cv2.destroyAllWindows()
