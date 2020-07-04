import requests
import Parameters
import json
import Functions
import cv2
import time


# 将事件录入到数据库
def addEvent(data, logger):
    try:

        data = json.dumps(data)
        # http://app.sucslife.com:8090/zpcg/api/public/video/event/problem
        # http://zpcg.sucslife.com:8090/api//public/video/event/problem
        res = requests.post("http://zpcg.sucslife.com:8090/api//public/video/event/problem", data=data,
                            headers={"Content-Type": "application/json"})

        if res.text:
            res = json.loads(res.text)
            if res['status'] == 200 and res['msg'] == "suc":
                logger.info("network_2 录入成功")
        else:
            logger.info("net_work_2-----addEvent(data) res = requests.post(parameters.ADD_EVENT_URL,data=data) 接口异常")
            logger.info(res)
    except:
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logger.error(now_time, "addEvent接口请求异常", "network.py")


# 获取事件列表测试接口
def getEventCode():
    '''
    :param url:
    :return:
    '''
    # res = requests.post('http://127.0.0.1:5050/getCamIP', data=data.encode("utf-8"))
    result = {}
    try:
        event = requests.get(Parameters.EVENT_URL)
        res = json.loads(event.text)
        if res['code'] != 10001:
            print("获取事件列表时出现异常")
        else:
            result = res['data']
    except:
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("{} getEventCode接口请求异常 network.py".format(now_time))
        # functions.WriteErrorLog(now_time, "getEventCode接口请求异常", "network.py")

    return result


# 上传图片到系统
def uploadImage(img_path,logger):
    '''
    :param img_path:
    :return:
    '''
    files = {
        "file": open(img_path, "rb")
    }
    result = ""
    try:
        # old path :http://app.sucslife.com:8090/zpcg/api/file/video/upload/image
        r = requests.post("http://zpcg.sucslife.com:8090/api/public/video/upload/image", files=files)
        res = json.loads(r.text)
        logger.info(res)
        if res['status'] == 200 and res['msg'] == 'suc':
            logger.info("图片上传成功")
            result = res['data']
    except:
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logger.error(now_time, "uploadImage接口请求异常", "network.py")

    return result


def sendAbormalsToIt(data, img_path, logger):
    '''
    :param data:传入事件异常信息{
    'cam_id': 'camera_2',
    'type': 'None',
    'x': 808,
    'y': 293,
    'w': 266,
    'h': 165,
    'time':
    1557727713}
    :param img:图像路径
    :return:
    '''
    camera_config = Functions.loadIPConfig(Functions.getProjectContext() + Parameters.CAMERAS_CONFIG)
    abnormal_data = {}
    # 获取经纬度信息
    for camera in camera_config:
        if camera['cam_id'] == data['cam_id']:
            abnormal_data['latitude'] = camera['latitude']
            abnormal_data['longitude'] = camera['longitude']
            break
    # 获取摄像机编号
    abnormal_data['camera_no'] = str(data['cam_id']).split("_")[0]
    # 获取宜昌区域bounding box
    abnormal_data['meta'] = [data['x'], data['y'], data['w'], data['h']]
    # 获取事件编号
    events = getEventCode()
    for event in events:
        if event['event_name'] == Functions.isType(data['type']):
            abnormal_data['event_cate_id'] = str(event['id'])
            break
    # 上传图片
    img_path_1 = uploadImage(img_path,logger)
    # 将异常图片裁剪并保存
    temp_img = cv2.imread(img_path)
    # 将裁剪好的异常区域图片进行处理，使它更加清晰
    cut_img = temp_img[data['y']:data['y'] + data['h'], data['x']:data['x'] + data['w']]
    cut_img = Functions.adjustGamma(cut_img, 2.0)
    cv2.imwrite(Parameters.CACHE + "temp.jpg", cut_img)
    img_path_2 = uploadImage(Functions.getProjectContext() + Parameters.CACHE + "temp.jpg",logger)

    # 获取图像路径
    abnormal_data['problem_pic'] = img_path_1 + ";" + img_path_2
    # 获取图像编号
    abnormal_data['picture_no'] = str(data['imgId']) + ";" + str(data['imgId']) + "_cut"

    logger.info(abnormal_data)
    # 将最终事件信息录入到系统
    addEvent(abnormal_data, logger)


def sendAbormalsToItTest():
    '''
    :param data:传入事件异常信息{'cam_id': 'camera_2', 'type': 'None', 'x': 808, 'y': 293, 'w': 266, 'h': 165, 'time': 1557727713}
    :param img:图像路径
    :return:
    '''

    abnormal_data = dict()

    abnormal_data['event_cate_id'] = "1234569"
    abnormal_data['camera_no'] = "002"
    abnormal_data['picture_no'] = "xb006;xb007"
    abnormal_data[
        'problem_pic'] = "/upload/20200325/temp/6-20200325181424.png;/upload/20200325/temp/6-20200325181424.png"
    abnormal_data['latitude'] = "121.23435"
    abnormal_data['longitude'] = "31.115343"
    abnormal_data['meta'] = "[10,10,20,20]"
    abnormal_data['ResultType'] = 0

    # 将最终事件信息录入到系统
    addEvent(abnormal_data)


# 将摄像头基本信息录入到数据库
def insertCamera():
    '''
    :return:
    '''
    cameras = Functions.loadIPConfig(Functions.getProjectContext() + Parameters.CAMERAS_CONFIG)
    for camera in cameras:
        data = json.dumps({
            "camera_no": camera['cam_id'],
            "address": camera['address'],
            "latitude": camera['latitude'],
            "longitude": camera['longitude']
        })
        # 需要以字典的形式传递到对方接口
        data = json.loads(data)
        res = requests.post(Parameters.ADD_CAMERA_URL, data=data)
        ret = json.loads(res.text)

        if ret['code'] == 10001:
            print("succed")
        else:
            print("failed")


if __name__ == "__main__":
    # print(getEventCode())

    sendAbormalsToItTest()
    uploadImage("../Resources/Cache/camera_5.jpg")
