"""
Example script using PyOpenPose.
"""
import sys
sys.path.append(r'/usr/local/lib')
import PyOpenPose as OP
import time
import cv2

import numpy as np
import os
import math

sys.path.append(r'/home/kevin/IFit/OpenPose/scripts')
import util
sys.path.append(r'/home/kevin/IFit/commumication')
import op_cfg

import cPickle

import tensorflow as tf

# OPENPOSE_ROOT = os.environ["OPENPOSE_ROOT"]
OPENPOSE_ROOT = r'/home/kevin/Python_DE/package/openpose/openpose'

pkl_path = r'/home/kevin/IFit/OpenPose/point_pkl'
video_num = '0001'
point_label = cPickle.load(open(os.path.join(pkl_path, video_num+'.pkl'), 'rb'))

def showHeatmaps(hm):
    for idx, h in enumerate(hm):
        cv2.imshow("HeatMap "+str(idx), h)


def showPAFs(PAFs, startIdx=0, endIdx=16):
    allpafs = []
    for idx in range(startIdx, endIdx):
        X = PAFs[idx*2]
        Y = PAFs[idx*2+1]
        tmp = np.dstack((X, Y, np.zeros_like(X)))
        allpafs.append(tmp)

    pafs = np.mean(allpafs, axis=0)
    cv2.imshow("PAF", pafs)

def draw(points, frame):
    scale = 1.0
    for point in points:
        for i in range(18):
            if point[i][0] != 0.0 and point[i][1] != 0.0:
                cv2.circle(frame, (int(point[i][0] / scale), int(point[i][1] / scale)), 5, (0, 255, 0), 2)
    return frame

def run(num):

    # cap = cv2.VideoCapture('test.mp4')
    cap = cv2.VideoCapture(0)

    download_heatmaps = False
    # with_face = with_hands = False
    # op = OP.OpenPose((656, 368), (368, 368), (1280, 720), "COCO", OPENPOSE_ROOT + os.sep + "models" + os.sep, 0,
    #                  download_heatmaps, OP.OpenPose.ScaleMode.ZeroToOne, with_face, with_hands)
    # op = OP.OpenPose((320, 240), (240, 240), (640, 480), "COCO", OPENPOSE_ROOT + os.sep + "models" + os.sep, 0, download_heatmaps)
    op = OP.OpenPose((320, 240), (240, 240), (640, 480), "COCO", OPENPOSE_ROOT + os.sep + "models" + os.sep, 0,
                     download_heatmaps)

    actual_fps = 0
    paused = False
    delay = {True: 0, False: 1}

    print("Entering main Loop.")
    frame_index = op_cfg.FRAME_INDEX
    while op_cfg.PLAY:
        res_point1, res_point2, similarity = None, None, None
        start_time = time.time()
        try:
            ret, frame = cap.read()
            # frame = cv2.imread('galloping knights.jpg')
            rgb = frame
            image_h, image_w, _ = rgb.shape
            # print("RGB", rgb.shape)

        except Exception as e:
            print("Failed to grab", e)
            break

        t = time.time()
        op.detectPose(frame)
        # op.detectFace(rgb)
        # op.detectHands(rgb)
        t = time.time() - t
        op_fps = 1.0 / t

        # res = op.render(frame)
        cv2.putText(frame, 'UI FPS = %f, OP FPS = %f' % (actual_fps, op_fps), (20, 20), 0, 0.5, (0, 0, 255))
        persons = op.getKeypoints(op.KeypointType.POSE)[0]

        cfd_list = []
        distance_center_list = []
        try:
            for person in persons:
                cfd_sum, i = 0, 0
                center_x_sum, center_y_sum = 0, 0
                for point in person:
                    if point[2] != 0:
                        cfd_sum += point[2]
                        center_x_sum += point[0]
                        center_y_sum += point[1]
                        i += 1
                if cfd_sum != 0:
                    cfd_mean = cfd_sum / i
                    distance_center = math.pow(center_x_sum/i - image_w/2, 2) + math.pow(center_y_sum/i - image_h/2, 2)
                    cfd_list.append(cfd_mean)
                    distance_center_list.append(distance_center)
            # print(len(cfd_list))
            # print('----------------------------')
            max_index = distance_center_list.index(min(distance_center_list))
            distance_center_list[max_index] = 1e5
            sec_index = distance_center_list.index(min(distance_center_list))
            # print(max_index)
            point = op.getKeypoints(op.KeypointType.POSE)[0][max_index]
            point2 = op.getKeypoints(op.KeypointType.POSE)[0][sec_index]
            res_point1 = point
            res_point2 = point2

            if num == 1:
                frame = draw([point], frame)
                util.action(point)
                similarity = str(util.consine(point_label[frame_index], point))
            if num == 2:
                frame = draw([point], frame)
                frame = draw([point2], frame)
                # print(util.consine(point, point2))
                similarity = str(util.consine(point, point2))
                cv2.putText(frame, str(util.consine(point, point2)), (100, 100), 2, 3, (0, 0, 225))
            if num == 3:
                frame = draw(op.getKeypoints(op.KeypointType.POSE)[0], frame)
        except:
            print('No people')

        # if persons is not None and len(persons) > 0:
        #     print("First Person: ", persons[0].shape)
        # cv2.imshow("OpenPose result", frame)
        key = cv2.waitKey(delay[paused])
        if key & 255 == ord('p'):
            paused = not paused

        if key & 255 == ord('q'):
            break

        actual_fps = 1.0 / (time.time() - start_time)

        # return image
        # frame = np.zeros_like(frame)
        # frame = draw([res_point1], frame)
        op_cfg.FRAME = frame
        op_cfg.KEYPOINT = [res_point1, res_point2]
        op_cfg.SIMILARITY = similarity
        print(similarity)
        # print(op_cfg.KEYPOINT)