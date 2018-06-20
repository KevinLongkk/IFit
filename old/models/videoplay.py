# -*- coding: UTF-8 -*-
import time
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from cv2 import *
from videoFrameBase import ScrollArea

import sys
sys.path.append(r'/home/kevin/IFit/commumication')
import op_cfg
sys.path.append(r'/home/kevin/IFit/OpenPose')
import openpose


import threading

class VideoBox(ScrollArea):

    VIDEO_TYPE_OFFLINE = 0
    VIDEO_TYPE_REAL_TIME = 1

    STATUS_INIT = 0
    STATUS_PLAYING = 1
    STATUS_PAUSE = 2

    video_url = ""

    def __init__(self, parent=None):
        super(VideoBox, self).__init__()
        self.video_url = "video/1.flv"
        self.video_type = 0  # 0: offline  1: realTime
        self.auto_play = False
        self.status = self.STATUS_INIT  # 0: init 1:playing 2: pause

        # 组件展示
        self.pictureLabel = QLabel()
        init_image = QPixmap("picture/b.jpg")#.scaled(self.width(), self.height())
        self.pictureLabel.setPixmap(init_image)

        self.pictureLabel2 = QLabel()
        init_image2 = QPixmap("picture/b.jpg")  # .scaled(self.width(), self.height())
        self.pictureLabel2.setPixmap(init_image2)

        self.playButton = QPushButton()
        self.playButton.setEnabled(True)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.switch_video)




        layout = QHBoxLayout()
        layout.addSpacing(25)
        layout.addWidget(self.pictureLabel)
        layout.addWidget(self.pictureLabel2)

        control_box = QVBoxLayout()
        control_box.addLayout(layout)
        control_box.setContentsMargins(0, 0, 0, 0)
        control_box.addWidget(self.playButton)


        self.setLayout(control_box)

        # timer 设置
        self.timer = VideoTimer()
        self.timer.timeSignal.signal[str].connect(self.show_video_images)

        # video 初始设置
        self.playCapture = VideoCapture()
        if self.video_url != "":
            self.playCapture.open(self.video_url)
            fps = self.playCapture.get(CAP_PROP_FPS)
            self.timer.set_fps(fps)
            self.playCapture.release()
            if self.auto_play:
                self.switch_video()
            # self.videoWriter = VideoWriter('*.mp4', VideoWriter_fourcc('M', 'J', 'P', 'G'), self.fps, size)

    def mat2pixmap(self,frame,ischange = 1):
        if frame is not None:
            height, width = frame.shape[:2]

            if frame.ndim == 3 and ischange:
                rgb = cvtColor(frame, COLOR_BGR2RGB)
            elif frame.ndim == 2 and ischange:
                rgb = cvtColor(frame, COLOR_GRAY2BGR)
            else:
                rgb = cvtColor(frame, COLOR_BGR2RGB)

            if height != 240 and width != 320:
                rgb = resize(rgb, (320, 240))

            qImage = QImage(rgb.flatten(), 320, 240, QImage.Format_RGB888)
            return qImage
        return None

    def reset(self):
        self.timer.stop()
        self.playCapture.release()
        self.status = VideoBox.STATUS_INIT
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def show_video_pose(self):
        while True:
            try:
                if op_cfg.FRAME is not None:
                    temp_image = op_cfg.FRAME
                    temp_image = self.mat2pixmap(temp_image, 0)
                    if temp_image is not None:
                        temp_pixmap = QPixmap.fromImage(temp_image)
                        self.pictureLabel2.setPixmap(temp_pixmap)
                    else:
                        init_image2 = QPixmap("picture/b.jpg")  # .scaled(self.width(), self.height())
                        self.pictureLabel2.setPixmap(init_image2)
                time.sleep(0.03)
            except:
                print("show pose fail")


    def show_video_images(self):
        if self.playCapture.isOpened():
            success, frame = self.playCapture.read()
            if success:
                op_cfg.FRAME_INDEX+=1

                ######################这个是用来显示关节的视频的地方############################

                # temp_image = op_cfg.FRAME
                # temp_image = self.mat2pixmap(temp_image,0)
                # if temp_image is not None:
                #     temp_pixmap = QPixmap.fromImage(temp_image)
                #     self.pictureLabel2.setPixmap(temp_pixmap)

                temp_image = self.mat2pixmap(frame)
                temp_pixmap = QPixmap.fromImage(temp_image)
                self.pictureLabel.setPixmap(temp_pixmap)
                # else:
                #     init_image2 = QPixmap("b.jpg")  # .scaled(self.width(), self.height())
                #     self.pictureLabel2.setPixmap(init_image2)
               ##################################################
            else:
                print("read failed, no frame data")
                success, frame = self.playCapture.read()
                if not success and self.video_type is VideoBox.VIDEO_TYPE_OFFLINE:
                    print("play finished")  # 判断本地文件播放完毕
                    self.reset()
                    self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
                return
        else:
            print("open file or capturing device error, init again")
            self.reset()

    def switch_video(self):
        op_cfg.PLAY = True
        threading._start_new_thread(openpose.run, (1, ))
        threading._start_new_thread(self.show_video_pose,())

        if self.video_url == "" or self.video_url is None:
            return
        if self.status is VideoBox.STATUS_INIT:
            self.playCapture.open(self.video_url)
            self.timer.start()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        elif self.status is VideoBox.STATUS_PLAYING:
            self.timer.stop()
            if self.video_type is VideoBox.VIDEO_TYPE_REAL_TIME:
                self.playCapture.release()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        elif self.status is VideoBox.STATUS_PAUSE:
            if self.video_type is VideoBox.VIDEO_TYPE_REAL_TIME:
                self.playCapture.open(self.video_url)
            self.timer.start()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

            self.status = (VideoBox.STATUS_PLAYING,
                           VideoBox.STATUS_PAUSE,
                           VideoBox.STATUS_PLAYING)[self.status]


class Communicate(QObject):

    signal = pyqtSignal(str)


class VideoTimer(QThread):

    def __init__(self, frequent=20):
        QThread.__init__(self)
        self.stopped = False
        self.frequent = frequent
        self.timeSignal = Communicate()
        self.mutex = QMutex()

    def time(self):
        while True:
            if self.stopped:
                return
            self.timeSignal.signal.emit("1")
            time.sleep(1 / self.frequent)#1 / self.frequent

    def run(self):
        with QMutexLocker(self.mutex):
            self.stopped = False
            while True:
                if self.stopped:
                    return
                self.timeSignal.signal.emit("1")
                time.sleep(1 / self.frequent)  # 1 / self.frequent
        #threading._start_new_thread(self.time, ())

    def stop(self):
        with QMutexLocker(self.mutex):
            self.stopped = True

    def is_stopped(self):
        with QMutexLocker(self.mutex):
            return self.stopped

    def set_fps(self, fps):
        self.frequent = fps


if __name__ == "__main__":
   app = QApplication(sys.argv)
   box = VideoBox("2.mp4")
   box.show()
   sys.exit(app.exec_())
