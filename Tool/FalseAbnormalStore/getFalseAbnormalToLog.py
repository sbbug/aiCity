import requests
import Parameters
import json
import Functions
import cv2
import time
import re
import numpy as np
np.set_printoptions(threshold=np.inf)


dirpath = "../../Resources/ReportLog/FakeAbnormal"

def findImagePath(img_name):
    import glob

    for name in glob.glob(dirpath + "/*/*/*.jpg"):
        if name.find(img_name)!=-1:
            return name
    return ""
# 获取事件列表测试接口
def getEventCode():
    '''
    :param url:
    :return:
    '''
    #res = requests.post('http://127.0.0.1:5050/getCamIP', data=data.encode("utf-8"))
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
        Functions.WriteErrorLog(now_time, "getEventCode接口请求异常", "network.py")

    return result
# 获取样本数据
def getSample(cur_page=1,page_size=10):
    '''
    :param url:
    :return:
    '''

    result = None
    try:
       sample = requests.get("http://aicity.hualinfo.com:7902/video/event/feedback?current_page="+str(cur_page)+"&page_size="+str(page_size))
       res = json.loads(sample.text)
       if res['code'] != 10001:
           print("获取事件列表时出现异常")
       else:
           result = res['data']
    except:
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        Functions.WriteErrorLog(now_time, "getSample接口请求异常", "network.py")

    return result

def getCameraNo(img_path):

    pattern = r'camera_([0-9]+)'
    res = re.search(pattern,img_path)

    return res.group()

if __name__ == "__main__":


  totalPage = getSample(1,100)['totalPage']
  False_abnormal_set = []


  for i in range(1,totalPage):
    result = getSample(i,100)
    all_abnormals = result['list']
    for abnormal in all_abnormals:
        if abnormal['exist_problem']==False:
            if abnormal.get("picture_no") != None:
                False_abnormal_set.append(abnormal)

  print("finish network request")

  print("filter current image id")

  current_false_abnormal = []
  for abnormal in False_abnormal_set:
      img_name = abnormal['picture_no'].split(";")[0]
      print(img_name)
      img_path = findImagePath(img_name)

      if img_path != "":
        print(img_path)
        false_abnormal = {}
        false_abnormal['id'] = abnormal['id']
        false_abnormal['picture_no'] = abnormal['picture_no'].split(";")[0]
        elements = abnormal['meta'].split(",")
        false_abnormal['x'] = int(elements[0])
        false_abnormal['y'] = int(elements[1])
        false_abnormal['w'] = int(elements[2])
        false_abnormal['h'] = int(elements[3])
        current_false_abnormal.append(false_abnormal)

  print("start filted false abormal write file")

  false_file = open("FalseAbnormalsRecord.log","w")
  for abnormal in current_false_abnormal:
      false_file.write(str(abnormal['id'])+" "+abnormal['picture_no']+" "+str(abnormal['x'])+" "+str(abnormal['y'])+" "+str(abnormal['w'])+" "+str(abnormal['h'])+"\n")

  false_file.close()

  print("finsh write log")




