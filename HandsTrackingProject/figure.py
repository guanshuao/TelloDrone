import numpy as np
import matplotlib.pyplot as plt

# 三组数据，每一组对应特定的最大和最小横滚、俯仰、偏航角度（6个数据）
data = [
    {'roll_min': 5, 'roll_max': 20, 'pitch_min': 10, 'pitch_max': 25, 'yaw_min': 2, 'yaw_max': 10},
    {'roll_min': 2, 'roll_max': 15, 'pitch_min': 8, 'pitch_max': 20, 'yaw_min': 1, 'yaw_max': 8},
    {'roll_min': 8, 'roll_max': 25, 'pitch_min': 12, 'pitch_max': 30, 'yaw_min': 3, 'yaw_max': 12}
]

# 计算无人机稳定性指数
def calc_stability_index(data):
    return (data['roll_max'] - data['roll_min']) + (data['pitch_max'] - data['pitch_min']) + (data['yaw_max'] - data['yaw_min'])

# 计算稳定性指数
stability_indices = [calc_stability_index(d) for d in data]

# 手势控制稳定性数据
gesture_stabilities = np.linspace(0.1, 0.3, 1)

# 计算无人机稳定性指数随手势控制稳定性的变化
drone_stabilities = np.interp(gesture_stabilities, [0, 0.5, 1], [0.2, np.mean(stability_indices), 0.8])

# 绘图
plt.plot(gesture_stabilities, drone_stabilities, label='无人机稳定性指数')
plt.scatter(stability_indices, np.ones(len(stability_indices)), color='red', label='数据点')
plt.xlabel('手势控制稳定性')
plt.ylabel('稳定性指数')
plt.legend()
plt.show()
