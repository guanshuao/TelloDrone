# 此程序用于实现无人机的监控功能，同时兼具键盘控制功能

from djitellopy import tello
import time
import cv2
import keyboard

me = tello.Tello()
me.connect()
print(me.get_battery())

global img

me.streamon()

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if keyboard.is_pressed('left'):  # if key 'left' is pressed
        lr = -speed
    elif keyboard.is_pressed('right'):
        lr = speed

    if keyboard.is_pressed('up'):
        fb = speed
    elif keyboard.is_pressed('down'):
        fb = -speed

    if keyboard.is_pressed('w'):
        ud = speed
    elif keyboard.is_pressed('s'):
        ud = -speed

    if keyboard.is_pressed('a'):
        yv = -speed
    elif keyboard.is_pressed('d'):
        yv = speed

    if keyboard.is_pressed('q'):
        me.land()
    if keyboard.is_pressed('e'):
        me.takeoff()

    if keyboard.is_pressed('z'):
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
    if cv2.waitKey(1) & 0xFF == ord('c'):
        me.land()
        break

cv2.destroyAllWindows()