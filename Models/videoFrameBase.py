# -*- coding: UTF-8 -*-
from PyQt5.QtWidgets import QApplication,QDialog ,QTabWidget,QTableWidget,\
    QAbstractItemView,QFrame,QPushButton,QHBoxLayout,QLabel,QScrollArea,\
    QVBoxLayout,QGridLayout,QTextEdit,QMenu


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt,QObject,pyqtSignal
from PyQt5.QtGui import QCursor


# 主要内容区

# class ConfigMainContent(QObject):
#     def __init__(self, mainContent):
#         super(ConfigMainContent, self).__init__()
#         self.mainContent = mainContent

# 一个用于继承的类，方便多次调用。
class ScrollArea(QScrollArea):
    """包括一个ScrollArea做主体承载一个QFrame的基础类。"""
    scrollDown = pyqtSignal()

    def __init__(self, parent=None):
        super(ScrollArea, self).__init__()
        self.parent = parent
        self.frame = QFrame()
        self.frame.setObjectName('frame')
        # 用于发出scroll滑到最底部的信号。
        self.verticalScrollBar().valueChanged.connect(self.sliderPostionEvent)

        self.setWidgetResizable(True)

        self.setWidget(self.frame)

    # def noInternet(self):
    #     # 设置没有网络的提示。
    #     self.noInternetLayout = QGridLayout()
    #     self.setLayout(self.mainLayout)
    #
    #     self.Tip = QLabel("您已进入没有网络的异次元，打破次元壁 →", self)
    #     self.TipButton = QPushButton("打破次元壁", self)
    #     self.TipButton.setObjectName("TipButton")
    #
    #     self.TipLayout = QHBoxLayout()
    #     self.TipLayout.addWidget(self.Tip)
    #     self.TipLayout.addWidget(self.TipButton)
    #
    #     # self.indexAllSings.setLayout(self.TipLayout)
    #
    #     self.noInternetLayout.addLayout(self.TipLayout, 0, 0, Qt.AlignCenter|Qt.AlignTop)
    #
    #     self.frame.setLayout(self.noInternetLayout)

    def sliderPostionEvent(self):
        if self.verticalScrollBar().value() == self.verticalScrollBar().maximum():
            self.scrollDown.emit()

    def maximumValue(self):
        return self.verticalScrollBar().maximum()

class LoadVideo(QObject):
    def __init__(self,parent=None):
        super(LoadVideo,self).__init__()
        self.sportVideo = parent
        self.sportVideoParent =  self.sportVideo.parent
        self.detailFrame = self.sportVideoParent.parent.detailVideos
        self.mainContents = self.sportVideoParent.parent

        # 歌单名称。
        self.singNames = []

        # 歌单id。
        self.playlistIds = []

        # 歌曲ids。
        self.singsIds = [1,2,3,4,
                         5,6,7,8,
                         9,10,11,12,
                         13,14,15,16,
                         17,18,19,20,
                         21,22,23,24,
                         25,26,27,28,
                         29,30,31,32,
                         33,34,35,36]

        # 一个是否滑到底部的flag。
        self.sliderDown = False

        # 布局用row。
        self.gridRow = 0

        # 布局用column。
        self.gridColumn = 0

        self.offset = 0

        self.picName = ['1.jpg','2.jpg','g1.jpg','t1.jpg',
                       't2.jpg','t3.jpg','d1.jpg','d2.jpg',
                        'pic/t4','pic/t5','pic/t6','pic/t7',
                        'pic/t8','pic/t9','pic/t10','pic/t11',
                        'pic/t12','pic/t13','pic/t14','pic/t15',
                        'pic/t16','pic/t17','pic/t18','pic/t19',
                        'pic/t20','pic/t21','pic/t22','pic/t23',
                        'pic/t24','pic/t25','pic/t26','pic/t27',
                        'pic/t28','pic/t29','pic/t30','pic/t31',
                        ]

        self.sportVideo.scrollDown.connect(self.sliderDownEvent)

    def loadStart(self):
        for i in range(30):
            i += self.offset
            # if i >= 8:
            #     self.offset = 0
            #     return
            videoFrame = OneVideo(self.gridRow, self.gridColumn,self.singsIds[int(i%36)], self, self.picName[int(i%36)])
            try:
                videoFrame.clicked.connect(self.changeTab)
            except:
                print("点击链接失败")
            self.sportVideo.mainLayout.addWidget(videoFrame, self.gridRow, self.gridColumn)
            # 用于布局，一行4个。
            if self.gridColumn == 3:
                self.gridColumn = 0
                self.gridRow += 1
            else:
                self.gridColumn += 1


    def changeTab(self,ids,picName):
        try:
            print(picName)
            print(ids)

            #self.detailFrame.config.setupDetailFrames(result, self.singsUrls, self.singsIds)
            # self.detailFrame.picLabel.setSrc('{0}'.format(self.picName))
            self.detailFrame.picName = picName
            self.detailFrame.setLabels()
            # 隐藏原来的区域，显示现在的区域。
            self.mainContents.mainContents.setCurrentIndex(1)

        except:
            print("点击失败")

    def sliderDownEvent(self):
        if self.sportVideo.isHidden() == False:
        # toDo, 多个
            self.offset += 30
            self.loadStart()

