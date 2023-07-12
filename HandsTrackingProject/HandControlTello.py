import cv2
import time
import HandTrackingMoudule as htm
from djitellopy import tello

#电脑摄像头初始化
wCam,hCam=640,480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
#屏幕遥控器初始化：
LeftPx,LeftPy=int(3*wCam/4),int(0.66*hCam)
RighPx,RighPy=int(wCam/4),int(0.66*hCam)
PointRange=60
#起降按钮大小：
tlPw,tlPh=64,48
#起飞按钮(以左上角为初始点）
tfP1x,tfP1y=600,30
tfP2x,tfP2y=tfP1x-tlPw,tfP1y+tlPh
takeoffcx,takeoffcy=0.5*(tfP1x+tfP2x),0.5*(tfP1y+tfP2y)
#降落按钮(以左上角为初始点）
lP1x,lP1y=104,30
lP2x,lP2y=lP1x-tlPw,lP1y+tlPh
launchcx,launchcy=0.5*(lP1x+lP2x),0.5*(lP1y+lP2y)
#标志位
takeoff = 0
flag = 0


#Tello初始化
wtello=360
htello=240

me = tello.Tello()
me.connect()
me.streamon()
print(me.get_battery())

#速度命令初始化
lr,fb,ud,yv=40,40,25,30


detector = htm.handDetector(detectionCon=0.7)#定义一个手部跟踪对象,置信度0.7

