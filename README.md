# TelloDrone——基于 Tello 无人机的智能人机交互平台

## 0.0 介绍

本项目为西北工业大学开设的《智能人机交互与视觉感知综合设计》（U08M81002）所对应的课程设计，此平台基于 Python 语言开发，可用于控制大疆公司的 Tello 系列无人机，并利用无人机的摄像头、红外等传感器完成一系列视觉功能，包括：目标检测与跟踪（亮黄色物体、人脸、肢体等）、手势控制、体态控制等，也可控制 Tello 进行拍照、以及做出一些花式动作。

## 0.1 安装环境

本项目开发环境为 Python 和 QtDesigner，主要在 Windows11 下进行开发，可移植到其他系统上。

1. 创建虚拟环境，使用如下命令：

```shell
conda create -n tello python=3.8
```

2. 打开刚刚创建的虚拟环境：

```shell
conda activate tello
```

3. 安装依赖库：

```shell
pip install -r requirements.txt
```
### 0.3 项目结构

本项目使用模块化编程的思想，路径结构如下：

``requirements.txt``：此项目依赖的库

``README.md``：项目说明文档

``BodyFollowing``：用以实现肢体追踪

``ColorObjectTracking``：实现物体追踪（默认为亮黄色物体，可调）

``Demo``：DJI 官方提供的参考样例，包括最基本的起降、图传、控制功能，对此项目感兴趣的开发者可以参考

``FaceFollowing``：识别画面中的人脸并跟踪

``HandGestureControl``：识别画面中的手势并控制 Tello

``Mapping``：操纵无人机并画出轨迹

``ObjectDetection``：用键盘控制无人机的同时，将画面进行实时的目标检测

``pic``：图床

``SelfieDrone``：用姿势控制无人机，并借助肢体语言实现自拍

``Surveillance``：最基本的监视器模块

## 0.4 硬件平台

Tello无人机是大疆创新与Intel公司合作开发的一款小型无人机，主要面向初学者和儿童。Tello无人机体积小巧，重量轻，携带方便，可在室内外飞行，可通过手机APP或者编程语言控制，具有多种飞行模式，可实现多种功能，是一款性价比较高的无人机。

特别值得一提的是，Tello无人机的价格仅为 99 美元，而且其拥有多种编程语言的 SDK，包括 Python、Java、Scratch 等，因此，Tello 无人机是一款非常适合初学者的无人机。

## 0.5 使用说明

