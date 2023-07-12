import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#生成手掌移动轨迹数据
t = np.linspace(0, 2*np.pi, 100)
x_hand = np.sin(t)
y_hand = np.cos(t)
z_hand = t

#生成震荡拟合的无调整的无人机移动轨迹数据
x_drone_no_tuning = np.sin(t) + np.random.normal(0, 0.05, 100)
y_drone_no_tuning = np.cos(t) + np.random.normal(0, 0.05, 100)
z_drone_no_tuning = t + np.random.normal(0, 0.05, 100)

#生成震荡拟合的较高程度的无人机移动轨迹数据
x_drone_tuned = np.sin(t) + np.random.normal(0, 0.02, 100)
y_drone_tuned = np.cos(t)  + np.random.normal(0, 0.02, 100)
z_drone_tuned = t + np.random.normal(0, 0.02, 100)

#绘制手掌移动轨迹和无调整无人机移动轨迹
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x_hand, y_hand, z_hand, label='Hand Trajectory')
ax.plot(x_drone_no_tuning, y_drone_no_tuning, z_drone_no_tuning, label='Drone Trajectory (No Tuning)')
ax.plot(x_drone_tuned, y_drone_tuned, z_drone_tuned, label='Drone Trajectory (Tuned)')
ax.legend()
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()







