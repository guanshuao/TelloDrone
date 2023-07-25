# 调取tello摄像头图像的基本示例
from djitellopy import tello
import cv2

me = tello.Tello() # 创建tello对象
me.connect()  # 连接tello
print(me.get_battery()) # 打印电量

# me.streamoff() # 关闭视频流
me.streamon() # 打开视频流

while True:# 主循环
    img = me.get_frame_read().frame # 读取图像
    img = cv2.resize(img, (1280, 720)) # 调整图像大小

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换色彩空间

    cv2.imshow("ImageDemo", img) # 显示图像
    cv2.waitKey(1) # 等待1ms

    if cv2.waitKey(1) & 0xFF == ord('c'):
        break

cv2.destroyAllWindows()
