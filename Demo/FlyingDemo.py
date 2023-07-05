from djitellopy import tello # 导入tello库
import time

me = tello.Tello() # 创建tello对象
me.connect()   # 连接tello
print(me.get_battery()) # 打印电量

me.takeoff() # 起飞

# Move using Distance
me.move_up(80) # 上升80cm

# Move using Speed
# send_rc_control(左右, 前后, 上下, 旋转)速度范围[-100, 100]
me.send_rc_control(0, 0, 0, 20)
time.sleep(5)

me.send_rc_control(0, 0, 0, 0)

me.land()

