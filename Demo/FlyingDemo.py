# 让Tello无人机起飞的基本示例

from djitellopy import tello
import time

me = tello.Tello()
me.connect()
print(me.get_battery())

me.takeoff()

time.sleep(5)

me.flip_left()


'''
# 左转
start_time = time.time() # 记录当前时间
while True: # 开始无限循环
    me.send_rc_control(0, 50, 0, 0) # 发送控制命令
    if time.time() - start_time > 2: # 检查是否已经过了一秒
        break # 如果已经过了一秒，结束循环
        
        '''

me.land()
