import os
import re
import cv2
log_dir = '/home/user/code/cityManager/Resources/ReportLog/ReportedAbnormal'
image_dir_path = '/home/user/code/cityManager/Resources/ReportLog/FakeAbnormal'
save_path = '/home/user/code/trainData/crop/train/back'
log_dir_list = os.listdir(log_dir)

for dir_name in log_dir_list:
    match = re.search(r'2020-0[34]-[0|2][0-9]', dir_name)
    if not match:
        continue
    cameral_log_path = os.path.join(log_dir, dir_name)
    image_list_dir = os.path.join(image_dir_path, dir_name)
    cameral_log_list = os.listdir(cameral_log_path)
    print(dir_name)
    for cameral_log in cameral_log_list:
        print(cameral_log)
        cameral_path = os.path.join(cameral_log_path, cameral_log)
        cameral_number = cameral_log[:-4]
        image_dir = os.path.join(image_list_dir, cameral_number)
        image_list = os.listdir(image_dir)
        # print(cameral_path)
        with open(cameral_path, 'r') as f:
            datas = f.readlines()
        # print(datas)
        for line in datas:
            _, _, x, y, w, h, image_name = line.split(' ')
            # print(type(x), type(y))
            x = int(x)
            y = int(y)
            w = int(w)
            h = int(h)
            image_name = image_name.strip('\n')
            image_name = f'{image_name}.jpg'
            print(image_name)
            if image_name not in image_list:
                continue
            image_path = os.path.join(image_dir, image_name)
            image = cv2.imread(image_path)
            # print(image.shape)

            cut_img = image[y:y+h+1, x:x+w+1, ]
            save_img_path = os.path.join(save_path, image_name)
            # cv2.imshow('test', cut_img)
            # cv2.waitKey(0)
            cv2.imwrite(save_img_path, cut_img)



