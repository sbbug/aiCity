'''
 Get video from camera
'''
# import cv2
#
# url = "rtsp://admin:zp123456@172.16.100.117:554/"
# cap = cv2.VideoCapture(url)  # 视频进行读取操作以及调用摄像头
#
# save_path = "./video/20190725/one/"
# i=1
# while cap.isOpened():  # 判断视频读取或者摄像头调用是否成功，成功则返回true。
#     ret, frame = cap.read()
#     if ret is True:
#         print('frame shape:', frame.shape)
#
#
#         cv2.imshow('frame', frame)
#         cv2.imwrite(save_path+str(i)+".jpg",frame)
#         i=i+1
#
# cap.release()
import datetime

t1 = '10:40'
t2 = '14:17'
now = datetime.datetime.now().strftime("%H:%M")
print("当前时间:" + now)
if t1 < now < t2:
    print("在此区间中")
else:
    print('不在此区间中')


