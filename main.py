import numpy as np
from skimage.transform import resize
from skimage import img_as_ubyte
import torch
from sync_batchnorm import DataParallelWithCallback

from modules.generator import OcclusionAwareGenerator
from modules.keypoint_detector import KPDetector
from animate import normalize_kp
from scipy.spatial import ConvexHull
import cv2
import os
import time

from demo import load_checkpoints, animate_image
import imageio

def load_image(image_path):
    source_image = imageio.imread(image_path)[..., :3]
    return resize(source_image,(frame_dim,frame_dim))

if __name__ == '__main__':

    images = ["./data/images/mette-fit.png", "./data/images/herzog-fit.png", "./data/images/02.png"]

    generator, kp_detector = load_checkpoints(config_path='config/vox-256.yaml',
                                checkpoint_path='./models/vox-cpk.pth.tar')


    image_ind = 0
    frame_dim = 256
    use_relative = True
    source_image = load_image(images[0])
    vid = cv2.VideoCapture(0)
    width = 1920
    height = 1080
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)




    capname = "cap"
    #cv2.namedWindow(capname,cv2.WND_PROP_FULLSCREEN)
    cv2.namedWindow(capname, cv2.WND_PROP_AUTOSIZE)
    cv2.moveWindow(capname,0,0)
    cv2.setWindowProperty(capname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    start_it = 0

    inc = 10

    save_file = os.path.abspath("camera_calibration.txt")

    wind_x, wind_y, wind_height, wind_width = int(width / 2), int(height / 2), 256, 256
    if(os.path.exists(save_file)):
        with(open(save_file,"r")) as file:
            line = file.read().split(",")
            wind_x, wind_y, wind_height, wind_width = line
            wind_x, wind_y, wind_height, wind_width = int(wind_x), int(wind_y), int(wind_height), int(wind_width)

    while (True):
        delta_T = time.time()
        ret, frame = vid.read()

        frame = frame[wind_y:wind_y+wind_height,wind_x:wind_x+wind_width]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = resize(frame, (frame_dim, frame_dim))
        #frame = cv2.resize(frame, (256, 256))
        if(start_it < 2):
            orig_frame = frame
        else:
            start_it+=1

        predictions = animate_image(source_image, frame,orig_frame, generator, kp_detector, relative=use_relative)
        #print(np.shape(predictions))
        predictions = cv2.cvtColor(predictions, cv2.COLOR_RGB2BGR)
        fps = vid.get(cv2.CAP_PROP_FPS)
        #cv2.waitKeyEx(56)
        print(time.time()-delta_T)
        cv2.imshow(capname, predictions)
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            image_ind = image_ind-1 if image_ind-1>0 else len(images)-1
            source_image = load_image(images[image_ind])
        if cv2.waitKey(1) & 0xFF == ord('e'):
            image_ind = (image_ind+1)%len(images)
            source_image = load_image(images[image_ind])



    vid.release()
    cv2.destroyAllWindows()