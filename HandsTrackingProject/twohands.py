import cv2
import time
import HandTrackingMoudule as htm
import mediapipe as mp

#电脑摄像头初始化
wCam,hCam=640,480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)i
pTime = 0


detector = htm.handDetector(detectionCon=0.7)#定义一个手部跟踪对象,置信度0.7
Hand1list=[]
Hand2list=[]

while True:
    success,img = cap.read()
    img = cv2.flip(img, 1)  # 水平镜像
    img = detector.findHands(img)#调用方法；将拍摄图像转换成带有手部标记的图像
    


    cv2.imshow("Img", img)
    cv2.waitKey(1)