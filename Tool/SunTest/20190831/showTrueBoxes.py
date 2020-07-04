from Functions import getProjectContext
import os
import cv2

if __name__ =="__main__":


    path = os.path.join(getProjectContext(),"Tool")
    result_images = "res_img"

    color = {"false":(255,255,0),"true":(255,255,)}

    log_path = os.path.join(path,"trueAbnormalsRecord.log")
    img_path = os.path.join(path,"JPEGImages")

    false_abnormals = []
    file_log = open(log_path,"r")
    log = file_log.readline()
    while log:
        false_abnormals.append(log.replace("\n","").split(" "))
        log = file_log.readline()
    file_log.close()

    print("false_abnormals",false_abnormals)
    print("len",len(false_abnormals))

    images = dict()
    for abnormal in false_abnormals:

        if not images.__contains__('{}.jpg'.format(abnormal[-1])):
            im_path = os.path.join(img_path, '{}.jpg'.format(abnormal[-1]))
            img_data = cv2.imread(im_path)
            images['{}.jpg'.format(abnormal[-1])] = img_data
        print(abnormal)
        left = int(abnormal[2])
        top = int(abnormal[3])
        bottom = top + int(abnormal[5])
        right = left + int(abnormal[4])
        cv2.rectangle(images['{}.jpg'.format(abnormal[-1])],(left,top),(right,bottom),color['true'],4)
    for im_key in images:
        print(images[im_key])
        cv2.imwrite(os.path.join("./res_img",im_key),images[im_key])
