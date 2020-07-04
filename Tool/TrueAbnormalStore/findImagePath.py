import os
import string
dirpath = "../../Resources/ReportLog/FakeAbnormal"
filelist1 = os.listdir(dirpath)

def findImagePath(img_name):
    import glob

    for name in glob.glob(dirpath + "/*/*/*.jpg"):
        if name.find(img_name)!=-1:
            return name
    return ""

def findImgPath(now_path,img_name):

    if now_path.endswith(".log") or now_path.endswith(".jpg"):
        if now_path.find(img_name) != -1:
            print("now+path",now_path)
            return now_path
    else:
        dirs = os.listdir(now_path)
        for dir in dirs:
            path = os.path.join(now_path,dir)
          # print(path)
            findImgPath(path,img_name)

def findResult(imgname,):
    imgname = imgname + ".jpg"
    result = ""
    path = ""
    path1 = ""
    for file in filelist1:
        imagelist = os.listdir(os.path.join(dirpath, file))
        path = os.path.join(dirpath, file)
        for image in imagelist:
            if image.endswith(".log"):
                continue
            else:
                path1 = os.path.join(path, image)
                imagelist1 = os.listdir(os.path.join(path, image))
                for img in imagelist1:
                    if imgname in img:
                        result = img
                        break
    result = os.path.join(path1, result)
    return result


if __name__ == "__main__":
    # image = input("Please input the name of image(not .jpg):")
    # result = findResult(image)
    # if result == "":
    #     print("This image is not exist")
    # else:
    #     print(result)

    #print(type(path))

    #print(findImgPath(dirpath,"5ba8e997-340c-3649-a57a-b83729a3f592"))
    print(findImagePath("6e570572-d34d-3928-9b5d-0519e66fc4cc"))