
from InterUtils import sendAbnormals
import cv2

if __name__=="__main__":

    frame = cv2.imread("./f17da2da-163e-3158-b41b-34d50e9341d1.jpg")



    reportingAbnormals= [
        {'type': 'UoDOFacilities', 'score': 0.68, 'x': 593, 'y': 268, 'w': 79, 'h': 59, 'cam_id': 'camera_24',
      'imgId': 'f17da2da-163e-3158-b41b-34d50e9341d1', 'time': 1569402283}]

    sendAbnormals(frame, reportingAbnormals, "camera_24")

