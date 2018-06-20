"""
Example script using PyOpenPose.
"""
import sys
sys.path.append('/usr/local/lib')
import PyOpenPose as OP
import time
import cv2

import numpy as np
import os

import Config

# OPENPOSE_ROOT = os.environ["OPENPOSE_ROOT"]
OPENPOSE_ROOT = r'/home/kevin/Python_DE/package/openpose/openpose'

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

def draw(point, frame):
    scale = 1.0
    cv2.circle(frame, (int(point[0][0] / scale), int(point[0][1] / scale)), 5, (0, 255, 0), 2)
    cv2.circle(frame, (int(point[1][0] / scale), int(point[1][1] / scale)), 5, (0, 255, 0), 2)
    cv2.circle(frame, (int(point[2][0] / scale), int(point[2][1] / scale)), 5, (0, 255, 0), 2)
    cv2.circle(frame, (int(point[3][0] / scale), int(point[3][1] / scale)), 5, (0, 255, 0), 2)
    cv2.circle(frame, (int(point[4][0] / scale), int(point[4][1] / scale)), 5, (0, 255, 0), 2)
    cv2.circle(frame, (int(point[5][0] / scale), int(point[5][1] / scale)), 5, (0, 255, 0), 2)
    cv2.circle(frame, (int(point[6][0] / scale), int(point[6][1] / scale)), 5, (0, 255, 0), 2)
    cv2.circle(frame, (int(point[7][0] / scale), int(point[7][1] / scale)), 5, (0, 255, 0), 2)
    cv2.circle(frame, (int(point[8][0] / scale), int(point[8][1] / scale)), 5, (0, 255, 0), 2)
    cv2.circle(frame, (int(point[9][0] / scale), int(point[9][1] / scale)), 5, (0, 255, 0), 2)
    cv2.circle(frame, (int(point[10][0] / scale), int(point[10][1] / scale)), 5, (0, 255, 0), 2)
    cv2.circle(frame, (int(point[11][0] / scale), int(point[11][1] / scale)), 5, (0, 255, 0), 2)
    cv2.circle(frame, (int(point[12][0] / scale), int(point[12][1] / scale)), 5, (0, 255, 0), 2)
    cv2.circle(frame, (int(point[13][0] / scale), int(point[13][1] / scale)), 5, (0, 255, 0), 2)
    cv2.circle(frame, (int(point[14][0] / scale), int(point[14][1] / scale)), 5, (0, 255, 0), 2)
    cv2.circle(frame, (int(point[15][0] / scale), int(point[15][1] / scale)), 5, (0, 255, 0), 2)
    cv2.circle(frame, (int(point[16][0] / scale), int(point[16][1] / scale)), 5, (0, 255, 0), 2)
    cv2.circle(frame, (int(point[17][0] / scale), int(point[17][1] / scale)), 5, (0, 255, 0), 2)
    return frame

def run():

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
    while True:
        start_time = time.time()
        try:
            ret, frame = cap.read()
            # frame = cv2.imread('galloping knights.jpg')
            rgb = frame
            print("RGB", rgb.shape)

        except Exception as e:
            print("Failed to grab", e)
            break

        t = time.time()
        op.detectPose(rgb)
        # op.detectFace(rgb)
        # op.detectHands(rgb)
        t = time.time() - t
        op_fps = 1.0 / t

        # res = op.render(rgb)
        cv2.putText(frame, 'UI FPS = %f, OP FPS = %f' % (actual_fps, op_fps), (20, 20), 0, 0.5, (0, 0, 255))
        persons = op.getKeypoints(op.KeypointType.POSE)[0]

        cfd_list = []
        for person in persons:
            cfd_sum, i = 0, 0
            for point in person:
                if point[2] != 0:
                    cfd_sum += point[2]
                    i += 1
            if cfd_sum != 0:
                cfd_mean = cfd_sum / i
                cfd_list.append(cfd_mean)
        print(len(cfd_list))

        print('----------------------------')
        max_index = cfd_list.index(max(cfd_list))
        cfd_list[max_index] = 0
        sec_index = cfd_list.index(max(cfd_list))
        print(max_index)
        point = op.getKeypoints(op.KeypointType.POSE)[0][max_index]
        point2 = op.getKeypoints(op.KeypointType.POSE)[0][sec_index]
        # point = op.getKeypoints(op.KeypointType.POSE)
        print(point)
        print('----------------------------')

        if download_heatmaps:
            hm = op.getHeatmaps()
            print("HM ",hm.shape, hm.dtype)
            showHeatmaps(hm)

            # hm = op.getHeatmaps()
            # parts = hm[:18]
            # background = hm[18]
            # PAFs = hm[19:]  # each PAF has two channels (total 16 PAFs)
            # cv2.imshow("Right Wrist", parts[4])
            # cv2.imshow("background", background)
            # showPAFs(PAFs)

        if persons is not None and len(persons) > 0:
            print("First Person: ", persons[0].shape)

        frame = draw(point, frame)
        frame = draw(point2, frame)

        cv2.imshow("OpenPose result", frame)

        key = cv2.waitKey(delay[paused])
        if key & 255 == ord('p'):
            paused = not paused

        if key & 255 == ord('q'):
            break

        actual_fps = 1.0 / (time.time() - start_time)

def main():
    run()