while True:
    success,img = cap.read()
    img = cv2.flip(img, 1)  # 水平镜像
    img = detector.findHands(img)#调用方法；将拍摄图像转换成带有手部标记的图像
    telloimg=me.get_frame_read().frame#调用tello摄像头
    telloimg = cv2.resize(telloimg, (360, 240))  # 调整图像大小
    lmList = detector.findPosition(img, draw=False)
    #显示手势控制按钮

    #起飞按钮
    if takeoff==1:
        cv2.rectangle(img, (tfP1x+4, tfP1y-3), (tfP2x-4, tfP2y+3), (0,255,0), cv2.FILLED)
        cv2.rectangle(img, (lP1x, lP1y), (lP2x, lP2y), (128, 128, 128), cv2.FILLED)
        cv2.putText(img, f'takeoff', (500, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
        # 左右遥杆：
        cv2.circle(img, (LeftPx, LeftPy), 10, (0, 255, 0), cv2.FILLED)
        cv2.circle(img, (LeftPx, LeftPy), PointRange, (0, 255, 0), 3)
        cv2.circle(img, (RighPx, RighPy), 10, (0, 255, 0), cv2.FILLED)
        cv2.circle(img, (RighPx, RighPy), PointRange, (0, 255, 0), 3)
    else:
        cv2.rectangle(img, (tfP1x, tfP1y), (tfP2x, tfP2y), (128, 128, 128), cv2.FILLED)
        cv2.rectangle(img, (lP1x + 4, lP1y - 3), (lP2x - 4, lP2y + 3), ( 255, 0, 0), cv2.FILLED)
        cv2.putText(img, f'land', (25, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)
        # 左右遥杆：
        cv2.circle(img, (LeftPx, LeftPy), 10, (128, 128, 128), cv2.FILLED)
        cv2.circle(img, (LeftPx, LeftPy), PointRange, (128, 128, 128), 3)
        cv2.circle(img, (RighPx, RighPy), 10, (128, 128, 128), cv2.FILLED)
        cv2.circle(img, (RighPx, RighPy), PointRange, (128, 128, 128), 3)

    if len(lmList) != 0:
        cv2.circle(img, (lmList[8][1], lmList[8][2]), 10, (0, 0, 255), cv2.FILLED)#显示手指
        #print(lmList[8][1], lmList[8][2])
        val = [0, 0, 0, 0]
        #点击起飞降落按钮
        if (takeoffcy - lmList[8][2]) ** 2 + (takeoffcx - lmList[8][1]) ** 2 < 13 ** 2:
            takeoff=1
            if flag==0:
                me.takeoff()
                flag=1
            #cv2.waitKey(50)
            #print("起飞")
        if (launchcy - lmList[8][2]) ** 2 + (launchcx - lmList[8][1]) ** 2 < 13 ** 2:
            takeoff=0
            me.land()
            flag=0
            #print("降落")

        #控制遥杆
        if (LeftPy-lmList[8][2])**2+(LeftPx-lmList[8][1])**2<PointRange**2:
            cv2.circle(img, (lmList[8][1], lmList[8][2]), 10, (255, 255, 0), cv2.FILLED)  # 指变色
            cv2.circle(img, (LeftPx, LeftPy), 10, (255, 255, 0), cv2.FILLED)
            cv2.circle(img, (LeftPx, LeftPy), PointRange, (255, 255, 0), 3)
            cv2.line(img, (LeftPx, LeftPy), (lmList[8][1], lmList[8][2]), (255,255,0), 3)  # 杆指间画线
            direction = abs((lmList[8][2] - LeftPy + 0.001) / (lmList[8][1] - LeftPx + 0.001))  # 计算指杆斜率绝对值

            if lmList[8][2]<LeftPy:#手指在上方
                if lmList[8][1] < LeftPx:#手指在第一象限
                    if direction<1:
                        print("向左")
                        val[0]=-lr
                        #me.send_rc_control(-lr, 0, 0, 0)
                    else:
                        print("向前")
                        val[1]=fb
                        #me.send_rc_control(0, fb, 0, 0)
                else:#手指在第四象限
                    if direction<1:
                        print("向右")
                        val[0] = lr
                        #me.send_rc_control(lr, 0, 0, 0)
                    else:
                        print("向前")
                        val[1]=fb
                        #me.send_rc_control(0, fb, 0, 0)
            else:#手指在下方
                if lmList[8][1] < LeftPx:#手指在第二象限
                    if direction<1:
                        print("向左")
                        val[0] = -lr
                        #me.send_rc_control(-lr, 0, 0, 0)
                    else:
                        print("向后")
                        val[1] = -fb
                        #me.send_rc_control(0, -fb, 0, 0)
                else:#手指在第四象限
                    if direction<1:
                        print("向右")
                        val[0] = lr
                        #me.send_rc_control(lr, 0, 0, 0)
                    else:
                        print("向后")
                        val[1]=-fb
                        #me.send_rc_control(0, -fb, 0, 0)
        elif (RighPy-lmList[8][2])**2+(RighPx-lmList[8][1])**2<PointRange**2:
            cv2.circle(img, (lmList[8][1], lmList[8][2]), 10, (255, 255, 0), cv2.FILLED)  # 指变色
            cv2.circle(img, (RighPx, RighPy), 10, (255, 255, 0), cv2.FILLED)
            cv2.circle(img, (RighPx, RighPy), PointRange, (255, 255, 0), 3)
            cv2.line(img, (RighPx, RighPy), (lmList[8][1], lmList[8][2]), (255,255,0), 3)  # 杆指间画线
            # 操作右遥杆发出命令：
            direction = abs((lmList[8][2] - RighPy + 0.001) / (lmList[8][1] - RighPx + 0.001))  # 计算指杆斜率绝对值
            if lmList[8][2] < RighPy:  # 手指在上方
                if lmList[8][1] < RighPx:  # 手指在第一象限
                    if direction < 1:
                        print("向左转向")
                        val[3] = yv
                        #me.send_rc_control(0, 0, 0, yv)
                    else:
                        print("上升")
                        val[2] = ud
                        #me.send_rc_control(0, 0, ud, 0)
                else:  # 手指在第四象限
                    if direction < 1:
                        print("向右转向")
                        val[3] = -yv
                        #me.send_rc_control(0, 0, 0, -yv)
                    else:
                        print("上升")
                        val[2] = ud
                        #me.send_rc_control(0, 0, ud, 0)
            else:  # 手指在下方
                if lmList[8][1] < RighPx:  # 手指在第二象限
                    if direction < 1:
                        print("向左转向")
                        val[3]=yv
                        #me.send_rc_control(0, 0, 0, yv)
                    else:
                        print("下降")
                        val[2]=-ud
                        #me.send_rc_control(0, 0, -ud, 0)
                else:  # 手指在第四象限
                    if direction < 1:
                        print("向右转向")
                        val[3]=-yv
                        #me.send_rc_control(0, 0, 0, -yv)
                    else:
                        print("下降")
                        val[2] = -ud
                        #me.send_rc_control(0, 0, -ud, 0)
        else:
            print("悬停")
        me.send_rc_control(val[0], val[1], val[2], val[3])

        #for shizhi in range(5,9):
            #cv2.circle(img, (lmList[shizhi][1], lmList[shizhi][2]), 10, (255, 0, 255), cv2.FILLED)
            #print(lmList[shizhi][1],lmList[shizhi][2])
        #print("##########")
        #direction = (lmList[12][2]-lmList[9][2])//(lmList[12][1]-lmList[9][1])
        #print(direction)

    # 帧率显示
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # 在img上实时显示帧率：坐标：（10,70），字体，比例，颜色，粗细
    cv2.putText(img, f'FPS:{int(fps)}', (270, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Img", img)
    cv2.imshow("Tello", telloimg)

    cv2.waitKey(1)