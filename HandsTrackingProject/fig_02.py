import matplotlib.pyplot as plt
import numpy as np

#手势控制精度MAE值（越小越好）
mae = [0.5, 0.4, 0.35, 0.3, 0.25, 0.22, 0.2]

#无人机位置误差
location_error = [0.6, 0.5, 0.45, 0.4, 0.3, 0.25, 0.2]

#姿态角误差
attitude_error = [25, 20, 18, 15, 12, 11, 10]

#创建画布和两个子图
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(8, 8))

#在第一个子图中绘制折线图1
ax1.plot(mae, location_error, label='Location Error', marker='o')
ax1.set_ylabel('Location Error (meters)')

#在第二个子图中绘制折线图2
ax2.plot(mae, attitude_error, label='Attitude Error', marker='s')
ax2.set_xlabel('MAE (Smaller is better)')
ax2.set_ylabel('Attitude Error (degrees)')

#添加标题和共同的坐标轴标签
fig.suptitle('Relationship between Gesture Control Accuracy and UAV Errors')
fig.text(0.5, 0.04, 'MAE (Smaller is better)', ha='center')
fig.text(0.04, 0.5, 'Error', va='center', rotation='vertical')

#添加网格线
ax1.grid(True)
ax2.grid(True)

#添加图例
ax1.legend()
ax2.legend()

#显示图形
plt.show()

