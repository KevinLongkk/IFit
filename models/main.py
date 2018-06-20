# -*- coding: UTF-8 -*-
from PyQt5.QtWidgets import QApplication,QDialog ,QTabWidget,QTableWidget,\
    QAbstractItemView,QFrame,QPushButton,QHBoxLayout,QLabel,QScrollArea,QVBoxLayout,QWidget

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtGui import QCursor,QIcon,QPixmap,QImage
import sys
sys.path.append(r'/home/kevin/IFit/Models')

from videoFrameBase import TaiChi,Gymnastics,Dance,LoadVideo,DetailVideos,MainContent,\
                            RecommendVideo,PlayGame,PlayGameList,DownloadPage,MyVideoPage,\
                            MyGamePage,LoadGame

from videoplay import VideoBox

class SportWindow(QWidget):
    def __init__(self):
        super(SportWindow,self).__init__()
        #self.setupUi(self)
        self.resize(900, 670)
        self.setObjectName('SportWindow')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color:white")#qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #6A848C, stop: 1.0 #0F9EAF)

        self.mainContent = MainContent(self)
        self.detailVideos = DetailVideos(self)
        self.playGame = PlayGame(self)
        self.videoPlay = VideoBox(self)
        self.playGameList = PlayGameList(self)
        self.myVideoPage = MyVideoPage(self)
        self.downloadPage = DownloadPage(self)
        self.myGamePage = MyGamePage(self)

        self.windowSizeChange=1

        self.setContents()
        self.setGamelist()
        self.setCover()
        self.setLogin()
        self.setLists()
        self.setTabs()
        self.setButtons()
        self.setLayouts()

    #设置内容到tab
    def setContents(self):
        self.mainContents = QTabWidget(self)
       # self.mainContents.setGeometry(QtCore.QRect(239, 25, 857, 755))
        self.mainContents.tabBar().setObjectName("mainTab")

        self.mainContents.addTab(self.mainContent, '')
        self.mainContents.addTab(self.detailVideos, '')
        self.mainContents.addTab(self.videoPlay, '')
        self.mainContents.addTab(self.playGameList, '')
        self.mainContents.addTab(self.playGame, '')
        self.mainContents.addTab(self.myVideoPage, '')
        self.mainContents.addTab(self.downloadPage, '')
        self.mainContents.addTab(self.myGamePage, '')

        self.mainContents.setStyleSheet( '''QTabBar::tab {width: 0; color: transparent;}
                                            QTabWidget::pane{border-color: transparent; }
                                        ''')

    def setGamelist(self):
        self.lg  = LoadGame(self.playGameList)
        self.lg.loadStart()

    #设置登录窗口
    def setLogin(self):
        self.loginBtm = QPushButton(self)
        self.loginBtm.setStyleSheet("background-color: white")
        self.loginBtm.setGeometry(QtCore.QRect(55, 80, 50, 50))

        self.loginNamelabel = QLabel(self)
        self.loginNamelabel.setStyleSheet("background-color: transparent")
        self.loginNamelabel.setGeometry(QtCore.QRect(55, 130, 50, 25))
        self.loginNamelabel.setText("请登录")

    #设置封面
    def setCover(self):
        self.mainlabel = QtWidgets.QLabel(self)
        #self.mainlabel.setGeometry(QtCore.QRect(0, 0, 160, 780))
        self.mainlabel.setMinimumWidth(160)
        self.mainlabel.setStyleSheet('''
        QLabel
        {
            background-color:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #6A848C, stop: 1.0 #0F9EAF);
        }
        ''')

        self.mainlabel.setText("")
        self.mainlabel.setObjectName("label")

        self.nullLabel = QLabel(self)
        self.nullLabel.setObjectName("nullLabel")
        self.nullLabel.setMaximumSize(160, 30)
        self.nullLabel.setStyleSheet('''QLabel{ background-color:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #6A848C); } ''')
       # self.nullLabel.setText("         ")



        self.softIcon = QLabel(self)
        self.softIcon.setGeometry(QtCore.QRect(10, 1, 47, 47))
        self.softIcon.setMaximumSize(47,47)
        self.softIcon.setStyleSheet("background-color:transparent")
        self.softIcon.setObjectName("softIcon")
        self.iconImage = QImage('Icon/ifit.png')
        image = self.iconImage.scaled(38,38)
        self.softIcon.setPixmap(QPixmap.fromImage(image))

        self.softName = QLabel(self)
        self.softName.setGeometry(QtCore.QRect(54, 18, 61, 16))
        self.softName.setText("IFIT")
        self.softName.setMaximumSize(160,30)
        self.softName.setStyleSheet('''
                                      QLabel{
                                        background-color:transparent;
                                        font:25px;
                                        font-family:"Dejavu";
                                         color:black; 
                                      } ''' )

        self.titleLayout = QHBoxLayout()
        #self.titleLayout.addWidget(self.softIcon)
        self.titleLayout.addWidget(self.nullLabel)

        self.titletransparentLabel = QLabel()
        self.titletransparentLabel.setStyleSheet('''
                                      QLabel{
                                        background-color:white;
                                      }
                                    ''' )
        self.titleLayout.addWidget(self.titletransparentLabel)


    #设置左边list
    def setLists(self):
        self.activityCenterlist =  QtWidgets.QListWidget(self)

        self.activityCenterlist.setGeometry(QtCore.QRect(0, 210, 160, 200))
        self.activityCenterlist.setStyleSheet("")
        self.activityCenterlist.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.activityCenterlist.setObjectName("activityCenterlist")
        self.activityCenterlist.setSpacing(4)
        self.activityCenterlist.setStyleSheet('''
                                                    QListWidget
                                                    {
                                                    background-color: transparent;
                                                    font:16px;
                                                    color:white;
                                                    }
                                                    ''')
        acList = ['        教学大厅',
                  '        游戏中心',
                  '        本地视频',
                  '        我的下载',
                  '        我的记录',
                  '        我的游戏'
                  ]
        for i in range(len(acList)):
            self.activityCenterlist.addItem(QtWidgets.QListWidgetItem(acList[i]))
        self.activityCenterlist.itemClicked.connect(self.listClickChangeTab)

        # self.localCenterlist = QtWidgets.QListWidget(self)
        # self.localCenterlist.setGeometry(QtCore.QRect(10, 370, 150, 101))
        # self.localCenterlist.setStyleSheet("background-color: rgb(85, 170, 255);")
        # self.localCenterlist.setFrameShape(QtWidgets.QFrame.NoFrame)
        # self.localCenterlist.setObjectName("localCenterlist")
        # lcList = ['  本地视频', '  我的下载', '  我的记录']
        # for i in range(len(lcList)):
        #     self.localCenterlist.addItem(QtWidgets.QListWidgetItem(lcList[i]))

    #设置各种运动tab
    def setTabs(self):
        self.recommendTab = RecommendVideo(self.mainContent)
        self.recommendTab.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.recommendTab.setStyleSheet("background-color: white;")
        self.mainContent.addTab(self.recommendTab, "推荐")
        self.q = LoadVideo(self.recommendTab)
        self.q.loadStart()

        self.indexTable1 = TaiChi(self.mainContent)
        self.indexTable1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.indexTable1.setStyleSheet("background-color: white;")
        self.mainContent.addTab(self.indexTable1, "体操")


        self.indexTable2 = Gymnastics(self.mainContent)
        self.indexTable2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.indexTable2.setStyleSheet("background-color: white;")
        self.mainContent.addTab(self.indexTable2, "太极")

        self.indexTable3 = Dance(self.mainContent)
        self.indexTable3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.indexTable3.setStyleSheet("background-color: white;")
        self.mainContent.addTab(self.indexTable3, "舞蹈")

    #设置各种关闭按钮
    def setButtons(self):
        """创建所有的按钮。"""

        self.closeButton = QPushButton('×', self)
        self.closeButton.setObjectName("closeButton")
        self.closeButton.setMaximumSize(35, 24)
        self.closeButton.setStyleSheet('''
                                        QPushButton{
                                            background-color:#6A848C;
                                        }
                                        ''')
       # self.closeButton.setGeometry(1050,10,35,24)

        self.showmaxButton = QPushButton('□', self)
        self.showmaxButton.setObjectName("maxButton")
        self.showmaxButton.setMaximumSize(35, 24)
        self.showmaxButton.setStyleSheet('''
                                                QPushButton{
                                                    background-color:#6A848C;
                                                }
                                                ''')
       # self.showmaxButton.setGeometry(1013, 10, 35, 24)

        self.showminButton = QPushButton('_', self)
        self.showminButton.setObjectName("minButton")
        self.showminButton.setMaximumSize(35, 24)
        self.showminButton.setStyleSheet('''
                                                QPushButton{
                                                    background-color:#6A848C;
                                                }
                                                ''')
       # self.showminButton.setGeometry(976, 10, 35, 24)

        self.titleLayout.addWidget(self.showminButton)
        self.titleLayout.addWidget(self.showmaxButton)
        self.titleLayout.addWidget(self.closeButton)

        self.closeButton.clicked.connect(self.close)
        self.showmaxButton.clicked.connect(self.setMaxWinodw)
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

    #设置最大化窗口
    def setMaxWinodw(self):
        if self.windowSizeChange == 1:
            self.showmaxButton.setText("❐")
            self.showMaximized()
            self.windowSizeChange = 0
        elif self.windowSizeChange == 0:
            self.windowSizeChange = 1
            self.showNormal()
            self.showmaxButton.setText("□")

    #布局。
    def setLayouts(self):

        self.mainLayout = QVBoxLayout()
        #self.mainLayout.addWidget(self.header)
        #self.mainLayout.addWidget(self.line1)

        self.contentLayout = QHBoxLayout()
        self.contentLayout.setStretch(0, 70)
        self.contentLayout.setStretch(1, 570)

        self.mainLayout.addLayout(self.titleLayout)
        self.contentLayout.addWidget(self.mainlabel)
        self.contentLayout.addWidget(self.mainContents)

        self.contentLayout.setSpacing(0)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)

        self.mainLayout.addLayout(self.contentLayout)
        #self.mainLayout.addWidget(self.playWidgets)

        self.mainLayout.setStretch(0, 43)
        self.mainLayout.setStretch(1, 0)
        self.mainLayout.setStretch(2, 576)
        self.mainLayout.setStretch(3, 50)

        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

    #list的点击事件
    def listClickChangeTab(self,item):
        if item.text() == u'        教学大厅':
            self.mainContents.setCurrentIndex(0)
        elif item.text() == u'        游戏中心':
            self.mainContents.setCurrentIndex(3)
        elif item.text() == u'        本地视频':
            self.mainContents.setCurrentIndex(5)
        elif item.text() == u'        我的下载':
            self.mainContents.setCurrentIndex(6)
        elif item.text() == u'        我的游戏':
            self.mainContents.setCurrentIndex(7)

    #鼠标事件
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
