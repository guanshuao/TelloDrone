import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

gesture_speeds = [0.5, 0.8, 1.1, 1.4, 1.7, 2.0, 2.3, 2.6]  # 手势控制速度
response_times = [0.5, 0.6, 0.7, 0.85, 1.0, 1.1, 1.15, 1.2]  # 无人机响应速度

# 对数据进行插值，生成一条平滑的曲线
x_new = np.linspace(np.min(gesture_speeds), np.max(gesture_speeds), 300)
spl = make_interp_spline(gesture_speeds, response_times, k=2)
y_smooth = spl(x_new)

# 绘制曲线并添加标签
plt.plot(x_new, y_smooth, label='Response Time')
plt.xlabel('Gesture Control Speed (m/s)')
plt.ylabel('Drone Response Time (s)')
plt.title('Relationship between Gesture Control Speed and Drone Response Time')

# 显示网格和图例
plt.grid(True)
plt.legend()
plt.show()



