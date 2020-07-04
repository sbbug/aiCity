import os
import string
dirpath = "../Resources/ReportLog/FakeAbnormal"
filelist1 = os.listdir(dirpath)

def findImagePath(img_name):
    import glob

    for name in glob.glob(dirpath + "/*/*/*.jpg"):
        if name.find(img_name)!=-1:
            return name
    return ""


if __name__ == "__main__":

    #print(findImgPath(dirpath,"5ba8e997-340c-3649-a57a-b83729a3f592"))
    print(findImagePath("6e570572-d34d-3928-9b5d-0519e66fc4cc"))