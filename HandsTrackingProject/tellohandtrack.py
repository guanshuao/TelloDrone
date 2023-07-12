import cv2
from djitellopy import tello
import HandTrackingMoudule as htm
import numpy as np
import KeyPressModule as kp



#####################
w,h = 360,240
#####################
fbRange = [20000,24000]
pid = [0.4,0.4,0]
pError = 0
#####################

lmList=[]

detector = htm.handDetector(detectionCon=0.7)#定义一个手部跟踪对象,置信度0.7

#######################
kp.init()
me = tello.Tello()
me.connect()
me.streamon()
print(me.get_battery())
#cap = cv2.VideoCapture(0)
flag = 0

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if kp.getKey("LEFT"): lr = -speed
    elif kp.getKey("RIGHT"): lr = speed

    if kp.getKey("UP"): fb = speed
    elif kp.getKey("DOWN"): fb = -speed

    if kp.getKey("w"): ud = speed
    elif kp.getKey("s"): ud = -speed

    if kp.getKey("a"): yv = speed
    elif kp.getKey("d"): yv = -speed

    if kp.getKey("q"): me.land()

    if kp.getKey("e"): me.takeoff()

    return [lr, fb, ud, yv]

def findHand(img,lmList):
    myHandList=[]
    myHandListArea=[]
    lmList = detector.findPosition(img, draw=False)
    X = []
    Y = []
    for i in range(20):#遍历20个点的坐标，找到最大点以及最小点使得手的框选取最大值
        X.append(lmList[i][1])
        Y.append(lmList[i][2])
    x1,y1 = np.min(X),np.min(Y)
    x2,y2 = np.max(X),np.max(Y)
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 厚度为2的绿色长方体
    cx,cy=0.5*(x1+x2),0.5*(y1+y2)
    area=(x1-x2)*(y1-y2)
    print(cx,cy)
    cv2.circle(img, (int(cx),int(cy)), 5, (255, 0, 0), cv2.FILLED)
    myHandList.append([cx,cy])
    myHandListArea.append(area)

    if len(myHandListArea) != 0:
        #i =myHandListArea.index(max(myHandListArea))#i是矩形框最大值的索引
        return img,[[cx,cy],myHandListArea[0]]#返回面部最大值
    else:
        return img,[[0,0],0]


def trackHand(info,w,pid,pError):#PID手部追踪算法
    area = info[1]
    x,y= info[0]
    fb = 0
    yverror = x - w//2 #error的意思是偏航误差
    yv = pid[0]*yverror + pid[1]*(yverror-pError)
    yv = int(np.clip(yv,-100,100))#将偏航速度上限调成100
    if area > fbRange[0] and area < fbRange[1]:#距离合适保持静止
        fb = 0
    if area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20
    if x == 0:
        yv = 0
        yverror = 0
    print(yv,fb)
    me.send_rc_control(0,fb,0,-yv)

    return yverror

#cap = cv2.VideoCapture(0)
if __name__ == '__main__':

    while True:
        #success,img = cap.read()
        img = me.get_frame_read().frame
        img = cv2.flip(img, 1)  # 水平镜像
        img = cv2.resize(img, (360, 240))#调整tello分辨率
        img = detector.findHands(img, lmList)  # 调用方法；将拍摄图像转换成带有手部标记的图像
        lmList = detector.findPosition(img, draw=False)
        print(lmList)
        if len(lmList) != 0:
        #img = cv2.flip(img, 0)  # 翻转
            img, info = findHand(img,lmList)
            pError = trackHand(info, w, pid, pError)
            print("Area", info[1], "Center", info[0])

        cv2.imshow("Image", img)

        vals = getKeyboardInput()
        cv2.waitKey(1)
    # cv2.imshow('Output',img)
    # if 0xFF == ord('1'):
    #     qfly.takeoff()
    # if cv2.waitKey(1) & 0xFF == ord("0"):
    #     qfly.land()