class OneVideo(QFrame):
    # 大量创建，这样可以省内存。
    __solts__ = ('parent', 'ggparent', 'detailFrame', 'row', 'column', 'ids',
     'picName', 'picLabel', 'nameLabel',
     'mainLayout',
     'mousePos',
     'result','catch',
     'singsIds', 'singsUrls')

    clicked = pyqtSignal(str, str)

    def __init__(self, row, column, ids=None, parent=None, picName=None):
        super(OneVideo, self).__init__()

        self.setObjectName('oneSing')
        # 自己的位置信息。
        self.row = row
        self.column = column
        # 歌单号。
        self.ids = str(ids)
        # 大图的缓存名。
        self.picName = picName

        self.setMinimumSize(180, 235)#180 235

        self.picLabel = QLabel()
        #self.picLabel.setText(self.ids)
        self.picLabel.setObjectName('picLabel')
        self.picLabel.setMinimumSize(180, 180)#180 180
        self.picLabel.setMaximumSize(180, 180)#180 180
        self.picLabel.setStyleSheet("QLabel#picLabel{border-image:url(%s);}"%(self.picName))

        self.nameLabel = QLabel()
        self.nameLabel.setText(self.picName)
        self.nameLabel.setMaximumSize(180, 20)  # 180 180
        #self.nameLabel.setMaximumWidth(180)
        self.nameLabel.setWordWrap(True)

        self.mainLayout = QVBoxLayout(self)

        self.mainLayout.addWidget(self.picLabel)
        self.mainLayout.addWidget(self.nameLabel)

    # 功能。
    def setStyleSheets(self, styleSheet=None):
        if styleSheet:
            self.setStyleSheet(styleSheet)

   # 事件。
    def mousePressEvent(self, event):
        # 记录下当前鼠标的位置。
        self.mousePos = QCursor.pos()

    def mouseReleaseEvent(self, event):
        try:
            # 先进行判断，防止误点将鼠标移开后还是会判断为已经点击的尴尬。
            if QCursor.pos() != self.mousePos:
                return
            else:
                self.clicked.emit(self.ids, self.picName)
        except:
            print("点击释放失败")

