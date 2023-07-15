# 使用cvzone模块，接收来自计算机内置相机的视频流，检测人脸

import cv2
from cvzone.FaceDetectionModule import FaceDetector

detector = FaceDetector()
cap = cv2.VideoCapture(0)

while True:
    _, img = cap.read()
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换色彩空间
    img, bboxs = detector.findFaces(img, draw=True)
    cv2.imshow("FaceDetection", img)
    if cv2.waitKey(1) & 0xFF == ord('c'):
        break

cap.release()
cv2.destroyAllWindows()
