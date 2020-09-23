# import the opencv library
import cv2
import os
if __name__ == '__main__':

    # define a video capture object
    vid = cv2.VideoCapture(os.path.abspath('./data/videos/04.mp4'))
    capname = "cap"
    cv2.namedWindow(capname,cv2.WND_PROP_AUTOSIZE)#cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow(capname,0,0)
    cv2.setWindowProperty(capname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    while (vid.isOpened()):
        # Capture frame-by-frame
        ret, frame = vid.read()
        if ret == True:
            cv2.imshow(capname, frame)
            cv2.waitKeyEx(1)
            print(cv2.getWindowImageRect(capname))
        else:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    #while (True):
    #
    #    # Capture the video frame
    #    # by frame
    #    ret, frame = vid.read()
    #
    #    # Display the resulting frame
    #    cv2.imshow('frame', frame)
    #
    #    # the 'q' button is set as the
    #    # quitting button you may use any
    #    # desired button of your choice
    #    if cv2.waitKey(1) & 0xFF == ord('q'):
    #        break
    #
    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()