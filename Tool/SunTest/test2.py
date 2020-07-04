import cv2
import time
import threading
from queue import Queue


def grap():
    while cap.isOpened():
        ret, frame = cap.read()
        print(ret)
        if ret == False:
            break


def enqueue():

    while True:
        if frame is not None:
            print(frame)
            Q.put(frame)
            time.sleep(5)

if __name__=="__main__":

    cap = cv2.VideoCapture('rtsp://admin:px68018888@172.16.100.17:554/')

    Q = Queue()
    frame = None

    thread_1 = threading.Thread(target=grap,)
    thread_1.start()

    thread_2 = threading.Thread(target=enqueue,)
    thread_2.start()

    while True:
        # get a frame
        if Q.qsize()>0:
            frame=Q.get()
        # show a frame
            cv2.imshow("capture", frame)

            time.sleep(1)


    cap.release()
    cv2.destroyAllWindows()
