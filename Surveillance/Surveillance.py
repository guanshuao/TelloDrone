# 此程序用于实现无人机的监控功能，同时兼具键盘控制功能

from djitellopy import tello
import KeyPressModule as kp
import time
import cv2

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

global img

me.streamoff()
me.streamon()

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if kp.getKey("LEFT"):
        lr = -speed
    elif kp.getKey("RIGHT"):
        lr = speed

    if kp.getKey("UP"):
        fb = speed
    elif kp.getKey("DOWN"):
        fb = -speed

    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    if kp.getKey("a"):
        yv = -speed
    elif kp.getKey("d"):
        yv = speed

    if kp.getKey("q"): me.land(); time.sleep(4)
    if kp.getKey("e"):  me.takeoff()

    # 按下z键时，保存当前图像至指定路径
    if kp.getKey("z"):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)
        time.sleep(0.3)

    return [lr, fb, ud, yv]


while True:

    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = me.get_frame_read().frame
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换色彩空间
    img = cv2.resize(img, (1080, 720))
    cv2.imshow("Image", img)
    cv2.waitKey(1)