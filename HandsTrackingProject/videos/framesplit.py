import cv2
import os

# 打开视频文件
video = cv2.VideoCapture('/Users/qiufeixiang/source/PycharmProjects/HandsTrackingProject/videos/0005.mp4')

# 创建文件夹
video_name = os.path.splitext(os.path.basename('0005.mp4'))[0]
if not os.path.exists(video_name):
    os.makedirs(video_name)

# 定义变量
frame_count = 0
pixel_value_dirs = {}

# 逐帧读取视频并计算平均像素值
while True:
    ret, frame = video.read()
    if not ret:
        break

    # 计算平均像素值并创建对应的目录
    avg_pixel_value = int(frame.mean())
    if avg_pixel_value not in pixel_value_dirs:
        pixel_value_dirs[avg_pixel_value] = os.path.join(video_name, f'{avg_pixel_value}')
        os.makedirs(pixel_value_dirs[avg_pixel_value])

    # 将帧保存为图像文件
    cv2.imwrite(os.path.join(pixel_value_dirs[avg_pixel_value], f'frame_{frame_count:04d}.jpg'), frame)

    frame_count += 1

# 输出不同像素值的图像保存目录
print(f'Pixel value directories: {pixel_value_dirs}')
