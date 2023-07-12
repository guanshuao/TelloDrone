from cvzone.PoseModule import PoseDetector
import time
from djitellopy import tello
import cv2
import cvzone

hi, wi, = 480, 640

#                   P   I  D
xPID = cvzone.PID([0.22, 0, 0.1], wi // 2)
yPID = cvzone.PID([0.27, 0, 0.1], hi // 2, axis=1)
zPID = cvzone.PID([0.00016, 0, 0.000011], 150000, limit=[-20, 15])

detector = PoseDetector(upBody=True)

snapTimer = 0
following = False
colorG = (0, 0, 255)
gesture = ''

me = tello.Tello()
me.connect()

me.streamoff()
me.streamon()
# me.takeoff()
# me.move_up(80)


while True:
    img = me.get_frame_read().frame
    img = cv2.resize(img, (640, 480))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换色彩空间
    img = detector.findPose(img, draw=True)
    lmList, bboxInfo = detector.findPosition(img, draw=True)

    xVal = 0
    yVal = 0
    zVal = 0

    if bboxInfo:

        cx, cy = bboxInfo['center']
        x, y, w, h = bboxInfo['bbox']
        area = w * h

        xVal = int(xPID.update(cx))
        yVal = int(yPID.update(cy))
        zVal = int(zPID.update(area))

        angArmL = detector.findAngle(img, 13, 11, 23, draw=True)
        angArmR = detector.findAngle(img, 14, 12, 24, draw=True)
        crossDistL, img, _ = detector.findDistance(15, 12, img, draw=True)
        crossDistR, img, _ = detector.findDistance(16, 11, img, draw=True)

        if detector.angleCheck(angArmL, 90) and detector.angleCheck(angArmR, 270):
            gesture = 'Tracking Mode: OFF' # 两手平举成T形状，关闭追踪
            colorG = (0, 0, 255)
            following = False
        elif detector.angleCheck(angArmL, 170) and detector.angleCheck(angArmR, 180):
            gesture = 'Tracking Mode: ON' # 双手举起，打开追踪模式
            colorG = (0, 255, 0)
            following = True
        elif crossDistL:
            if crossDistL < 70 and crossDistR < 70:
                gesture = "Cross" # 两手在胸前交叉，准备自拍
                snapTimer = time.time()

        if snapTimer > 0:
            totalTime = time.time() - snapTimer
            print(totalTime)
            if totalTime < 1.9:
                cv2.putText(img, "Ready", (225, 260), cv2.FONT_HERSHEY_PLAIN,
                            5, (255, 0, 255), 5)
            elif totalTime > 2:
                snapTimer = 0
                cv2.imwrite(f'Saved/{time.time()}.jpg', img)
                cv2.putText(img, "Saved", (225, 260), cv2.FONT_HERSHEY_PLAIN,
                            5, (0, 255, 0), 5)
                time.sleep(0.2)
        else:
            cv2.putText(img, gesture, (20, 50),
                        cv2.FONT_HERSHEY_PLAIN, 3, colorG, 3)

    if following:
        me.send_rc_control(0, -zVal, -yVal, xVal)
    else:
        me.send_rc_control(0, 0, 0, 0)

    cv2.imshow("Image ", img)


    if cv2.waitKey(5) & 0xFF == ord('q'):
        me.land()
        break

    if cv2.waitKey(5) & 0xFF == ord('e'):
        me.takeoff()


cv2.destroyAllWindows()



# THOjUPLsS5M