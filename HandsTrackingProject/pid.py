import numpy as np
class PID:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp  # 比例控制器系数
        self.Ki = Ki  # 积分控制器系数
        self.Kd = Kd  # 微分控制器系数

        self.last_error = 0  # 上一次的误差
        self.integral = 0  # 积分项

    def update(self, setpoint, measured_value, dt):
        error = setpoint - measured_value  # 当前误差
        #print(f"error：{error:.4f}", end='  ')
        #print(f'self.integral：{self.integral:.4f}', end='  ')
        self.integral += error * dt  # 累计误差
        #print(f'累计：{self.integral:.4f}', end='  ')
        derivative = (error - self.last_error) / dt  # 当前误差变化率
        #print(f'变化率：{derivative:.4f}', end='  ')
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative  # PID控制器输出
        #print(f'pid输出：{output:.4f}', end='  ')
        self.last_error = error  # 保存当前误差作为上一次误差
        #print(f'保存误差：{self.last_error:.4f}', end='  ')
        return output


def pidcontroller(setpoint,measured_value,PID_0,dt,limit):#目标值，测量值，PID参数，微分量，速度上限
    a,b,c = PID_0[0],PID_0[1],PID_0[2]
    pid = PID(a,b,c)
    output = pid.update(setpoint,measured_value,dt)
    output = int(np.clip(output, -limit, limit))  # 设置速度上限
    return output

if __name__ == '__main__':
    w, h = 360, 240  # tello摄像头分辨率
    x=100
    y=50
    area =10000
    PID_lr = [0.5, 0.4, 0.1]
    PID_ud = [0.5, 0.4, 0.1]
    PID_yv = [0.5, 0.4, 0.1]
    PID_fb = [0.5, 0.4, 0.1]

    lr = pidcontroller(w // 2, x, PID_lr, 1, 20)
    ud = pidcontroller(h // 2, y, PID_ud, 1, 50)
    yv = pidcontroller(w // 2, x, PID_lr, 1, 50)
    fb = pidcontroller(22000,area,PID_fb,1,50)

    self.me.send_rc_control(lr, fb, ud, -yv)