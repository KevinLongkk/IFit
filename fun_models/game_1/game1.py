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
import rotateImage
import math

op_cfg.PLAY = True
keypoint = op_cfg.KEYPOINT

pit_path = r'/home/kevin/IFit/fun_models/game_1/picture'
hammer_scale = 2
frame_width = 640
frame_height = 480

SCORE = 0
BEGIN = False
count = 0

blood_x = 80
blood_y = 140
blood_num = 10

score_flag = False
FIRST_LOAD = True


def draw_picture(src, dst):
    # assert src.channels() == 3 and dst.channels() == 4
    dst = cv2.resize(dst, (src.shape[1], src.shape[0]))
    for i in range(3):
        src[:, :, i] = np.multiply(src[:, :, i], (255 - dst[:, :, 3])/255)
        src[:, :, i] += np.multiply(dst[:, :, i], dst[:, :, 3] / 255)
    return src


def setText(frame):
    cv2.putText(frame, u"Score:"+str(SCORE), (20, 35), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    return frame


def is_impact(obj_x, obj_y, target_x, target_y, target_w, target_h):
    if obj_x > target_x-target_w/2 and obj_x < target_x+target_w/2 \
        and obj_y > target_y-target_h/2 and obj_y < target_y+target_h/2:
        return True
    else:
        return False


def draw_hammer(frame, keypoint, pit_hammer):

    hammer_y = int(keypoint[0][4][1])
    hammer_x = int(keypoint[0][4][0])
    rotate_angle = math.atan2(int(keypoint[0][3][1]) - int(keypoint[0][4][1]),
                              int(keypoint[0][3][0]) - int(keypoint[0][4][0])) * 180.0 / math.pi
    rotate_angle = 90 - rotate_angle
    hammer_image = rotateImage.rotateImage(
        pit_hammer[int(6 * 1.4):int(75 * 1.4), int(53 * 1.4):int(-3 * 1.4), :], rotate_angle)

    hammer_height = hammer_image.shape[0]
    hammer_width = hammer_image.shape[1]
    if hammer_x > frame_width - hammer_width/2:
        hammer_x = frame_width - hammer_width/2
    if hammer_y < hammer_height/2:
        hammer_y = hammer_height/2
    if hammer_x < hammer_width/2:
        hammer_x = hammer_width/2

    frame[int(hammer_y - hammer_height/2):int(hammer_y + hammer_height/2),
        int(hammer_x - math.floor(hammer_width/2)):int(hammer_x + math.floor(hammer_width/2))] = \
        draw_picture(frame[int(hammer_y - hammer_height/2):int(hammer_y + hammer_height/2),
                     int(hammer_x-math.floor(hammer_width/2)):int(hammer_x + math.floor(hammer_width/2))],
                     hammer_image)
    return frame

def draw_hand(frame, keypoint, pit_hand):
    frame[int(keypoint[0][4][1]-pit_hand.shape[1]/2):int(keypoint[0][4][1]+pit_hand.shape[1]/2),
          int(keypoint[0][4][0]-pit_hand.shape[0]/2):int(keypoint[0][4][0]+pit_hand.shape[0]/2)] = \
          draw_picture(frame[int(keypoint[0][4][1]-pit_hand.shape[1]/2):int(keypoint[0][4][1]+pit_hand.shape[1]/2),
          int(keypoint[0][4][0]-pit_hand.shape[0]/2):int(keypoint[0][4][0]+pit_hand.shape[0]/2)], pit_hand)
    return frame


def draw_blood(frame, blood_num):
    if blood_num < 0:
        blood_num = 0
    pit_blood = cv2.imread(os.path.join(pit_path, 'blood'+str(blood_num)+'.png'))
    pit_blood = cv2.resize(pit_blood, (100, 6))
    frame[blood_y:blood_y+pit_blood.shape[0], blood_x:blood_x+pit_blood.shape[1]] = pit_blood
    return frame


def get_hammer_xy(keypoint, pit_hammer):
    hammer_y = int(keypoint[0][4][1])
    hammer_x = int(keypoint[0][4][0])
    rotate_angle = math.atan2(int(keypoint[0][3][1]) - int(keypoint[0][4][1]),
                              int(keypoint[0][4][0]) - int(keypoint[0][3][0])) * 180.0 / math.pi
    rotate_angle = 90 - rotate_angle
    # hammer_image = rotateImage.rotateImage(
    #     pit_hammer[int(6 * 1.4):int(75 * 1.4), int(53 * 1.4):int(-3 * 1.4), :], rotate_angle)
    #
    # # hammer_height = hammer_image.shape[0]
    # # hammer_width = hammer_image.shape[1]
    if rotate_angle < 0:
        offset_x = -30
        offset_y = 25
    else:
        offset_x = 30
        offset_y = 25
    return hammer_x+offset_x, hammer_y - offset_y


def run():

    threading._start_new_thread(openpose.run, (1,))
    pit_hammer = cv2.imread(os.path.join(pit_path, '1.png'), -1)
    pit_background = cv2.imread(os.path.join(pit_path, 'beijing.png'))[:, ::-1, :]
    pit_target = cv2.imread(os.path.join(pit_path, 'horse.png'), -1)
    pit_begin_background = cv2.imread(os.path.join(pit_path, 'start_beijing.png'))
    pit_play_button = cv2.imread(os.path.join(pit_path, 'play.png'), -1)
    pit_hand_1 = cv2.imread(os.path.join(pit_path, 'hand.png'), -1)

    pit_hammer = cv2.resize(pit_hammer, (140, 140))
    pit_target = cv2.resize(pit_target, (250, 250))
    pit_play_button = cv2.resize(pit_play_button, (250, 50))
    pit_begin_background = cv2.resize(pit_begin_background, (640, 480))


    global BEGIN
    global count
    global score_flag
    global SCORE
    global blood_num
    global FIRST_LOAD
    while True:
        if not BEGIN:
            pit_begin = np.zeros_like(pit_begin_background)
            pit_begin[:, :] = pit_begin_background[:, :]
            keypoint = op_cfg.KEYPOINT
            pit_begin[(frame_height - pit_play_button.shape[0]) / 2:
                      (frame_height + pit_play_button.shape[0]) / 2,
                      (frame_width - pit_play_button.shape[1]) / 2:
                      (frame_width + pit_play_button.shape[1]) / 2] \
                      = draw_picture(pit_begin[(frame_height - pit_play_button.shape[0]) / 2:
                                         (frame_height + pit_play_button.shape[0]) / 2,
                                         (frame_width - pit_play_button.shape[1]) / 2:
                                         (frame_width + pit_play_button.shape[1]) / 2],
                                         cv2.flip(pit_play_button, 1))
            if keypoint is not None:
                if keypoint[0][3][0] != 0.0 and keypoint[0][3][1] != 0.0 and keypoint[0][4][0] != 0.0 and keypoint[0][4][1] != 0.0:
                    # cv2.circle(pit_begin, (int(keypoint[0][4][0]), int(keypoint[0][4][1])), 5, (0, 255, 0), 2)
                    pit_begin = draw_hand(pit_begin, keypoint, cv2.flip(pit_hand_1, 1))
                    # hammer_x, hammer_y = get_hammer_xy(keypoint, pit_hammer)
                    if is_impact(int(keypoint[0][4][0]), int(keypoint[0][4][1]), frame_width/2, frame_height/2,
                                 pit_play_button.shape[1], pit_play_button.shape[0]):
                        cv2.ellipse(pit_begin, (int(keypoint[0][4][0]-20), int(keypoint[0][4][1]-40)), (8, 8), 0.0, 270.,
                                    270+count/50.0*360, (255, 50, 50), 2)
                        count += 1
                    else:
                        count = 0
                    if count > 50:
                        BEGIN = True
                    op_cfg.GAME_1_FRAME = pit_begin[:, ::-1, :]
            else:
                op_cfg.GAME_1_FRAME = pit_begin[:, ::-1, :]
        else:
            keypoint = op_cfg.KEYPOINT
            if keypoint is not None:
                FRAME = np.zeros_like(op_cfg.FRAME)
                FRAME[:, :] = pit_background[0:480, 0:640]
                if keypoint[0][3][0] != 0.0 and keypoint[0][3][1] != 0.0 and keypoint[0][4][0] != 0.0 and keypoint[0][4][1] != 0.0:
                    if FIRST_LOAD:
                        pit_background[(frame_height - pit_target.shape[1]) / 2:(frame_height + pit_target.shape[1]) / 2,
                            0:pit_target.shape[0]] = \
                            draw_picture(
                                FRAME[(frame_height - pit_target.shape[1]) / 2:(frame_height + pit_target.shape[1]) / 2,
                                0:pit_target.shape[0]], cv2.flip(pit_target, 1))
                        FIRST_LOAD = False
                    t = time.time()
                    FRAME = draw_blood(FRAME, blood_num)
                    FRAME = draw_hammer(FRAME, keypoint, pit_hammer)
                    print(time.time()-t)

                    # hammer_y = int(keypoint[0][4][1])
                    # hammer_x = int(keypoint[0][4][0])
                    # rotate_angle = math.atan2(int(keypoint[0][3][1]) - int(keypoint[0][4][1]),
                    #                int(keypoint[0][3][0]) - int(keypoint[0][4][0])) * 180.0 / math.pi
                    # hammer_image = rotateImage.rotateImage(
                    #     pit_hammer[int(6 * 1.4):int(75 * 1.4), int(53 * 1.4):int(-3 * 1.4), :], 90-rotate_angle)
                    #
                    # hammer_height = hammer_image.shape[0] - 20
                    # hammer_width = hammer_image.shape[1]

                    # FRAME[hammer_y - hammer_height:hammer_y, hammer_x:hammer_x + hammer_width] = \
                    #     draw_picture(FRAME[hammer_y-hammer_height:hammer_y,
                    #                   hammer_x:hammer_x+hammer_width], hammer_image)

                    # cv2.rectangle(FRAME, (pit_target.shape[0] / 2 - 50, (frame_height) / 2 - 80),
                    #               (pit_target.shape[0] / 2 + 50, (frame_height) / 2 + 80),
                    #               (0, 0, 255))

                    hammer_x, hammer_y = get_hammer_xy(keypoint, pit_hammer)
                    # cv2.circle(FRAME, (hammer_x, hammer_y), 8, (255, 0, 0))
                    if is_impact(hammer_x, hammer_y, pit_target.shape[0]/2,
                                 (frame_height)/2+20, 120, 160):
                        if score_flag is not True:
                            blood_num -= 1
                            SCORE += 1
                        score_flag = True
                    else:
                        score_flag = False

                    # hammer_y = int(keypoint[0][4][1])
                    # hammer_x = int(keypoint[0][4][0])
                    # rotate_angle = math.atan2(int(keypoint[0][3][1]) - int(keypoint[0][4][1]),
                    #                           int(keypoint[0][4][0]) - int(keypoint[0][3][0])) * 180.0 / math.pi
                    # # rotate_angle = -(90+rotate_angle)
                    # rotate_angle = -(90 - rotate_angle)
                    # print('angle:'+str(rotate_angle))
                    # hammer_image = rotateImage.rotateImage(
                    #     pit_hammer[int(6 * 1.4):int(75 * 1.4), int(53 * 1.4):int(-3 * 1.4), :], rotate_angle)

                    # hammer_height = hammer_image.shape[0]
                    # hammer_width = hammer_image.shape[1]
                    # if hammer_x > frame_width - hammer_width:
                    #     hammer_x = frame_width - hammer_width
                    # if hammer_y < hammer_height:
                    #     hammer_y = hammer_height
                    # if hammer_x < 0:
                    #     hammer_x = 0
                    # if hammer_y > frame_height - (hammer_width / 2) / max(math.sin(rotate_angle / 180 * math.pi), 1e-5):
                    #     hammer_y = int(
                    #         frame_height - (hammer_width / 2) / max(math.sin(rotate_angle / 180 * math.pi), 1e-5))
                    # if rotate_angle > 0:
                    #     cv2.circle(FRAME, (int(hammer_x-(hammer_width/2*math.cos(rotate_angle*math.pi/180))),
                    #                        int(hammer_y-(hammer_width/2*math.cos((90-rotate_angle)*math.pi/180)))
                    #                        ), 5, (255, 0, 0))
                    # else:
                    #     cv2.circle(FRAME, (int(hammer_x + (hammer_width / 2 * math.cos(rotate_angle * math.pi / 180))),
                    #                        int(hammer_y - (hammer_width / 2 * math.cos(
                    #                            (90 - rotate_angle) * math.pi / 180)))
                    #                        ), 5, (255, 0, 0))
                    # cv2.circle(FRAME, (int(hammer_x - hammer_width),
                    #                    int(hammer_y - 2*(hammer_width / 2 * math.sin(-rotate_angle * math.pi / 180)))
                    #                    ), 5, (0, 0, 255))
                    # hhhy = hammer_y - hammer_height
                    # hhhx = hammer_x - hammer_width
                    # cv2.circle(FRAME, (int(hhhx), int(hhhy)), 5, (0, 0, 255))
                    # cv2.circle(FRAME, (30, 240), 30, (0, 0, 255), 3)
                    # cv2.line(FRAME, ((int(keypoint[0][3][0]), int(keypoint[0][3][1]))), (int(keypoint[0][4][0]), int(keypoint[0][4][1])),
                    #          (0, 255, 0), 2)
                    FRAME = cv2.flip(FRAME, 1)
                    setText(FRAME)
                    op_cfg.GAME_1_FRAME = FRAME
                    op_cfg.UPDATE = True
