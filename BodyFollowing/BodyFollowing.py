from djitellopy import tello
import cv2
import cvzone
from cvzone.PoseModule import PoseDetector

detector = PoseDetector(upBody=True)

hi, wi, = 480, 640

xPID = cvzone.PID([0.22, 0, 0.1], wi // 2)
yPID = cvzone.PID([0.27, 0, 0.1], hi // 2, axis=1)
zPID = cvzone.PID([0.00016, 0, 0.000011], 150000, limit=[-20, 15])

myPlotX = cvzone.LivePlot(yLimit=[-100, 100], char='X')
myPlotY = cvzone.LivePlot(yLimit=[-100, 100], char='Y')
myPlotZ = cvzone.LivePlot(yLimit=[-100, 100], char='Z')

me = tello.Tello()
me.connect()
print(me.get_battery())
me.streamon()


while True:
    img = me.get_frame_read().frame
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换色彩空间
    img = cv2.resize(img, (640, 480))

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
        imgPlotX = myPlotX.update(xVal)
        imgPlotY = myPlotY.update(yVal)
        imgPlotZ = myPlotZ.update(zVal)

        img = xPID.draw(img, [cx, cy])
        img = yPID.draw(img, [cx, cy])
        imgStacked = cvzone.stackImages([img, imgPlotX, imgPlotY, imgPlotZ], 2, 0.75)
        cv2.putText(imgStacked, str(area), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    else:
        imgStacked = cvzone.stackImages([img], 1, 0.75)

    me.send_rc_control(0, -zVal, -yVal, xVal)

    cv2.imshow("BodyFollowing", imgStacked)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
    if cv2.waitKey(1) & 0xFF == ord('e'):
        me.takeoff()
    if cv2.waitKey(1) & 0xFF == ord('c'):
        me.emergency()
        break

cv2.destroyAllWindows()