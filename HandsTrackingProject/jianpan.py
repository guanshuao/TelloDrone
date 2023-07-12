import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QCheckBox
from PyQt5.QtCore import Qt
from djitellopy import Tello

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.drone = Tello()
        self.drone.connect()

    def initUI(self):
        self.setWindowTitle('PyQt5 UI')
        self.setGeometry(300, 300, 300, 200)

        self.label = QLabel(self)
        self.label.setText("控制关闭")
        self.label.move(50, 50)

        self.checkbox = QCheckBox('Checkbox', self)
        self.checkbox.move(50, 100)
        self.checkbox.stateChanged.connect(self.on_clicked)

    def on_clicked(self):
        if self.checkbox.isChecked():
            self.label.setText("控制开启")
            self.setFocus()
        else:
            self.label.setText("控制关闭")

    def keyPressEvent(self, event):
        if self.checkbox.isChecked():
            if event.key() == Qt.Key_Up:
                self.drone.send_rc_control(0, 0, +50, 0)
            elif event.key() == Qt.Key_Down:
                self.drone.send_rc_control(0, 0, -50, 0)
            elif event.key() == Qt.Key_Left:
                self.drone.left(50)
            elif event.key() == Qt.Key_Right:
                self.drone.right(50)
            elif event.key() == Qt.Key_W:
                self.drone.forward(50)
            elif event.key() == Qt.Key_S:
                self.drone.backward(50)
            elif event.key() == Qt.Key_A:
                self.drone.left(50)
            elif event.key() == Qt.Key_D:
                self.drone.right(50)
            elif event.key() == Qt.Key_R:
                self.drone.takeoff()
            elif event.key() == Qt.Key_F:
                self.drone.land()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
