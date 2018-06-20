# -*- coding: UTF-8 -*-
from PyQt5.QtWidgets import QApplication,QDialog ,QTabWidget,QTableWidget,\
    QAbstractItemView,QFrame,QPushButton,QHBoxLayout,QLabel,QScrollArea,QVBoxLayout,QWidget

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
import sys
sys.path.append(r'/home/kevin/IFit/Models')
from videoFrameBase import TaiChi,Gymnastics,Dance,LoadVideo,DetailVideos,MainContent
from videoplay import VideoBox

class SportWindow(QWidget):
    def __init__(self):
        super(SportWindow,self).__init__()
        #self.setupUi(self)
        self.resize(1096, 780)
        self.setObjectName('SportWindow')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: white;")

        self.mainContent = MainContent(self)
        self.detailVideos = DetailVideos(self)
        self.videoPlay = VideoBox(self)

        self.setContents()
        self.setCover()
        self.setLists()
        self.setTabs()
        self.setButtons()

    def setContents(self):
        self.mainContents = QTabWidget(self)
        self.mainContents.setGeometry(QtCore.QRect(239, 25, 857, 755))
        self.mainContents.tabBar().setObjectName("mainTab")
        self.mainContents.addTab(self.mainContent, '')
        self.mainContents.addTab(self.detailVideos, '')
        self.mainContents.addTab(self.videoPlay, '')
        self.mainContents.setStyleSheet( '''QTabBar::tab {width: 0; color: transparent;}
                                            QTabWidget::pane{border-color: transparent; }
                                        ''')

    def setCover(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 0, 240, 780))
        self.label.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.label.setText("")
        self.label.setObjectName("label")

        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(630, 10, 61, 16))
        self.label_4.setObjectName("label_4")
        self.label_4.setText("快乐运动")

        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(10, 180, 61, 16))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.label_5.setObjectName("label_5")
        self.label_5.setText("活动中心")

        self.label_6 = QtWidgets.QLabel(self)
        self.label_6.setGeometry(QtCore.QRect(10, 340, 61, 16))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.label_6.setObjectName("label_6")
        self.label_6.setText("本地中心")

    def setLists(self):
        self.activityCenterlist =  QtWidgets.QListWidget(self)

        self.activityCenterlist.setGeometry(QtCore.QRect(10, 210, 201, 81))
        self.activityCenterlist.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.activityCenterlist.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.activityCenterlist.setObjectName("activityCenterlist")
        acList = ['  教学大厅', '  互动中心']
        for i in range(len(acList)):
            self.activityCenterlist.addItem(QtWidgets.QListWidgetItem(acList[i]))
        self.activityCenterlist.itemClicked.connect(self.listClickChangeTab)

        self.localCenterlist = QtWidgets.QListWidget(self)
        self.localCenterlist.setGeometry(QtCore.QRect(10, 370, 201, 101))
        self.localCenterlist.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.localCenterlist.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.localCenterlist.setObjectName("localCenterlist")
        lcList = ['  本地视频', '  我的下载', '  我的记录']
        for i in range(len(lcList)):
            self.localCenterlist.addItem(QtWidgets.QListWidgetItem(lcList[i]))

    def setTabs(self):
        self.indexTable1 = TaiChi(self.mainContent)
        self.indexTable1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.indexTable1.setStyleSheet("background-color: white;")
        self.mainContent.addTab(self.indexTable1, "体操")
        self.q = LoadVideo(self.indexTable1)
        self.q.loadStart()

        self.indexTable2 = Gymnastics(self.mainContent)
        self.indexTable2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.indexTable2.setStyleSheet("background-color: white;")
        self.mainContent.addTab(self.indexTable2, "太极")

        self.indexTable3 = Dance(self.mainContent)
        self.indexTable3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.indexTable3.setStyleSheet("background-color: white;")
        self.mainContent.addTab(self.indexTable3, "舞蹈")

    def setLabels(self):
        """创建标签。"""

        self.logoLabel = QLabel('login')
        self.logoLabel.setObjectName("logoLabel")
        self.logoLabel.setMinimumSize(21, 17)

        self.descriptionLabel = QLabel('descriptionLabel')
        self.descriptionLabel.setObjectName("descriptionLabel")
        self.descriptionLabel.setMinimumSize(21, 17)

    # 布局。
    def setButtons(self):
        """创建所有的按钮。"""

        self.closeButton = QPushButton('×', self)
        self.closeButton.setObjectName("closeButton")
        self.closeButton.setMinimumSize(35, 24)
        self.closeButton.setGeometry(1050,10,35,24)

        self.showmaxButton = QPushButton('□', self)
        self.showmaxButton.setObjectName("maxButton")
        self.showmaxButton.setMaximumSize(35, 24)
        self.showmaxButton.setGeometry(1013, 10, 35, 24)

        self.showminButton = QPushButton('_', self)
        self.showminButton.setObjectName("minButton")
        self.showminButton.setMinimumSize(35, 24)
        self.showminButton.setGeometry(976, 10, 35, 24)

        self.closeButton.clicked.connect(self.close)
        self.showmaxButton.clicked.connect(self.showMaximized)
        self.showminButton.clicked.connect(self.showMinimized)
        # self.loginButton = QPushButton("未登录 ▼", self)
        # self.loginButton.setObjectName("loginButton")
        #
        # self.prevButton = QPushButton("<")
        # self.prevButton.setObjectName("prevButton")
        # self.prevButton.setMaximumSize(28, 22)
        # self.prevButton.setMinimumSize(28, 22)
        #
        # self.nextButton = QPushButton(">")
        # self.nextButton.setObjectName("nextButton")
        # self.nextButton.setMaximumSize(28, 22)
        # self.nextButton.setMinimumSize(28, 22)

    def setLayouts(self):
        """设置布局。"""
        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setSpacing(0)
        self.mainLayout.addWidget(self.logoLabel)
        self.mainLayout.addWidget(self.descriptionLabel)
        self.mainLayout.addSpacing(70)
        self.mainLayout.addWidget(self.prevButton)
        self.mainLayout.addWidget(self.nextButton)
        self.mainLayout.addSpacing(10)
        #self.mainLayout.addWidget(self.searchLine)
        #self.mainLayout.addStretch(1)
        #self.mainLayout.addWidget(self.userPix)
        #self.mainLayout.addSpacing(7)
        self.mainLayout.addWidget(self.loginButton)
        self.mainLayout.addSpacing(7)
        #self.mainLayout.addWidget(self.line1)
        #self.mainLayout.addSpacing(30)
        self.mainLayout.addWidget(self.showminButton)
        self.mainLayout.addWidget(self.showmaxButton)
        self.mainLayout.addSpacing(3)
        self.mainLayout.addWidget(self.closeButton)
        self.setLayout(self.mainLayout)

    def listClickChangeTab(self,item):
        if item.text() == u'  教学大厅':
            self.mainContents.setCurrentIndex(0)

    def mousePressEvent(self, event):
        try:
            if event.button() == Qt.LeftButton:
                self.m_flag = True
                self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
                if event.globalY()-self.y() <= 35:
                    event.accept()
                else:
                    self.m_flag = False
        except:
            print("get pos fail ")

    def mouseMoveEvent(self, event):
        try:
            if Qt.LeftButton and self.m_flag:
                self.move(event.globalPos() - self.m_Position)  # 更改窗口位置
                event.accept()
        except:
            print("move fail")

    def mouseReleaseEvent(self, event):
        self.m_flag = False

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)  # A new instance of QApplication
    main = SportWindow()
    main.show()
    sys.exit(app.exec_())  # and execute the app
