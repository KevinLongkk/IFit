# -*- coding: UTF-8 -*-
import sys
sys.path.append(r'/home/kevin/IFit/commumication')
import op_cfg
sys.path.append(r'/home/kevin/IFit/OpenPose')
import openpose
import numpy as np
import cv2
import threading
import time
import os
import math


class GAME(object):

    def __init__(self):
        op_cfg.PLAY = True
        self.pit_path = r'/home/kevin/IFit/fun_models/game_2/picture'
        self.GIF_INDEX = 0
        self.person_1_x = 120
        self.person_1_y = 300
        self.person_2_x = 200
        self.person_2_y = 220

    def run(self):
        threading._start_new_thread(openpose.run, (1,))
        self.start()
        # while True:
        #     self.keypoint = op_cfg.KEYPOINT
        #     t = time.time()
        #     FRAME = self.draw_background(os.path.join(self.pit_path, 'background'), self.GIF_INDEX, 14)
        #     op_cfg.GAME_1_FRAME = FRAME
        #     print(time.time() - t)
        #     # if self.keypoint is not None:
        #     #     if self.keypoint[0][7][1] < self.keypoint[0][0][1] and self.keypoint[0][6][1] > self.keypoint[0][1][1] and \
        #     #             self.keypoint[0][7][1] > 0:
        #     #         self.gif_play('motion1', 22)
        #     #     elif self.keypoint[0][10][1] - self.keypoint[0][8][1] < 50 and \
        #     #             self.keypoint[0][13][1] - self.keypoint[0][11][1] < 50 and \
        #     #             self.keypoint[0][9][1] - self.keypoint[0][1][1] < 100 and self.keypoint[0][10][1] > 0:
        #     #         self.gif_play('motion_down', 13)
        #     #     elif self.keypoint[0][13][1] > 0 and self.keypoint[0][12][1] > self.keypoint[0][13][1] and\
        #     #             self.keypoint[0][11][1] > self.keypoint[0][12][1]:
        #     #         self.gif_play('motion_kick', 16)
        #     #     elif self.keypoint[0][4][0] > 0 and self.keypoint[0][2][0] - self.keypoint[0][4][0] > 200:
        #     #         self.gif_play('motion_2', 46)
        #     #     else:
        #     #         FRAME = self.draw_person(FRAME, os.path.join(self.pit_path, 'motion_stand'), self.GIF_INDEX, 17)
        #     #         op_cfg.GAME_1_FRAME = FRAME
        #
        #     self.GIF_INDEX += 1

    def start(self):
        self.pit_bgs = []
        for i in range(15):
            pit_bg = cv2.imread(os.path.join(self.pit_path, 'background', 'frame'+str(i)+'.png'))
            pit_bg = cv2.resize(pit_bg, (640, 480))
            self.pit_bgs.append(pit_bg)
        pits_motion_1 = []
        for i in range(17):
            pit_motion_1 = cv2.imread(os.path.join(self.pit_path, 'motion_stand', 'frame'+str(i)+'.png'), -1)
            pits_motion_1.append(pit_motion_1)
        self.pits_p2motion_1 = []
        for i in range(23):
            pit_p2motion_1 = cv2.imread(os.path.join(self.pit_path, 'p2motion_1', 'frame' + str(i) + '.png'), -1)
            self.pits_p2motion_1.append(pit_p2motion_1)
        while True:
            self.keypoint = op_cfg.KEYPOINT
            pit_background = self.draw_background(self.pit_bgs, self.GIF_INDEX, 15)
            FRAME = pit_background.copy()

            # if self.keypoint is not None:
            #     if self.keypoint[0][7][1] < self.keypoint[0][0][1] and self.keypoint[0][6][1] > self.keypoint[0][1][1] and \
            #             self.keypoint[0][7][1] > 0:
            #         self.gif_play('motion1', 22, self.person_1_x, self.person_1_y)
            #     elif self.keypoint[0][10][1] - self.keypoint[0][8][1] < 50 and \
            #             self.keypoint[0][13][1] - self.keypoint[0][11][1] < 50 and \
            #             self.keypoint[0][9][1] - self.keypoint[0][1][1] < 100 and self.keypoint[0][10][1] > 0:
            #         self.gif_play('motion_down', 13, self.person_1_x, self.person_1_y)
            #     elif self.keypoint[0][13][1] > 0 and self.keypoint[0][12][1] > self.keypoint[0][13][1] and\
            #             self.keypoint[0][11][1] > self.keypoint[0][12][1]:
            #         self.gif_play('motion_kick', 16, self.person_1_x, self.person_1_y)
            #     elif self.keypoint[0][4][0] > 0 and self.keypoint[0][2][0] - self.keypoint[0][4][0] > 200:
            #         self.gif_play('motion_2', 46, self.person_1_x, self.person_1_y)
            #     else:
            #         FRAME = self.draw_person(FRAME, os.path.join(self.pit_path, 'motion_stand'), self.GIF_INDEX, 17,
            #                                  self.person_1_x, self.person_1_y)
            #         FRAME = self.draw_person(FRAME, os.path.join(self.pit_path, 'p2motion_1'),
            #                                  self.GIF_INDEX, 23, self.person_2_x, self.person_2_y, flip=True)
            #         op_cfg.GAME_1_FRAME = FRAME
            t = time.time()
            FRAME = self.draw_person(FRAME, pits_motion_1, self.GIF_INDEX, 17,
                                     self.person_1_x, self.person_1_y)
            FRAME = self.draw_person(FRAME, self.pits_p2motion_1,
                                     self.GIF_INDEX, 23, self.person_2_x, self.person_2_y, flip=True)
            print(time.time() - t)
            op_cfg.GAME_1_FRAME = FRAME
            self.GIF_INDEX += 1


    def gif_play(self, motion, number, x, y):
        self.GIF_INDEX = 0
        for i in range(number):
            FRAME = self.draw_background(self.pit_bgs, self.GIF_INDEX, 14)
            FRAME = self.draw_person(FRAME, self.pits_p2motion_1,
                                     self.GIF_INDEX, 23, self.person_2_x, self.person_2_y, flip=True)
            FRAME = self.draw_person(FRAME, os.path.join(self.pit_path, motion), self.GIF_INDEX, number, x, y)
            op_cfg.GAME_1_FRAME = FRAME
            self.GIF_INDEX += 1


    def draw_background(self, pit_bgs, index, number):
        index = index % number
        FRAME = pit_bgs[index]
        return FRAME

    def draw_person(self, FRAME, pits, index, number, x, y, flip=False):
        index = index % number
        pit = pits[index]
        if flip:
            pit = cv2.flip(pit, 1)
        FRAME[y:y + pit.shape[0], x:x + pit.shape[1]] = self.draw_picture(FRAME[y:y + pit.shape[0],
                                                                          x:x + pit.shape[1]], pit)
        return FRAME

    def draw_picture(self, src, dst):
        # assert src.channels() == 3 and dst.channels() == 4
        dst = cv2.resize(dst, (src.shape[1], src.shape[0]))
        for i in range(3):
            src[:, :, i] = np.multiply(src[:, :, i], (255 - dst[:, :, 3]) / 255)
            src[:, :, i] += np.multiply(dst[:, :, i], dst[:, :, 3] / 255)
        return src

