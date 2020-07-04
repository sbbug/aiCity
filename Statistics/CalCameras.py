import os
from Functions import getProjectContext
if __name__ == "__main__":
    dir = "Resources/HttpCameras"
    date = "2020-05-25"


    for idx,camera in enumerate(os.listdir(getProjectContext()+os.path.join(dir,date))):

        print(idx)

        for angle in os.listdir(getProjectContext()+os.path.join(dir,date,camera)):

            print("------",angle)


