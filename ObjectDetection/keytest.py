import cv2
import keyboard


# Initialize control values
lr, fb, ud, yv = 0, 0, 0, 0
speed = 50

import keyboard


def on_press(key):
    global lr, fb, ud, yv

    if key == 'left':
        lr = -speed
    elif key == 'right':
        lr = speed
    elif key == 'up':
        fb = speed
    elif key == 'down':
        fb = -speed
    elif key == 'w':
        ud = speed
    elif key == 's':
        ud = -speed
    elif key == 'a':
        yv = -speed
    elif key == 'd':
        yv = speed


def on_release(key):
    global lr, fb, ud, yv

    if key in ['left', 'right']:
        lr = 0
    elif key in ['up', 'down']:
        fb = 0
    elif key in ['w', 's']:
        ud = 0
    elif key in ['a', 'd']:
        yv = 0

keyboard.on_press(on_press)
keyboard.on_release(on_release)


while True:
    print([lr,fb,ud,yv])
    cv2.waitKey(1)