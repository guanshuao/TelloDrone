import cv2
import time
import os
import HandTrackingMoudule as htm

wCam,hCam=640,480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

#显示图片
# folderPath = "iphones"
# myList = os.listdir(folderPath)
# print(myList)
# overlayList = []#将图片的地址生成列表
# for imPath in myList:
#     image = cv2.imread(f"{folderPath}/{imPath}")#输出所有图片的路径
#     overlayList.append(image)

pTime = 0

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4,8,12,16,20]#从大拇指到小指
while True:

    success,img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    img = cv2.flip(img, 1)  # 水平镜像
    if len(lmList) != 0:
        fingers = []
        #Thumb
        if lmList[4][1] > lmList[3][1]:  # 大拇指特殊处理
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1,5):
            if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]:#指尖点的像素坐标在指关节像素坐标之上
                fingers.append(1)
            else:
                fingers.append(0)
       # print(fingers)
        totalFingers = fingers.count(1)#计数展开的手指
        print(totalFingers)
#显示图片
#     h, w, c = overlayList[totalFingers].shape #当索引值为-1时，显示最后一个图像
#        img[0:h, 0:w] = overlayList[totalFingers]  # 将图片放在显示界面(0,0)是初始坐标


    # 在img上实时显示帧率：坐标：（10,70），字体，比例，颜色，粗细
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS:{int(fps)}', (450, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Img", img)
    cv2.waitKey(1)

