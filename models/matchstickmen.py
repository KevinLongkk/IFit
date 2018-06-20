
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtWidgets import QApplication,QLabel,QFrame
from PyQt5.QtGui import QPixmap,QImage
import sys
from cv2 import *
from videoFrameBase import ScrollArea

class MatchStickMen(QFrame):
    def __init__(self):
        super(MatchStickMen,self).__init__()
        self.resize(640, 480)
        self.setStyleSheet("background-color:black")
        self.image = QPixmap('game/1.png')
        self.bgLabel = QLabel(self)
        self.bgLabel.setMinimumSize(640,480)
        self.bgLabel.setPixmap(self.image)


if __name__ == "__main__":
    app = QApplication(sys.argv)  # A new instance of QApplication
    main = MatchStickMen()
    main.show()
    sys.exit(app.exec_())  # and execute the app