import sys
import cv2

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from PyQt5 import uic
from djitellopy import tello
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
import tellohandtrack as tht
import KeyPressModule as kp
import subprocess
import time
import HandTrackingMoudule as htm
import cv2
from djitellopy import tello
from PyQt5.QtGui import QPixmap
#drone_pix = QPixmap("drone_783px_1219960_easyicon.net.png")

import numpy as np



handcontrol_process = None
class MyWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):


        self.mytello = False
        self.handtrack = False



        #加载ui
        self.ui = uic.loadUi("UI01.ui")


        # 提取要操作的控件
        self.label = QLabel()
        self.tello_connect = self.ui.checkBox  # wifi连接tello
        self.tello_status = self.ui.pushButton
        #self.tello_status.setStyleSheet("background-image: url({});".format("drone_783px_1219960_easyicon.net.png"))
        self.battery = self.ui.lcdNumber_3
        self.tellospeed_x = self.ui.lcdNumber_2
        self.tellospeed_y = self.ui.lcdNumber_4
        self.tellospeed_z = self.ui.lcdNumber_5

        self.textwindow = self.ui.textBrowser
        self.cameracontrol = self.ui.pushButton_3
        self.tlcontrol = self.ui.pushButton_5                   #起飞降落
        self.handcontrol = self.ui.pushButton_4  # 手势控制模式
        self.handtrack = self.ui.pushButton_6          #手掌跟踪模式
        self.exitbutton = self.ui.pushButton_7      #退出按钮


        # 绑定信号与槽函数
        self.tello_connect.clicked.connect(self.connect)
        self.tello_status.clicked.connect(self.show_status_window)
        self.cameracontrol.clicked.connect(self.start_camera)
        self.tlcontrol.clicked.connect(self.takeoff_land)        #起飞降落

        self.handtrack.clicked.connect(self.hand_track)     #手掌跟踪
        self.handcontrol.clicked.connect(self.hand_control)  #手势控制
        self.exitbutton.clicked.connect(self.exit_app)


        #Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.me = tello.Tello()

    def connect(self):
        #print("oooook")
        if self.tello_connect.isChecked():
            # 无人机初始化
            #self.me = tello.Tello()
            self.me.connect()
            self.textwindow.setText("tello已连接！\n" )

            self.timer_0 = QTimer()
            self.timer_0.timeout.connect(self.updateStatus)
            self.timer_0.start(1000)  # 每100ms更新一次状态

            self.mytello = True
            self.tello_status.setText('0')
        else:
            self.textwindow.setText("tello连接断开！\n")
            self.mytello = False


    def updateStatus(self):

        self.battery.display(self.me.get_battery())  # 显示电量
        self.tellospeed_x.display(self.me.get_speed_x())  # 显示速度
        self.tellospeed_y.display(self.me.get_speed_y())  # 显示速度
        self.tellospeed_z.display(self.me.get_speed_z())  # 显示速度

        #print(state)

    def show_status_window(self):
        if self.mytello is True:
            # 创建一个文本窗口
            if self.tello_status.text()=='0':
                self.tello_status.setText('1')
                # self.textWindow = TextWindow_0(self)
                # self.textWindow.show()
                self.setGeometry(350, 350, 250, 150)
                self.setWindowTitle('无人机状态')
                # 创建一个文本编辑框
                self.textedit = QTextEdit(self)
                # self.setCentralWidget(self.textedit)
                self.timer_1 = QTimer()
                self.timer_1.timeout.connect(self.show_tello_status)
                self.timer_1.start(1000)  # 每100ms更新一次状态
            elif self.tello_status.text()=='1':
                self.tello_status.setText('0')
                if self.handtrack.text()=="关闭手掌跟踪":
                    self.textwindow.setText("手部跟踪模式已开启:\n聚焦pygame对话框可以对无人机进行键盘控制：\nE:起飞\nQ:降落\nW:上升\nS：下降\nA:左旋\nD：右旋\n⬆️：向前\n⬇️：向后\n⬅️：向左\n➡️：向右")
                elif self.handcontrol.text()=="关闭手势控制":
                    self.textwindow.setText("手势控制模式已开启：\n")
                else:self.textwindow.setText("")

            #else:self.tello_status.setText('0')

        else:self.textwindow.setText("tello未连接！请先连接无人机！\n")

    # def enableButton(self):
    #     # 当文本窗口关闭时调用，启用按钮
    #     self.tello_status.setEnabled(True)

    def show_tello_status(self):
        if self.tello_status.text() == '1':
            state = self.me.get_current_state()
            status = "俯仰:{pitch}度\n横滚:{roll}度\n偏航:{yaw}度\nx轴速度:{vgx}cm/s\ny轴速度:{vgy}cm/s\nz轴速度:{vgz}cm/s\n主板最低温度:{templ}摄氏度\n主板最高温度:{temph}摄氏度\ntof距离:{tof}厘米\n相对起飞点高度:{h}厘米\n当前电量:{bat}%\n气压计测量高度:{baro}米\n电机运转时间:{time}秒\nx轴加速度:{agx}\ny轴加速度:{agy}\nz轴加速度:{agz}\n"
            state = status.format(**state)
            #print(str(state))
            self.textwindow.setText(str(state))


    def takeoff_land(self):
        if self.mytello is True:
            if  self.tlcontrol.text()=="起飞" :
                self.tlcontrol.setText("降落")
                self.me.takeoff()
                self.textwindow.setText("飞行中\n")
            elif self.tlcontrol.text() == "降落":
                self.me.land()
                self.tlcontrol.setText("起飞")
                self.textwindow.setText("已降落\n")
        else:
            self.textwindow.setText("tello未连接！请先连接无人机！\n")

    def tl_check(self):
        if self.mytello is True:
            state = self.me.get_current_state()
            print(state)
            if state['time'] == 0:
                self.tlcontrol.setText("起飞")
                return 0
            if state['time'] != 0:
                self.tlcontrol.setText("降落")
                return 1
        else:return 0


    def start_camera(self):
        if self.mytello is True:

            if not self.timer.isActive():
                self.timer.start(5)
                self.me.streamon()
                self.cameracontrol.setText("关闭摄像头")
                self.textwindow.setText("摄像头已开启\n")
                #self.camera = self.me.get_frame_read().frame
            else:
                self.timer.stop()
                self.me.streamoff()
                self.cameracontrol.setText("开启摄像头")
                self.textwindow.setText("摄像头已关闭\n")
        else:self.textwindow.setText("tello未连接！请先连接无人机！\n")

    def update_frame(self):
        frame_read = self.me.get_frame_read()
        frame = frame_read.frame
        if frame is not None:
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.flip(frame, 1)  # 水平镜像
                frame = cv2.resize(frame, (360, 240))
                cv2.imshow("Image", frame)
                cv2.waitKey(1)

    def closeEvent(self, event):
        self.timer.stop()
        #self.camera.release()


