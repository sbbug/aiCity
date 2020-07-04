from Functions import getProjectContext
import os
import cv2

if __name__ =="__main__":

    date = "2019-09-09"
    camera_id = "camera_26"
    path = os.path.join(getProjectContext(),"Resources/ReportLog/ReportedAbnormal")
    image_path = os.path.join(getProjectContext(),"Resources/ReportLog/FakeAbnormal")
    result_images = "res_img"

    color = {"false":(255,255,0),"true":(0,0,255)}

    log_path = os.path.join(path,date,camera_id+".log")
    img_path = os.path.join(image_path,date,camera_id)

    false_abnormals = []
    file_log = open(log_path,"r")
    log = file_log.readline()

    while log:
        false_abnormals.append(log.replace("\n","").split(" "))
        log = file_log.readline()

    file_log.close()
    print("false_abnormals",false_abnormals)
    print("len",len(false_abnormals))

    im_path = os.path.join(img_path, '{}.jpg'.format(false_abnormals[0][6]))

    img_data = cv2.imread(im_path)

    for abnormal in false_abnormals:

        left = int(abnormal[2])
        top = int(abnormal[3])
        bottom = top + int(abnormal[5])
        right = left + int(abnormal[4])
        cv2.rectangle(img_data,(left,top),(right,bottom),color['false'],1)

    path = os.path.join(getProjectContext(), "Resources/ReportLog/ReportedAbnormal")
    result_images = "res_img"

    log_path = os.path.join(path, date, camera_id + ".log")

    true_abnormals = []

    file_log = open(log_path, "r")
    log = file_log.readline()

    while log:
        true_abnormals.append(log.replace("\n", "").split(" "))
        log = file_log.readline()

    file_log.close()
    print("true_abnormals", true_abnormals)
    print("len", len(true_abnormals))
    for abnormal in true_abnormals:

        left = int(abnormal[2])
        top = int(abnormal[3])
        bottom = top + int(abnormal[5])
        right = left + int(abnormal[4])
        cv2.rectangle(img_data,(left,top),(right,bottom),color['true'],4)
    cv2.imwrite(os.path.join(result_images,'{}.jpg'.format(camera_id)),img_data)
