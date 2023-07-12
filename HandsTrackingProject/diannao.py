dict={'pitch': -8, 'roll': 3, 'yaw': 0, 'vgx': 0, 'vgy': 0, 'vgz': 0, 'templ': 88, 'temph': 90, 'tof': 10, 'h': 0, 'bat': 48, 'baro': -75.16, 'time': 0, 'agx': -150.0, 'agy': -61.0, 'agz': -982.0}

status = "俯仰:{pitch}度\n横滚:{roll}度\n偏航:{yaw}度\nx轴速度:{vgx}cm/s\ny轴速度:{vgy}cm/s\nz轴速度:{vgz}cm/s\n主板最低温度:{templ}摄氏度\n主板最高温度:{temph}摄氏度\ntof距离:{tof}厘米\n相对起飞点高度:{h}厘米\n当前电量:{bat}%\n气压计测量高度:{baro}米\n电机运转时间:{time}秒\nx轴加速度:{agx}\ny轴加速度:{agy}\nz轴加速度:{agz}\n"

formatted_string = status.format(**dict)

print(formatted_string)
