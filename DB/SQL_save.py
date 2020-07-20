from DB.SQL_Init import SQLI
from Parameters import FEEDBACK_URL
import time
import requests
import json
from Functions import getProjectContext
import Parameters
import os
from Tool.logger.make_logger import make_logger



def getNum():
    sql = 'select * from NUM_FB'
    ob = SQLI('root', '123456Pa!', 'test')
    res = ob.find(sql)

    if len(res) == 0:
        return 0

    return res[0][0]


def setNum(num):
    sql = 'update NUM_FB set count = {}'.format(num)
    ob = SQLI('root', '123456Pa!', 'test')
    ob.update_data(sql)


NUM_FB = getNum()


def getFeedback():
    '''
    :param url:
    :return:
    '''
    result = []
    try:
       feedback = requests.get(FEEDBACK_URL)
       res = json.loads(feedback.text)
       totalPage = res['data']['totalPage']
       if res['code'] != 10001:
           print("获取事件列表时出现异常")
       else:
           result = []
           for i in range(int(NUM_FB/10)+1, totalPage+1):
               newurl = FEEDBACK_URL+"?current_page={}".format(i)
               feedback = requests.get(newurl)
               res = json.loads(feedback.text)
               print(res)
               if res['code'] != 10001:
                   print("获取事件列表时出现异常")
               else:
                   result.extend(res['data']['list'])
           return result
    except Exception as e:
        print("error:{}".format(e))
        #now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #functions.WriteErrorLog(now_time, "getFeedback接口请求异常", "SQL_save.py")

def dataProcess():
    list_fb = getFeedback()
    #print("normal1")
    if len(list_fb) <= NUM_FB%10:
        return []
    else:
        return list_fb[(NUM_FB % 10)-1:]

def dataRefresh():
    result = []
    picture_path = dict()
    datas = dataProcess()
    ReportPath = os.path.join(getProjectContext(), Parameters.CAMERA_REPORTED)
    getPciturePath(ReportPath, picture_path)
    for data in datas:
        no = str(data['picture_no'])
        no = no[0:no.find(';')]
        if no in picture_path:
            begin = picture_path[no].find('camera')
            end = picture_path[no].find('.log')
            camId = picture_path[no][begin:end]
            data['camId'] = camId
            data['path'] = picture_path[no]
            result.append(data)
    return result

def createLogDir():
    dirpath = '/home/aicity/code/cityManager/Resources/Log/' + str(time.strftime('%Y-%m-%d', time.localtime()))
    isExists = os.path.exists(dirpath)
    if not isExists:
        os.makedirs(dirpath)
        print('director created susccess!')

    return dirpath


def update_feedback():
    save_dir = createLogDir()
    logger = make_logger('SQL', save_dir, 'SQL_execute_log')
    insert_data = dataRefresh()
    count = NUM_FB+len(insert_data)
    if len(insert_data) == 0:
        # now_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        # line = now_time + " " + "No data update\n"
        line = "No data update\n"
        logger.info(line)
    else:
        #print("normal")
        SQL_Object = SQLI('root', '123456Pa!', 'test')
        now_time = time.strftime("%Y-%m-%d", time.localtime())
        for data in insert_data:
            #print(data)
            sql = "insert into feedback values(null,'{}','{}',{},{},'null',{},'{}','{}','{}')".format(data['picture_no'], data['meta'], data['exist_problem'], data['event_cate_id'], data['id'], now_time, data['camId'], data['path'])
            SQL_Object.update_data(sql)
        SQL_Object.close()
        setNum(count)
        # now_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        # line = now_time + " " + "update {} datas\n".format(len(insert_data))
        line = "update {} datas\n".format(len(insert_data))
        logger.info(line)
        print('finish!')


def search(col):
    sql = "select {} from feedback".format(col)
    SQL_Object = SQLI('root', '123456Pa!', 'test')
    #print(SQL_Object.find(sql))
    return SQL_Object.find(sql)

def getPciturePath(dir, picture_dic):

    cam_dir = os.listdir(dir)
    for f_or_d in cam_dir:
        fd_path = os.path.join(dir, f_or_d)
        if os.path.isdir(fd_path):
            getPciturePath(fd_path, picture_dic)
        elif os.path.isfile(fd_path) & f_or_d.endswith('.log'):
            with open(fd_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    li = line.strip().split()
                    picture_dic[li[6]] = fd_path
        else:
            pass

def updateCamId():
    table = 'feedback'
    columns = ['camId', 'path']
    types = ['varchar(50)', 'varchar(300)']
    SQL_Object = SQLI('root', '123456Pa!', 'test')
    #SQL_Object.add_column(table, columns, types)

    picture_path = dict()
    # 获取存储已上报异常的目录
    ReportPath = os.path.join(getProjectContext(), Parameters.CAMERA_REPORTED)
    getPciturePath(ReportPath, picture_path)

    sql = 'select picture_no,id from feedback;'
    res = SQL_Object.find(sql)
    count = 0
    #res = list(res)
    #print(res)
    for (no, id) in res:
        no = no[0:no.find(';')]
        if no in picture_path:
            begin = picture_path[no].find('camera')
            end = picture_path[no].find('.log')
            camId = picture_path[no][begin:end]
            sql_1 = 'update feedback set camId="{}",path="{}" where id={};'.format(camId, picture_path[no], id)
            SQL_Object.update_data(sql_1)
            #print('{}:{}'.format(camId, picture_path[no]))
            print('{}:{}'.format(no, id))
            count += 1
    print(count)
    SQL_Object.close()


if __name__ == "__main__":
    #pass
    #update()
    #search()
    getFeedback()
    # update_feedback()
    #updateCamId()
