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

<<<<<<< HEAD
from demo import load_checkpoints, animate_image,key_pressed
=======
from demo import load_checkpoints, animate_image
>>>>>>> ac110e35654bd612bec6c90d38e6f2e3e78ce3c8
import imageio

def load_image(image_path):
    source_image = imageio.imread(image_path)[..., :3]
    return resize(source_image,(frame_dim,frame_dim))

if __name__ == '__main__':

<<<<<<< HEAD

    with(open("./data/images/images_to_use.txt","r")) as file:
        images = file.readlines()
    for ind,i in enumerate(images):
        images[ind] = i.replace("\n","")

    #images = ["./data/images/mette-fit.png", "./data/images/herzog-fit.png", "./data/images/02.png","./data/images/DF_1.png","./data/images/DF_2.png"
    #          ,"./data/images/DF_3.png","./data/images/DF_4.png","./data/images/DF_5.png","./data/images/DF_6.png"
    #          ,"./data/images/søren_brostrøm_fit.jpg","./data/images/peter_Sommer_fit.jpg"]
=======
    images = ["./data/images/mette-fit.png", "./data/images/herzog-fit.png", "./data/images/02.png"]
>>>>>>> ac110e35654bd612bec6c90d38e6f2e3e78ce3c8

    generator, kp_detector = load_checkpoints(config_path='config/vox-256.yaml',
                                checkpoint_path='./models/vox-cpk.pth.tar')


    image_ind = 0
    frame_dim = 256
<<<<<<< HEAD
    use_relative = False
=======
    use_relative = True
>>>>>>> ac110e35654bd612bec6c90d38e6f2e3e78ce3c8
    source_image = load_image(images[0])
    vid = cv2.VideoCapture(0)
    width = 1920
    height = 1080
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


<<<<<<< HEAD
    debug_name = "debug"
    cv2.namedWindow(debug_name, cv2.WND_PROP_AUTOSIZE)
    cv2.moveWindow(debug_name, 0, 0)
    cv2.setWindowProperty(debug_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
=======
>>>>>>> ac110e35654bd612bec6c90d38e6f2e3e78ce3c8


    capname = "cap"
    #cv2.namedWindow(capname,cv2.WND_PROP_FULLSCREEN)
<<<<<<< HEAD
    cv2.namedWindow(capname, cv2.WINDOW_NORMAL)
    #cv2.namedWindow(capname, cv2.WND_PROP_AUTOSIZE)
    cv2.resizeWindow(capname,640,380)
    cv2.moveWindow(capname,960,-40)
    #cv2.setWindowProperty(capname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
=======
    cv2.namedWindow(capname, cv2.WND_PROP_AUTOSIZE)
    cv2.moveWindow(capname,0,0)
    cv2.setWindowProperty(capname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
>>>>>>> ac110e35654bd612bec6c90d38e6f2e3e78ce3c8
    start_it = 0

    inc = 10

    save_file = os.path.abspath("camera_calibration.txt")

    wind_x, wind_y, wind_height, wind_width = int(width / 2), int(height / 2), 256, 256
    if(os.path.exists(save_file)):
        with(open(save_file,"r")) as file:
            line = file.read().split(",")
            wind_x, wind_y, wind_height, wind_width = line
            wind_x, wind_y, wind_height, wind_width = int(wind_x), int(wind_y), int(wind_height), int(wind_width)
<<<<<<< HEAD
            print(f"{wind_x},{wind_y},{wind_height},{wind_width}")
    pressed=False
    while (True):
        #delta_T = time.time()
=======

    while (True):
        delta_T = time.time()
>>>>>>> ac110e35654bd612bec6c90d38e6f2e3e78ce3c8
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
<<<<<<< HEAD
        #cv2.waitKeyEx(56)
        #print(time.time()-delta_T)
        cv2.imshow(capname, predictions)
        cv2.imshow(debug_name,frame)
        #print(time.time() - delta_T)
        if (key_pressed("x")):
            break
        elif (key_pressed("q")):
            if (not pressed):
                pressed = True
                image_ind = image_ind-1 if image_ind-1>=0 else len(images)-1
                source_image = load_image(images[image_ind])
        elif (key_pressed("e")):
            if (not pressed):
                pressed = True
                image_ind = (image_ind+1)%len(images)
                source_image = load_image(images[image_ind])
        else:
            pressed=False
        cv2.waitKey(1)
=======
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
>>>>>>> ac110e35654bd612bec6c90d38e6f2e3e78ce3c8



    vid.release()
    cv2.destroyAllWindows()