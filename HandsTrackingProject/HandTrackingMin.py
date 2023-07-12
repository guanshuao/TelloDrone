import mediapipe as mp
import cv2
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()

#mp.solutions.drawing_utils用于绘制
mpDraw = mp.solutions.drawing_utils


pTime = 0 #初始时间
cTime = 0


while True:
    success,img  = cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)#转换成RGB格式
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:#如果检测到手势
        for handLms in results.multi_hand_landmarks:#对每只手进行操作
            for id,lm in enumerate(handLms.landmark):#id用于获取手点阵的索引（0为手的跟部，4为大拇指），lm获取手的坐标(比例值）

                h,w,c=img.shape#图像：高，宽，通道
                cx,cy=int(lm.x*w),int(lm.y*h)
                #if id == 4:#实时显示某个手的索引
                    #cv2.circle(img,(cx,cy),25,(255,0,0),cv2.FILLED)
                    #print(id,cx,cy)
            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)#绘制每只手的点阵，且相连

    cTime = time.time()#返回1970至今的时间戳
    fps = 1/(cTime-pTime)#计算实时帧率
    pTime = cTime
    #在img上实时显示帧率：坐标：（10,70），字体，比例，颜色，粗细
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)



    cv2.imshow("Image",img)
    cv2.waitKey(1)


