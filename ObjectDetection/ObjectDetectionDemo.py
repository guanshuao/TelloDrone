import cv2
import cvzone

thres = 0.55 # 设置置信度阈值
nmsThres = 0.2 # 设置非极大值抑制阈值，用于消除重叠边界框

classNames = []
classFile = 'coco.names'
with open(classFile, 'rt') as f:
    classNames = f.read().split('\n')

configPath = 'ssd_mobilenet_v3_large_coco.pbtxt'
weightsPath = "frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

cap = cv2.VideoCapture(0)

# Initialize control values
lr, fb, ud, yv = 0, 0, 0, 0
speed = 50

keys_pressed = set()

while True:
    _, img = cap.read()
    classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nmsThres)

    try:
        for classId, conf, box in zip(classIds.flatten(), confs.flatten(), bbox):
            cvzone.cornerRect(img, box)
            cv2.putText(img, f'{classNames[classId - 1].upper()} {round(conf * 100, 2)}',
                        (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        1, (0, 255, 0), 2)
    except:
        pass

    img = cv2.resize(img, (1080, 720))
    cv2.imshow("ObjectDetectionDemo", img)

    if cv2.waitKey(1) & 0xFF == ord('c'):
        break

cap.release()
cv2.destroyAllWindows()