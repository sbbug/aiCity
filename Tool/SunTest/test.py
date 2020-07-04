


import os
import time

def get_now_time():
    now_time = time.localtime()
    ntime = "{}:{:0>2d}".format(now_time.tm_hour, (now_time.tm_min % 60))
    return ntime
if __name__ == "__main__":

    # xml_path = "../Annotations/"
    # img_path = "../JPEGImages/"
    # xml_paths = os.listdir(xml_path)
    # img_paths = os.listdir(img_path)
    #
    # for xml in xml_paths:
    #     temp = xml.split(".")[0]
    #     img_p = os.path.join(img_path,temp+".jpg")
    #     if os.path.exists(img_p):
    #         print(xml)
    starttime = "10:14"  # e.g. 14:14
    stoptime = "06:00"  # e.g. 14:23
    ntime = get_now_time()
    print(ntime>starttime)
    print(ntime<stoptime)