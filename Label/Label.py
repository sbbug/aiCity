'''
这是一个软件标注的工具类，方法采用静态方法
'''
import json
import os
import cv2
import sys
sys.path.append("..")
import Parameters as const
import Functions

# 软件标注的方法类
class Label:

    # 构造
    def __init__(self):
        pass

    # 打开文件的基本方法，获取文件句柄
    @staticmethod
    def openFile(path):
        # 文件异常处理
        try:
            file = open(path,encoding="utf-8")

        except IOError:
            print("Error: 没有找到文件或读取文件失败")

        return file

    # 加载摄像头基本信息
    @staticmethod
    def loadIPConfig(camera_config_path):
        '''
        :param camera_config_path:
        :return:
        '''

        # 使用默认路径
        if camera_config_path is None or camera_config_path=="":
            camera_config_path = const.CAMERAS_CONFIG

        # 文件异常处理
        try:
            file = open(camera_config_path)

        except IOError:
            print("Error: 没有找到文件或读取文件失败")

        result = json.load(file)
        cameras = []

        # 将摄像头信息以列表形式返回
        for c in result['cameras']:
            cameras.append(result['cameras'][c])

        return cameras

    # 根据摄像头的编号获取基准图片
    @staticmethod
    def getCamBaseImg(cam_id):
        '''
        :param cam_id:
        :return:
        '''

        base_path = Functions.getProjectContext() + os.path.join(const.IMAGE_TEMPLATE, str(cam_id) + ".jpg")

        # 判断基准图片是否存在
        if os.path.exists(base_path)==False:
            base_path = os.path.join(const.IMAGE_TEMPLATE, "default.jpg")

        return cv2.imread(base_path)

    # 根据摄像头的编号获取摄像头场景的配置文件
    @staticmethod
    def getCamConfigFile(cam_id):
        '''
        :param cam_id:
        :return:
        '''

        base_config_path = Functions.getProjectContext() + os.path.join(const.IMAGE_CONFIG, str(cam_id) + ".json")

        # 首先判断该配置文件是否存在
        # 不存在时,从模板文件里读取格式信息
        if not os.path.exists(base_config_path):
            file = Label.openFile(Functions.getProjectContext() + const.IMAGE_CONFIG_TPL)
        # 存在时
        else:
            file = Label.openFile(base_config_path)

        return json.load(file)

    # 根据摄像头的编号将配置文件写入
    @staticmethod
    def writeCamConfig(cam_id,cam_config):
        '''
        :param cam_id:
        :param cam_config: 内容
        :return:
        '''

        base_config_path = os.path.join(Functions.getProjectContext() + const.IMAGE_CONFIG, str(cam_id) + ".json")

        # 文件异常处理
        try:
            file = open(base_config_path,mode="w",encoding="utf-8")

        except IOError:
            print("Error: 没有找到文件或读取文件失败")

        json.dump(cam_config,file,ensure_ascii=False)
        file.close()



if __name__ =="__main__":

    label = Label()
    res = label.loadIPConfig(const.CAMERAS_CONFIG)

    content = label.getCamConfigFile(res[0]['cam_id'])

    label.writeCamConfig(res[0]['cam_id'],content)