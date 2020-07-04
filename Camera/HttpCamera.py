import requests
import datetime
import json
import urllib.request
from Functions import getProjectContext
import uuid
import os
from Parameters import HTTP_CAMERAS
import cv2


class HttpCamera:
    HTTP_SERVER = "http://59.83.214.5:33333/getCapturePictures"
    HEADERS = {'Content-Type': 'application/json'}

    def __init__(self, camera_id, date_time=None):

        self.camera_id = camera_id
        self.angles_pre_time = dict()

        if date_time is None:
            self.camera_date_time = str(datetime.datetime.now().strftime('%Y%m%d'))
        else:
            self.camera_date_time = date_time

    def getLatestMetaDataByCameraId(self):
        '''
        :return:
        '''
        result_json_data_field_sorted = None
        try:

            data = {

                'cameraIndexCode': self.camera_id,
                'captureDate': self.camera_date_time

            }
            response = requests.post(
                url=HttpCamera.HTTP_SERVER,
                headers=HttpCamera.HEADERS,
                data=json.dumps(data)
            )
            # str to json
            result_json = json.loads(response.text)
            # get data field
            result_json_data_field = result_json['data']
            # sort
            result_json_data_field_sorted = sorted(result_json_data_field, key=lambda x: x['dateTime'], reverse=True)
        except:
            print("http server error")
        if result_json_data_field_sorted is None or len(result_json_data_field_sorted) == 0:
            return None
        return result_json_data_field_sorted[0]

    def downloadImageToTargetDir(self, meta_data):
        '''
        :param meta_data:
        :return:
        '''
        if meta_data is None:
            return None
        # print(meta_data)

        now_date = self.camera_date_time
        camera_id = meta_data['cameraIndexCode']
        angle_id = str(meta_data['presetIndex'])

        if self.angles_pre_time.__contains__(angle_id):

            # not need to detect image

            if str(self.angles_pre_time[angle_id]) == str(meta_data['dateTime']):
                return None

        # update time
        self.angles_pre_time[angle_id] = str(meta_data['dateTime'])

        if not os.path.exists(os.path.join(getProjectContext() + "Resources/HttpCameras", now_date)):
            os.mkdir(os.path.join(getProjectContext() + "Resources/HttpCameras", now_date))
        if not os.path.exists(os.path.join(getProjectContext() + "Resources/HttpCameras", now_date, camera_id)):
            os.mkdir(os.path.join(getProjectContext() + "Resources/HttpCameras", now_date, camera_id))
        if not os.path.exists(
                os.path.join(getProjectContext() + "Resources/HttpCameras", now_date, camera_id, angle_id)):
            os.mkdir(os.path.join(getProjectContext() + "Resources/HttpCameras", now_date, camera_id, angle_id))

        img_root_path = os.path.join(getProjectContext() + "Resources/HttpCameras", now_date, camera_id, angle_id)
        im_name = str(uuid.uuid4())
        pic = None
        try:
            # print(meta_data['url'], "----------")

            if meta_data['url'] is None:
                return None

            response = urllib.request.urlopen(
                meta_data['url'],
                timeout=10
            )
            pic = response.read()

        except:
            print("read http image error")

        with open(os.path.join(img_root_path, im_name + ".jpg"), 'wb') as f:
            if pic is not None:
                f.write(pic)

        return os.path.join(img_root_path, im_name + ".jpg")

    def getImageAngleByFeature(self):
        pass

    def getDownloadImagePath(self):

        meta_data = self.getLatestMetaDataByCameraId()

        if meta_data is None:
            return None,None

        im_path = self.downloadImageToTargetDir(meta_data)

        angle_id = meta_data['presetIndex']

        return im_path, angle_id

    def readCameraInfo(self):
        '''
        :return:
        '''

        im_path, angle_id = self.getDownloadImagePath()

        im_data = None
        if im_path is not None:
            im_data = cv2.cvtColor(cv2.imread(im_path), cv2.COLOR_BGR2RGB)
            im_data = cv2.resize(im_data, (1280, 720))

        return {
            'camera_id': self.camera_id,
            'angle_id': angle_id,
            'im_path': im_path,
            'im_data': im_data
        }


if __name__ == "__main__":

    import time

    http_cameras = dict()

    for camera_id in HTTP_CAMERAS:
        http_cameras[camera_id] = HttpCamera(camera_id)

    # http_camera = HttpCamera('516c070a92fb4a48a151c63d0323201b')

    # print(http_camra.getLatestMetaDataByCameraId())
    while True:

        for key in http_cameras.keys():
            time.sleep(0.1)

            print(http_cameras[key].readCameraInfo()['im_path'])