# 视频详情页。
class DetailVideos(ScrollArea):

    def __init__(self, parent=None):
        super(DetailVideos, self).__init__(self)

        # self.hide()
        self.parent = parent
        self.picName = None
        self.setObjectName('detailVideos')
        # with open('QSS/detailSings.qss', 'r', encoding='utf-8') as f:
        #     self.setStyleSheet(f.read())

        #self.settLabels()

        self.settLabels()
        self.setButtons()
        self.setTabs()
        self.setLabels()
        self.setLayouts()

    # 布局。
    def setLabels(self):

        self.picLabel = QLabel(self.frame)
        self.picLabel.setMinimumSize(180, 180)  # 180 180
        self.picLabel.setMaximumSize(180, 180)  # 180 180
        if self.picName != None:
            self.picLabel.setStyleSheet("QLabel#picLabel{border-image:url(%s);}"%(self.picName))
        self.picLabel.setObjectName('picLabel')



        # self.settLabels()
        # self.setButtons()
        # self.setTabs()
        # self.setLayouts()

    def settLabels(self):
        self.titleLabel = QLabel(self.frame)
        self.titleLabel.setObjectName('titleLabel')
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setMaximumHeight(40)

        self.authorPic = QLabel(self.frame)
        self.authorName = QLabel(self.frame)
        self.authorName.setObjectName('authorName')
        self.authorName.setMaximumHeight(28)

        self.descriptionText = QTextEdit(self.frame)
        self.descriptionText.setReadOnly(True)
        self.descriptionText.setObjectName('descriptionText')
        self.descriptionText.setMaximumWidth(450)
        self.descriptionText.setMaximumHeight(100)
        self.descriptionText.setMinimumHeight(100)

    def setButtons(self):
        # self.showButton = QPushButton("教学")
        # self.showButton.setObjectName('showButton')
        # self.showButton.setMaximumSize(36, 20)

        self.descriptionLabel = QLabel(" 简介 ：")
        self.descriptionLabel.setObjectName('descriptionLabel')
        self.descriptionLabel.setMaximumSize(40, 40)

        self.playAllButton = QPushButton("开始播放")
        #self.playAllButton.setIcon(QIcon('resource/playAll.png'))
        self.playAllButton.setObjectName('playAllButton')
        self.playAllButton.setMaximumSize(90, 24)
        self.playAllButton.clicked.connect(self.changeVideoTab)

    def changeVideoTab(self):
        self.parent.mainContents.setCurrentIndex(2)

    def setTabs(self):
        self.contentsTab = QTabWidget(self.frame)

        self.singsTable = TableWidget(3, ['记录', '记录', '记录'])
        self.singsTable.setObjectName('singsTable')
        self.singsTable.setMinimumWidth(self.width())
        self.singsTable.setColumnWidths({i: j for i, j in zip(range(3),
                                                              [self.width() / 3 * 1.25, self.width() / 3 * 1.25,
                                                               self.width() / 3 * 0.5])})

        self.contentsTab.addTab(self.singsTable, "歌曲列表")

    def setLayouts(self):
        self.mainLayout = VBoxLayout()

        self.topLayout = HBoxLayout()

        self.descriptionLayout = VBoxLayout()
        self.titleLayout = HBoxLayout()
        #self.titleLayout.addWidget(self.showButton)
        self.titleLayout.addSpacing(5)
        self.titleLayout.addWidget(self.titleLabel)

        self.authorLayout = HBoxLayout()
        self.authorLayout.addWidget(self.authorPic)
        self.authorLayout.addWidget(self.authorName)
        self.authorLayout.addStretch(1)

        self.descriptLayout = HBoxLayout()
        self.descriptLayout.addWidget(self.descriptionLabel)
        self.descriptLayout.addWidget(self.descriptionText)

        self.descriptionLayout.addSpacing(10)
        self.descriptionLayout.addWidget(self.playAllButton)
        self.descriptionLayout.addSpacing(5)
        self.descriptionLayout.addLayout(self.titleLayout)
        self.descriptionLayout.addLayout(self.authorLayout)
        self.descriptionLayout.addSpacing(5)
        self.descriptionLayout.addLayout(self.descriptLayout)


        self.topLayout.addSpacing(18)
        self.topLayout.addWidget(self.picLabel)
        self.topLayout.addSpacing(18)
        self.topLayout.addLayout(self.descriptionLayout)

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addWidget(self.contentsTab)

        self.frame.setLayout(self.mainLayout)

