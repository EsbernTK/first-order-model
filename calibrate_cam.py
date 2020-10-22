import cv2
from skimage.transform import resize
import os
from demo import key_pressed
if __name__ == '__main__':

    frame_dim = 256
    vid = cv2.VideoCapture(0)
    width = 1920
    height = 1080
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    capname = "cap"
    # cv2.namedWindow(capname,cv2.WND_PROP_FULLSCREEN)
    cv2.namedWindow(capname, cv2.WND_PROP_AUTOSIZE)
    cv2.moveWindow(capname, 0, 0)
    cv2.setWindowProperty(capname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    start_it = 0

    inc = 10
    save_file = os.path.abspath("camera_calibration.txt")

    wind_x, wind_y, wind_height, wind_width = int(width / 2), int(height / 2), 256, 256

    #print(os.path.exists(save_file))
    if(os.path.exists(save_file)):
        with(open(save_file,"r")) as file:
            line = file.read().split(",")
            wind_x, wind_y, wind_height, wind_width = line
            wind_x, wind_y, wind_height, wind_width = int(wind_x), int(wind_y), int(wind_height), int(wind_width)
    #wind_x, wind_y, wind_height, wind_width = 710, 480, 486, 486

    pressed = False
    while (True):
        ret, frame = vid.read()

        frame = frame[wind_y:wind_y + wind_height, wind_x:wind_x + wind_width]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = resize(frame, (frame_dim, frame_dim))

        cv2.imshow(capname, frame)
        if (key_pressed("x")):
            break
        elif (key_pressed("w")):
            if (not pressed):
                pressed = True
                wind_y = max(0, wind_y - inc)
        elif (key_pressed("s")):
            if (not pressed):
                pressed = True
                wind_y = min(height - wind_height, wind_y + inc)
        elif (key_pressed("a")):
            if (not pressed):
                pressed = True
                wind_x = max(0, wind_x - inc)
        elif (key_pressed("d")):
            if (not pressed):
                pressed = True
                wind_x = min(width - wind_width, wind_x + inc)

        elif (key_pressed("q")):
            if (not pressed):
                pressed = True
                wind_height = max(frame_dim, wind_height - inc)
                wind_width = wind_height
        elif (key_pressed("e")):
            if (not pressed):
                pressed = True
                wind_height = min(height - wind_y, wind_height + inc)
                wind_width = wind_height
        elif (key_pressed("z")):
            if (not pressed):
                pressed = True
                print(f"saved file {save_file}")
                with(open(save_file,"w")) as f:
                    f.write(f"{wind_x},{wind_y},{wind_height},{wind_width}")
                print(f"{wind_x},{wind_y},{wind_height},{wind_width}")
        else:
            pressed = False
        cv2.waitKey(1)
        #print(f"{wind_x}, {wind_y}, {wind_height}, {wind_width}")

    vid.release()
    cv2.destroyAllWindows()