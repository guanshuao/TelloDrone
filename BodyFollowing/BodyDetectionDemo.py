
import cv2
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture(0)
detector = PoseDetector(upBody=True)

while True:
    _, img = cap.read()
    img = detector.findPose(img, draw=True)
    lmList, bboxInfo = detector.findPosition(img, draw=True)

    cv2.imshow("BodyDetectionDemo", img)
    if cv2.waitKey(1) & 0xFF == ord('c'):
        break

cap.release()
cv2.destroyAllWindows()