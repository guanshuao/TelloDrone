# 调取tello摄像头图像的基本实例

from djitellopy import tello
import cv2

me = tello.Tello() # 创建tello对象
me.connect()  # 连接tello
print(me.get_battery()) # 打印电量

me.streamoff() # 关闭视频流
me.streamon() # 打开视频流

while True:
    img = me.get_frame_read().frame # 读取图像
    img = cv2.resize(img, (640, 480)) # 调整图像大小
    cv2.imshow("Image", img) # 显示图像
    
    if cv2.waitKey(5) & 0xFF == ord('q'):
        me.streamoff()
        break

cv2.destroyAllWindows()
