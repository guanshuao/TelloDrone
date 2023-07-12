
import cv2
import time
import HandTrackingMoudule as htm

pTime = 0  # 初始时间
cTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()

while True:



    success, img = cap.read()
    img = cv2.flip(img, 1)#水平镜像
    img = detector.findHands(img)
    lmList=detector.findPosition(img)
    if len(lmList) != 0:
        print(lmList[4])#4是大拇指
    cTime = time.time()  # 返回1970至今的时间戳
    fps = 1 / (cTime - pTime)  # 计算实时帧率
    pTime = cTime
    # 在img上实时显示帧率：坐标：（10,70），字体，比例，颜色，粗细
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)