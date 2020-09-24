import cv2
from skimage.transform import resize
import os
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

    while (True):
        ret, frame = vid.read()

        frame = frame[wind_y:wind_y + wind_height, wind_x:wind_x + wind_width]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = resize(frame, (frame_dim, frame_dim))

        cv2.imshow(capname, frame)
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break
        if cv2.waitKey(1) & 0xFF == ord('w'):
            wind_y = max(0, wind_y - inc)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            wind_y = min(height - wind_height, wind_y + inc)
        if cv2.waitKey(1) & 0xFF == ord('a'):
            wind_x = max(0, wind_x - inc)
        if cv2.waitKey(1) & 0xFF == ord('d'):
            wind_x = min(width - wind_width, wind_x + inc)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            wind_height = max(frame_dim, wind_height - inc)
            wind_width = wind_height
        if cv2.waitKey(1) & 0xFF == ord('e'):
            wind_height = min(height - wind_y, wind_height + inc)
            wind_width = wind_height
        if cv2.waitKey(1) & 0xFF == ord('z'):
            print(f"saved file {save_file}")
            with(open(save_file,"w")) as f:
                f.write(f"{wind_x},{wind_y},{wind_height},{wind_width}")
        #print(f"{wind_x}, {wind_y}, {wind_height}, {wind_width}")

    vid.release()
    cv2.destroyAllWindows()