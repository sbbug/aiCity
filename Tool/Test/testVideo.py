import cv2
import Functions
import Parameters



cap = cv2.VideoCapture("rtmp://rtmp01open.ys7.com/openlive/c727397cf1a84d66a5368a75ad1b7507.hd")
print(cap)

ret, frame = cap.read()
print(ret,frame)
while True:
    ret, frame = cap.read()
    if ret is True:
        frame = cv2.resize(frame, (1280, 720))
        cv2.imshow('frame', frame)
    else:
        break
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()

