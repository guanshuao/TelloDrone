from djitellopy import tello
import KeyPressModule as kp
import time
import cv2
import torch
from models import *  # 导入你的YOLOv4模型，这取决于你的实现和目录结构
from utils.utils import *  # 导入YOLOv4的辅助函数，这取决于你的实现和目录结构

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 加载YOLOv4模型
model = Darknet("config_file_path", img_size=416).to(device)  # config_file_path替换为你的YOLOv4配置文件路径
model.load_darknet_weights("weights_path")  # weights_path替换为你的YOLOv4权重文件路径
model.eval()

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

global img

me.streamoff()
me.streamon()


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if kp.getKey("LEFT"):
        lr = -speed
    elif kp.getKey("RIGHT"):
        lr = speed

    if kp.getKey("UP"):
        fb = speed
    elif kp.getKey("DOWN"):
        fb = -speed

    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    if kp.getKey("a"):
        yv = -speed
    elif kp.getKey("d"):
        yv = speed

    if kp.getKey("q"): me.land(); time.sleep(4)
    if kp.getKey("e"):  me.takeoff()

    # 按下z键时，保存当前图像至指定路径
    if kp.getKey("z"):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)
        time.sleep(0.3)

    return [lr, fb, ud, yv]


while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = me.get_frame_read().frame
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换色彩空间
    img = cv2.resize(img, (1080, 720))

    # 物体检测
    img_tensor = torch.from_numpy(img).float().div(255.0).unsqueeze(0).to(device)
    detections = model(img_tensor)
    detections = non_max_suppression(detections, 0.8, 0.4)  # 使用你的阈值
    if detections[0] is not None:
        detections = rescale_boxes(detections[0], 416, img.shape[:2])
        for x1, y1, x2, y2, conf, cls_conf, cls_pred in detections:
            # 画出边框和标签
            box_w = x2 - x1
            box_h = y2 - y1
            color = [int(c) for c in COLORS[int(cls_pred)]]
            img = cv2.rectangle(img, (x1, y1, x2, y2), color, 2)
            cv2.putText(img, f"{cls_pred}: {cls_conf.item():.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color,
                        2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
