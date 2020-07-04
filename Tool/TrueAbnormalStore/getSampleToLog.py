import requests
import Parameters
import json
import Functions
import cv2
import time
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

if __name__ == "__main__":

  event_name_name = {
      "暴露垃圾":"ExposedTrash",
      "擅自占用道路堆物、施工":"UORoads",
      "占道无证经营、跨门营业":"IllegalStand",
      "乱设或损坏户外设施":"UoDOFacilities"
  }
  #{7: 'ExposedTrash', 10: 'UORoads', 12: 'IllegalStand', 9: 'UoDOFacilities'}
  event_id_name = {}
  events = getEventCode()

  for name in event_name_name.keys():
    for event in events:
        if event['event_name']==name:
            event_id_name[event['id']] = event_name_name[name]

  totalPage = getSample(1,10)['totalPage']
  true_abnormal=0
  true_abnormal_set = []

  for i in range(1,totalPage):
    result = getSample(i,10)
    all_abnormals = result['list']
    for abnormal in all_abnormals:
        if abnormal['exist_problem']==True:
            true_abnormal = true_abnormal+1
            abnormal['event_cate_name'] = event_id_name[abnormal['event_cate_id']]
            #print(abnormal["picture_no"])
            true_abnormal_set.append(abnormal)
  print("true_abnormal",true_abnormal)

  file = open("trueAbnormalsRecord.log","w")
  for abnormal_set in true_abnormal_set:
      record = "123"
      record = record + " " + abnormal_set['event_cate_name']
      elements = abnormal_set['meta'].split(",")
      record = record + " " + elements[0] + " " + elements[1] + " " + elements[2] + " " + elements[3]
      record = record + " " +abnormal_set['picture_no'].split(";")[0]+"\n"
      #print(record)
      file.write(record)
  file.close()


