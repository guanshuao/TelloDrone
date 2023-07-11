import cv2
from djitellopy import tello
import cvzone
import time
import keyboard

thres = 0.55
nmsThres = 0.2

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

me = tello.Tello()
me.connect()
me.streamoff()
me.streamon()

# Initialize control values
lr, fb, ud, yv = 0, 0, 0, 0
speed = 50

def on_press(key):
    global lr, fb, ud, yv
    key_name = key.name
    if key_name == 'left':
        lr = -speed
    elif key_name == 'right':
        lr = speed
    elif key_name == 'up':
        fb = speed
    elif key_name == 'down':
        fb = -speed
    elif key_name == 'w':
        ud = speed
    elif key_name == 's':
        ud = -speed
    elif key_name == 'a':
        yv = -speed
    elif key_name == 'd':
        yv = speed
    elif key_name == 'q':
        me.land()
    elif key_name == 'e':
        me.takeoff()

def on_release(key):
    global lr, fb, ud, yv
    key_name = key.name
    if key_name in ['left', 'right']:
        lr = 0
    elif key_name in ['up', 'down']:
        fb = 0
    elif key_name in ['w', 's']:
        ud = 0
    elif key_name in ['a', 'd']:
        yv = 0

keyboard.on_press(on_press)
keyboard.on_release(on_release)


while True:
    me.send_rc_control(lr, fb, ud, yv)

    img = me.get_frame_read().frame
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

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
    cv2.imshow("Image", img)
    cv2.waitKey(1)
