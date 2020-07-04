'''
这个脚本文件用来标定每个摄像头的base图像
'''
import sys
sys.path.append("..")
import cv2
import Functions
import os
import Parameters
import Label.Label as label

vars = {}
vars['now_x'] = 0
vars['now_y'] = 0
vars['i'] = 0
vars['flag'] = None
def transformCoordinate(x,y):

    return x,y

def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    '''
    :param event: 事件
    :param x: 坐标
    :param y: 坐标
    :param flags:
    :param param:
    :return: 无
    '''
    if event == cv2.EVENT_LBUTTONDOWN:
        vars['now_x'],vars['now_y'] = transformCoordinate(x,y)

# 根据文件名字获取cam_id
def getCamId(tpl_name):
    '''
    :param tpl_name: 图像名字
    :return: 摄像机编号
    '''
    tpl_name = str(tpl_name)

    if tpl_name.find(".")==-1:
        Functions.showError("传入的tpl_name文件名字是非法的")

    return tpl_name[0:tpl_name.index(".")]

# 根据cam_id将标定信息写入到配置文件里
def writeSpaceToConfig(spaces,cam_id):
    '''
    :param spaces: 已经标注好的区域
    :param cam_id: 摄像机编号
    :return:
    '''
    L = label.Label()
    config = L.getCamConfigFile(cam_id)
    # 将标注好的感兴趣区域添加到配置文件里
    config['ROI'] = spaces
    # 将信息进行保存
    L.writeCamConfig(cam_id,config)

    print(config)

# @pysnooper.snoop()
def startLabel():

    L = label.Label()

    # 标定场景信息
    # 获取模板文件下的所有模板图像名字
    tpl_name_list = os.listdir(Functions.getProjectContext() + Parameters.IMAGE_TEMPLATE)

    cv2.namedWindow('image')
    cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
    spaces = []  # 存储多个区域
    points = []  # 存储区域坐标

    while vars['i'] < len(tpl_name_list):

        # 读取模板图像
        template = L.getCamBaseImg(getCamId(tpl_name_list[vars['i']]))

        # 鼠标点击，坐标加入列表
        if vars['now_x'] != 0 or vars['now_y'] != 0:
            # 入栈
            points.append([vars['now_x'], vars['now_y']])
            # 归零
            vars['now_x'] = 0
            vars['now_y'] = 0

        # 绘图
        if len(points) > 0:
            for i in range(len(points) - 1):
                cv2.circle(template, (points[i][0], points[i][1]), 5, (0, 0, 255), thickness=-1)
                cv2.line(template, (points[i][0], points[i][1]), (points[i + 1][0], points[i + 1][1]), (0, 255, 0), 1)
                cv2.circle(template, (points[i + 1][0], points[i + 1][1]), 5, (0, 0, 255), thickness=-1)

        cv2.imshow('image', template)

        flag = cv2.waitKey(2)
        # 下一个需要标定的区域
        if flag & 0xFF == ord('n'):
            if len(points) != 0:
                spaces.append(points)
                points = [] # 在这里points.clear()与points = []效果不一样，使用第一个会将spaces里的也消除掉
                vars['now_x'] = 0
                vars['now_y'] = 0

        # 下一张图像
        if flag & 0xFF == ord(' '):
            spaces.append(points)
            if len(spaces) != 0:
                # 标定信息写入配置文件
                cam_id = getCamId(tpl_name_list[vars['i']])
                writeSpaceToConfig(spaces, cam_id)

                spaces = []
            if len(points) != 0:
                points = []

            vars['now_x'] = 0
            vars['now_y'] = 0
            vars['i'] = vars['i'] + 1
    cv2.destroyAllWindows()


if __name__ =="__main__":
   '''
   使用说明
   空格键代表切换到下一张图像
   n代表切换到下一个感兴趣区域ROI
   
   
   '''
   startLabel()

