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
