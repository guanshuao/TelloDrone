import cv2
import time
import numpy as  np
import HandTrackingMoudule as htm
import  math
#可调用电脑音量
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume
#################################
wCam,hCam=640,480
#################################
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)#定义一个手部跟踪对象,置信度0.7

#调用电脑音量
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume = cast(interface,POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
#print(volume.GetVolumeRange())

minVol = volRange[0]
maxVol = volRange[1]
#print(minVol,maxVol)
vol = 0
volBar = 400
volPer = 0

while True:
    success,img = cap.read()
    img = cv2.flip(img, 1)  # 水平镜像
    img = detector.findHands(img)#调用方法；将拍摄图像转换成带有手部标记的图像
    lmList = detector.findPosition(img,draw=False)#生成手部点阵标记列表
    if len(lmList) != 0:
        #print(lmList[4],lmList[8])#打印食指，拇指的坐标

        x1,y1 = lmList[4][1],lmList[4][2]#打印拇指的坐标
        x2, y2 = lmList[8][1], lmList[8][2]  # 打印食指的坐标
        cx,cy = (x1+x2)//2 , (y1+y2)//2
        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)#两指间画线
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)#线的中点描点

        length = math.hypot(x2-x1,y2-y1)#计算两点之间长度
        #print(length)
        if length<25:
            cv2.circle(img, (cx, cy), 10, (0,255,0), cv2.FILLED)  # 当两点之间足够近时，按钮变色

        # Hand Range (25,230) --> Volume Range (-65,0)
        vol = np.interp(length, [25, 230], [minVol, maxVol])  # 手指间距到系统音量的映射
        volBar = np.interp(length, [25, 230], [400, 150])
        volPer = np.interp(length, [25, 230], [0, 100])

        volume.SetMasterVolumeLevel(vol, None)  # 设置电脑音量（0=100；-62.25=0）


    cv2.rectangle(img,(50,150),(85,400),(255,0,0),3)#创建音量条
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255,0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0, 0), 3)

    #帧率显示
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    # 在img上实时显示帧率：坐标：（10,70），字体，比例，颜色，粗细
    cv2.putText(img, f'FPS:{int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)


    cv2.imshow("Img",img)
    cv2.waitKey(1)