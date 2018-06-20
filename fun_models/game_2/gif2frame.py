from PIL import Image, ImageSequence
import cv2
import numpy as np

pit_path = r'/home/kevin/IFit/fun_models/game_2/picture/p2motion_1.gif'

ii = Image.open(pit_path)
ite = ImageSequence.Iterator(ii)

index = 0
for i in ite:
    i.save("/home/kevin/IFit/fun_models/game_2/picture/p2motion_1/frame%d.png" % index)
    index+=1