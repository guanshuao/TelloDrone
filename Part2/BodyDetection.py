'''

import cv2
from cvzone.PoseModule import PoseDetector


cap = cv2.VideoCapture(0)
detector = PoseDetector()


while True:
    _, img = cap.read()
    img = detector.findPose(img, draw=True)
    lmList, bboxInfo = detector.findPosition(img, draw=True)

    cv2.imshow("Image", img)
    cv2.waitKey(1)


'''

import cv2
from djitellopy import tello
from cvzone.PoseModule import PoseDetector


me= tello.Tello()
me.connect()
print(me.get_battery())
me.streamoff()
me.streamon()

detector = PoseDetector()


while True:
    _ , img = me.get_frame_read().frame
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换色彩空间
    img = detector.findPose(img, draw=True)
    lmList, bboxInfo = detector.findPosition(img, draw=True)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