class MainContent(ScrollArea):
    # 定义一个滑到了最低部的信号。
    # 方便子控件得知已经滑到了最底部，要做些加载的动作。

    def __init__(self, parent=None):
        """主内容区，包括推荐歌单等。"""
        super(MainContent, self).__init__()
        self.parent = parent
        self.setObjectName("MainContent")

        self.tab = QTabWidget()
        self.tab.setObjectName("contentsTab")

        # self.setGeometry(QtCore.QRect(240, 50, 857, 730))

        self.tab.setStyleSheet(
            '''
            QTabBar::tab
            {
               width: 80px;
               height: 30px;
               font: 15px;
               background-color: white;
               border-color: black;
            }
            QTabWidget::tab-bar
            {
               left: 308px;
            }

            QTabBar::tab:selected
            {
               margin-left: 0;
               margin-right: 0;
               background: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0.915, stop:0 rgba(0, 0, 255, 255), stop:1 rgba(255,255,255 255));
               color: red;
            }

            QTabBar::tab:!selected
            {
               color: black;
               margin-left: 0;
               margin-right: 0;
            }

            QTabBar::tab:hover:!selected
            {
               color: red;
               margin-left: 0;
               margin-right: 0;
            }

            QTabBar::tab:!selected
            {
               margin-top: 1px;
               margin-bottom: 0px;
            }​
         '''
        )
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.tab)

        self.frame.setLayout(self.mainLayout)

    def addTab(self, widget, name=''):
        self.tab.addTab(widget, name)

class TableWidget(QTableWidget):
    def __init__(self, count, headerLables):
        super(TableWidget, self).__init__()
        self.setColumnCount(count)
        self.setHorizontalHeaderLabels(headerLables)

        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def setColumnWidths(self, widths):
        for key in widths:
            self.setColumnWidth(key, widths[key])

# 去除了margin和spacing的布局框。
class VBoxLayout(QVBoxLayout):
    def __init__(self, *args):
        super(VBoxLayout, self).__init__(*args)

        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

class HBoxLayout(QHBoxLayout):

    def __init__(self, *args):
        super(HBoxLayout, self).__init__(*args)

        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

# 默认情况下。
# ----!!!----
# 一个水平居中的布局。
# class HStretchBox(HBoxLayout):
#
#     def __init__(self, parentLayout, *widgets, frontStretch=1, behindStretch=1):
#         super(HStretchBox, self).__init__()
#         self.addStretch(frontStretch)
#         for i in widgets:
#             self.addWidget(i)
#
#         self.addStretch(behindStretch)
#
#         parentLayout.addLayout(self)

# 默认情况下。
#  |
#  !
#  |
# 一个垂直居中的布局。
# class VStretchBox(VBoxLayout):
#
#     def __init__(self, parentLayout, *widgets, frontStretch=1, behindStretch=1):
#         super(VStretchBox, self).__init__()
#         self.addStretch(frontStretch)
#         for i in widgets:
#             self.addWidget(i)
#         self.addStretch(behindStretch)
#
#         self.parentLayout.addLayout(self)

class sportFrame(ScrollArea):
    def __init__(self, parent=None):
        super(sportFrame, self).__init__()
        self.parent = parent
       # self.transTime = addition.itv2time

        self.setObjectName("sportFrame")

        # 主布局。
        self.mainLayout = QGridLayout(self.frame)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setHorizontalSpacing(10)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

class TaiChi(sportFrame):
    def __init__(self, parent=None):
        super(TaiChi, self).__init__(parent)

class Gymnastics(sportFrame):
    def __init__(self, parent=None):
        super(Gymnastics, self).__init__(parent)

class Dance(sportFrame):
    def __init__(self, parent=None):
        super(Dance, self).__init__(parent)