#手掌跟踪模式

    def hand_track(self):
        if self.mytello is True:
            # if self.handcontrol.text()=="关闭手势控制":
            #     self.handcontrol.setText()="开启手势控制"
            if self.handtrack.text()=="开启手掌跟踪":
                self.handtrack.setText("关闭手掌跟踪")
                self.textwindow.setText("手部跟踪模式已开启:\n聚焦pygame对话框可以对无人机进行键盘控制：\nE:起飞\nQ:降落\nW:上升\nS：下降\nA:左旋\nD：右旋\n⬆️：向前\n⬇️：向后\n⬅️：向左\n➡️：向右")
                w, h = 360, 240 #tello摄像头分辨率
                fbRange = [20000, 24000]#矩形框的面积范围
                #pid = [0.4, 0.4, 0]
                PID_lr = [0.1, 0.4, 0.1]
                PID_ud = [0.1, 0.4, 0.1]
                PID_yv = [0.1, 0.4, 0.1]
                PID_fb = [0.002, 0.05, 0.1]
                #pid =PID_ud,PID_yv,PID_lr,PID_fb
                #pError = 0

                lmList = []

                detector = htm.handDetector(detectionCon=0.7)  # 定义一个手部跟踪对象,置信度0.7
                kp.init()

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
                        yv = speed
                    elif kp.getKey("d"):
                        yv = -speed

                    if kp.getKey("q"): self.me.land()

                    if kp.getKey("e"): self.me.takeoff()

                    return [lr, fb, ud, yv]

                def findHand(img, lmList):
                    myHandList = []
                    myHandListArea = []
                    lmList = detector.findPosition(img, draw=False)
                    X = []
                    Y = []
                    for i in range(20):  # 遍历20个点的坐标，找到最大点以及最小点使得手的框选取最大值
                        X.append(lmList[i][1])
                        Y.append(lmList[i][2])
                    x1, y1 = np.min(X), np.min(Y)
                    x2, y2 = np.max(X), np.max(Y)
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 厚度为2的绿色长方体
                    cv2.rectangle(img,(125,125),(235,235),(0,0,255),2)#红色框
                    cx, cy = 0.5 * (x1 + x2), 0.5 * (y1 + y2)
                    area = (x1 - x2) * (y1 - y2)#绿色矩形框面积
                        #print(cx, cy)
                    cv2.circle(img, (int(cx), int(cy)), 5, (255, 0, 0), cv2.FILLED)#矩形框中央红色圆点
                    cv2.circle(img,(180,180),6,(0,0,255))
                    myHandList.append([cx, cy])
                    myHandListArea.append(area)

                    if len(myHandListArea) != 0:
                            # i =myHandListArea.index(max(myHandListArea))#i是矩形框最大值的索引
                        return img, [[cx, cy], myHandListArea[0]]  # 返回面部最大值
                    else:
                        return img, [[0, 0], 0]

                def trackHand(info, w, h,PID_lr,PID_ud,PID_fb,PID_yv):  # PID手部追踪算法
                    area = info[1]  # 面积
                    print(area)
                    x, y = info[0]  # 中心坐标
                    class PID:
                        def __init__(self, Kp, Ki, Kd):
                            self.Kp = Kp  # 比例控制器系数
                            self.Ki = Ki  # 积分控制器系数
                            self.Kd = Kd  # 微分控制器系数
                            self.last_error = 0  # 上一次的误差
                            self.integral = 0  # 积分项
                        def update(self, setpoint, measured_value, dt):
                            error = setpoint - measured_value  # 当前误差
                            # print(f"error：{error:.4f}", end='  ')
                            # print(f'self.integral：{self.integral:.4f}', end='  ')
                            self.integral += error * dt  # 累计误差
                            # print(f'累计：{self.integral:.4f}', end='  ')
                            derivative = (error - self.last_error) / dt  # 当前误差变化率
                            # print(f'变化率：{derivative:.4f}', end='  ')
                            output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative  # PID控制器输出
                            # print(f'pid输出：{output:.4f}', end='  ')
                            self.last_error = error  # 保存当前误差作为上一次误差
                            # print(f'保存误差：{self.last_error:.4f}', end='  ')
                            return output

                    def pidcontroller(setpoint, measured_value, PID_0, dt, limit):  # 目标值，测量值，PID参数，微分量，速度上限
                        pid = PID(PID_0[0], PID_0[1], PID_0[2])
                        output = pid.update(setpoint, measured_value, dt)
                        output = int(np.clip(output, -limit, limit))  # 设置速度上限
                        return output
                    #对四个方向进行pid控制
                    lr = pidcontroller(w // 2, x, PID_lr, 1, 10)
                    ud = pidcontroller(h // 2, y, PID_ud, 1, 20)
                    yv = pidcontroller(w // 2, x, PID_yv, 1, 30)
                    fb = pidcontroller(120, area//100, PID_fb, 1, 20)
                    self.me.send_rc_control(lr, fb, ud, yv)
                    return

                while self.handtrack.text()=="关闭手掌跟踪":
                            # success,img = cap.read()
                    img = self.me.get_frame_read().frame
                    img = cv2.flip(img, 1)  # 水平镜像
                    img = cv2.resize(img, (360, 360))  # 调整tello分辨率
                    img = detector.findHands(img, lmList)  # 调用方法；将拍摄图像转换成带有手部标记的图像
                    lmList = detector.findPosition(img, draw=False)
                        #print(lmList)
                    if len(lmList) != 0:
                                # img = cv2.flip(img, 0)  # 翻转
                        img, info = findHand(img, lmList)
                        trackHand(info, w, h,PID_lr,PID_ud,PID_fb,PID_yv)
                            #print("Area", info[1], "Center", info[0])
                    else:self.me.send_rc_control(0, 0, 0, 0)#悬停

                    cv2.imshow("HandTracking", img)
                    vals = getKeyboardInput()
                    cv2.waitKey(1)
            if self.handtrack.text() == "关闭手掌跟踪":
                #print("tianna")
                self.handtrack.setText("开启手掌跟踪")
                self.textwindow.setText("手部跟踪模式已关闭")
        else:self.textwindow.setText("tello未连接！请先连接无人机！\n")


#手势控制模式
    def hand_control(self):
        if self.mytello is True:
            # if self.handtrack.text()=="关闭手掌跟踪":
            #     self.handtrack.setText("开启手掌跟踪")
            if self.handcontrol.text()=="开启手势控制":
                self.handcontrol.setText("关闭手势控制")
                self.textwindow.setText("手势控制已开启:\n")
                #电脑摄像头初始化
                wCam, hCam = 640, 480
                cap = cv2.VideoCapture(0)
                cap.set(3, wCam)
                cap.set(4, hCam)
                pTime = 0
                # 屏幕遥控器初始化：
                LeftPx, LeftPy = int(3 * wCam / 4), int(0.66 * hCam)
                RighPx, RighPy = int(wCam / 4), int(0.66 * hCam)
                PointRange = 60
                # 起降按钮大小：
                tlPw, tlPh = 64, 48
                # 起飞按钮(以左上角为初始点）
                tfP1x, tfP1y = 600, 30
                tfP2x, tfP2y = tfP1x - tlPw, tfP1y + tlPh
                takeoffcx, takeoffcy = 0.5 * (tfP1x + tfP2x), 0.5 * (tfP1y + tfP2y)
                # 降落按钮(以左上角为初始点）
                lP1x, lP1y = 104, 30
                lP2x, lP2y = lP1x - tlPw, lP1y + tlPh
                launchcx, launchcy = 0.5 * (lP1x + lP2x), 0.5 * (lP1y + lP2y)
                # 标志位
                takeoff = self.tl_check()
                #print('aaaaaaaaaaaaaaaaaaaaa',takeoff)
                flag = 0

                # 速度命令初始化
                lr, fb, ud, yv = 40, 40, 25, 30

                detector = htm.handDetector(detectionCon=0.7)  # 定义一个手部跟踪对象,置信度0.7

                while self.handcontrol.text()=="关闭手势控制":

                    success, img = cap.read()
                    img = cv2.flip(img, 1)  # 水平镜像
                    img = detector.findHands(img)  # 调用方法；将拍摄图像转换成带有手部标记的图像
                    #telloimg = self.me.get_frame_read().frame  # 调用tello摄像头
                    #telloimg = cv2.resize(telloimg, (360, 240))  # 调整图像大小
                    lmList = detector.findPosition(img, draw=False)
                    # 显示手势控制按钮

                    # 起飞按钮
                    if takeoff == 1:
                        cv2.rectangle(img, (tfP1x + 4, tfP1y - 3), (tfP2x - 4, tfP2y + 3), (0, 255, 0), cv2.FILLED)
                        cv2.rectangle(img, (lP1x, lP1y), (lP2x, lP2y), (128, 128, 128), cv2.FILLED)
                        cv2.putText(img, f'takeoff', (500, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                        cv2.putText(img, f'land', (25, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (128, 128, 128), 1)
                        # 左右遥杆：
                        cv2.circle(img, (LeftPx, LeftPy), 10, (0, 255, 0), cv2.FILLED)
                        cv2.circle(img, (LeftPx, LeftPy), PointRange, (0, 255, 0), 3)
                        cv2.circle(img, (RighPx, RighPy), 10, (0, 255, 0), cv2.FILLED)
                        cv2.circle(img, (RighPx, RighPy), PointRange, (0, 255, 0), 3)
                    else:
                        cv2.rectangle(img, (tfP1x, tfP1y), (tfP2x, tfP2y), (128, 128, 128), cv2.FILLED)
                        cv2.rectangle(img, (lP1x + 4, lP1y - 3), (lP2x - 4, lP2y + 3), (255, 0, 0), cv2.FILLED)
                        cv2.putText(img, f'takeoff', (500, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (128, 128, 128), 1)
                        cv2.putText(img, f'land', (25, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

                        # 左右遥杆：
                        cv2.circle(img, (LeftPx, LeftPy), 10, (128, 128, 128), cv2.FILLED)
                        cv2.circle(img, (LeftPx, LeftPy), PointRange, (128, 128, 128), 3)
                        cv2.circle(img, (RighPx, RighPy), 10, (128, 128, 128), cv2.FILLED)
                        cv2.circle(img, (RighPx, RighPy), PointRange, (128, 128, 128), 3)

                    if len(lmList) != 0:
                        cv2.circle(img, (lmList[8][1], lmList[8][2]), 10, (0, 0, 255), cv2.FILLED)  # 显示手指
                        # print(lmList[8][1], lmList[8][2])
                        val = [0, 0, 0, 0]
                        # 点击起飞降落按钮
                        if (takeoffcy - lmList[8][2]) ** 2 + (takeoffcx - lmList[8][1]) ** 2 < 13 ** 2:
                            takeoff = 1
                            if flag == 0:
                                self.me.takeoff()
                                flag = 1
                            # cv2.waitKey(50)
                            # print("起飞")
                        if (launchcy - lmList[8][2]) ** 2 + (launchcx - lmList[8][1]) ** 2 < 13 ** 2:
                            takeoff = 0
                            self.me.land()
                            flag = 0
                            # print("降落")

                        # 控制遥杆
                        if (LeftPy - lmList[8][2]) ** 2 + (LeftPx - lmList[8][1]) ** 2 < PointRange ** 2:
                            cv2.circle(img, (lmList[8][1], lmList[8][2]), 10, (255, 255, 0), cv2.FILLED)  # 指变色
                            cv2.circle(img, (LeftPx, LeftPy), 10, (255, 255, 0), cv2.FILLED)
                            cv2.circle(img, (LeftPx, LeftPy), PointRange, (255, 255, 0), 3)
                            cv2.line(img, (LeftPx, LeftPy), (lmList[8][1], lmList[8][2]), (255, 255, 0), 3)  # 杆指间画线
                            direction = abs((lmList[8][2] - LeftPy + 0.001) / (lmList[8][1] - LeftPx + 0.001))  # 计算指杆斜率绝对值

                            if lmList[8][2] < LeftPy:  # 手指在上方
                                if lmList[8][1] < LeftPx:  # 手指在第一象限
                                    if direction < 1:
                                        print("向左")
                                        val[0] = -lr
                                        # self.me.send_rc_control(-lr, 0, 0, 0)
                                    else:
                                        print("向前")
                                        val[1] = fb
                                        # self.me.send_rc_control(0, fb, 0, 0)
                                else:  # 手指在第四象限
                                    if direction < 1:
                                        print("向右")
                                        val[0] = lr
                                        # self.me.send_rc_control(lr, 0, 0, 0)
                                    else:
                                        print("向前")
                                        val[1] = fb
                                        # self.me.send_rc_control(0, fb, 0, 0)
                            else:  # 手指在下方
                                if lmList[8][1] < LeftPx:  # 手指在第二象限
                                    if direction < 1:
                                        print("向左")
                                        val[0] = -lr
                                        # self.me.send_rc_control(-lr, 0, 0, 0)
                                    else:
                                        print("向后")
                                        val[1] = -fb
                                        # self.me.send_rc_control(0, -fb, 0, 0)
                                else:  # 手指在第四象限
                                    if direction < 1:
                                        print("向右")
                                        val[0] = lr
                                        # self.me.send_rc_control(lr, 0, 0, 0)
                                    else:
                                        print("向后")
                                        val[1] = -fb
                                        # self.me.send_rc_control(0, -fb, 0, 0)
                        elif (RighPy - lmList[8][2]) ** 2 + (RighPx - lmList[8][1]) ** 2 < PointRange ** 2:
                            cv2.circle(img, (lmList[8][1], lmList[8][2]), 10, (255, 255, 0), cv2.FILLED)  # 指变色
                            cv2.circle(img, (RighPx, RighPy), 10, (255, 255, 0), cv2.FILLED)
                            cv2.circle(img, (RighPx, RighPy), PointRange, (255, 255, 0), 3)
                            cv2.line(img, (RighPx, RighPy), (lmList[8][1], lmList[8][2]), (255, 255, 0), 3)  # 杆指间画线
                            # 操作右遥杆发出命令：
                            direction = abs((lmList[8][2] - RighPy + 0.001) / (lmList[8][1] - RighPx + 0.001))  # 计算指杆斜率绝对值
                            if lmList[8][2] < RighPy:  # 手指在上方
                                if lmList[8][1] < RighPx:  # 手指在第一象限
                                    if direction < 1:
                                        print("向左转向")
                                        val[3] = yv
                                        # self.me.send_rc_control(0, 0, 0, yv)
                                    else:
                                        print("上升")
                                        val[2] = ud
                                        # self.me.send_rc_control(0, 0, ud, 0)
                                else:  # 手指在第四象限
                                    if direction < 1:
                                        print("向右转向")
                                        val[3] = -yv
                                        # self.me.send_rc_control(0, 0, 0, -yv)
                                    else:
                                        print("上升")
                                        val[2] = ud
                                        # self.me.send_rc_control(0, 0, ud, 0)
                            else:  # 手指在下方
                                if lmList[8][1] < RighPx:  # 手指在第二象限
                                    if direction < 1:
                                        print("向左转向")
                                        val[3] = yv
                                        # self.me.send_rc_control(0, 0, 0, yv)
                                    else:
                                        print("下降")
                                        val[2] = -ud
                                        # self.me.send_rc_control(0, 0, -ud, 0)
                                else:  # 手指在第四象限
                                    if direction < 1:
                                        print("向右转向")
                                        val[3] = -yv
                                        # self.me.send_rc_control(0, 0, 0, -yv)
                                    else:
                                        print("下降")
                                        val[2] = -ud
                                        # self.me.send_rc_control(0, 0, -ud, 0)
                        else:
                            print("悬停")
                        self.me.send_rc_control(val[0], val[1], val[2], val[3])

                        # for shizhi in range(5,9):
                        # cv2.circle(img, (lmList[shizhi][1], lmList[shizhi][2]), 10, (255, 0, 255), cv2.FILLED)
                        # print(lmList[shizhi][1],lmList[shizhi][2])
                        # print("##########")
                        # direction = (lmList[12][2]-lmList[9][2])//(lmList[12][1]-lmList[9][1])
                        # print(direction)

                    # 帧率显示
                    cTime = time.time()
                    fps = 1 / (cTime - pTime)
                    pTime = cTime

                    # 在img上实时显示帧率：坐标：（10,70），字体，比例，颜色，粗细
                    cv2.putText(img, f'FPS:{int(fps)}', (270, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

                    cv2.imshow("手势控制模式", img)
                    #cv2.imshow("Tello", telloimg)

                    cv2.waitKey(1)

            if self.handcontrol.text()=="关闭手势控制":
                print("weishq")
                self.handcontrol.setText("开启手势控制")
                self.textwindow.setText("手势控制模式已关闭")
        else:self.textwindow.setText("tello未连接！请先连接无人机！\n")


    def keyPressEvent(self, event):
       # print(event.key)
        if self.keyboard.isChecked():
            print(12345)
            if event.key() == QtCore.Qt.Key_Up:
                self.me.send_rc_control(0, 0, -50, 0)
                self.textwindow.setText("上升")
            elif event.key() == Qt.Key_Down:
                self.me.send_rc_control(0, 0, 50, 0)
                self.textwindow.setText("下降")
            elif event.key() == Qt.Key_Left:
                self.me.send_rc_control(0, 0, 0, -50)
                self.textwindow.setText("左旋")
            elif event.key() == Qt.Key_Right:
                self.me.send_rc_control(0, 0, 0, 50)
                self.textwindow.setText("右旋")
            elif event.key() == Qt.Key_W:
                self.me.send_rc_control(0, -50, 0, 0)
                self.textwindow.setText("前进")
            elif event.key() == Qt.Key_S:
                self.me.send_rc_control(0, 50, 0, 0)
                self.textwindow.setText("后退")
            elif event.key() == Qt.Key_A:
                self.me.send_rc_control(-50, 0, 0, 0)
                self.textwindow.setText("向左")
            elif event.key() == Qt.Key_D:
                self.me.send_rc_control(50, 0, 0, 0)
                self.textwindow.setText("向右")
            elif event.key() == Qt.Key_Q:
                self.me.takeoff()
                self.textwindow.setText("起飞")
            elif event.key() == Qt.Key_E:
                self.me.land()
                self.textwindow.setText("降落")

    def exit_app(self):
        # 退出程序
        self.me.streamoff()
        self.me.land()
        self.me.end()
        sys.exit()

class TextWindow_0(MyWindow):
    def __init__(self,parent):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(350, 350, 250, 150)
        self.setWindowTitle('无人机状态')
        # 创建一个文本编辑框
        self.textedit = QTextEdit(self)
        #self.setCentralWidget(self.textedit)

        self.timer_1 = QTimer()
        self.timer_1.timeout.connect(self.show_tello_status)
        self.timer_1.start(1000)  # 每100ms更新一次状态

    def show_tello_status(self):
        super().connect()
        state = self.me.get_current_state()
        self.textedit.setText(str(state))



    def closeEvent(self, event):
        # 当用户关闭窗口时调用，启用父窗口的按钮
        #MyWindow.enableButton(self)
        super().init_ui()
        self.tello_status.setText("0")
        #event.accept()
        #print("已开启")


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = MyWindow()
    # 展示窗口
    w.ui.show()
    w.setFocus()
    app.exec()
