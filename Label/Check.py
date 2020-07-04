'''
这个脚本文件用来标定每个摄像头的base图像
'''
import label
import cv2
import sys
sys.path.append("..")
import Functions
import Parameters
import os




# 根据文件名字获取cam_id
def getCamId(tpl_name):
    '''
    :param tpl_name: 图像名字
    :return: 摄像机编号
    '''
    tpl_name = str(tpl_name)

    # if tpl_name.find(".")==-1:
    #     functions.showError("传入的tpl_name文件名字是非法的")

    return tpl_name[0:tpl_name.index(".")]


def checkLabel():
    L = label.Label()

    # 获取模板文件下的所有模板图像名字
    tpl_name_list = os.listdir(Functions.getProjectContext() + Parameters.IMAGE_TEMPLATE)
    cv2.namedWindow('image')

    for tpl in tpl_name_list:

        # 读取模板图像
        template = L.getCamBaseImg(getCamId(tpl))
        # 读取配置信息
        config = L.getCamConfigFile(getCamId(tpl))
        print(config['ROI'] )
        for points in config['ROI']:
            for i in range(len(points) - 1):
                cv2.circle(template, (points[i][0], points[i][1]), 5, (0, 0, 255), thickness=-1)
                cv2.line(template, (points[i][0], points[i][1]), (points[i + 1][0], points[i + 1][1]), (0, 255, 0), 1)
                cv2.circle(template, (points[i + 1][0], points[i + 1][1]), 5, (0, 0, 255), thickness=-1)

        cv2.imshow('image', template)
        flag = cv2.waitKey(-1)
        # 下一张图像
        if flag & 0xFF == ord(' '):
            continue
    cv2.destroyAllWindows()

if __name__ == "__main__":
    '''
    使用说明
    空格键代表切换到下一张图像
    n代表切换到下一个感兴趣区域ROI
 
 
    '''

    checkLabel()

