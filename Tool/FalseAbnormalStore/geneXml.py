'''
1564022287 ExposedTrash 674 718 121 165 17b739b1-ef8c-3f04-84e8-570204fdbcd5
生成voc格式的xml
'''
from lxml.etree import Element, SubElement, tostring
from Tool.TrueAbnormalStore.findImagePath import findImagePath
import os
import shutil
object = {
    "name":"other",
    "pose":"Unspecified",
    "truncated":"0",
    "difficult":"0",
    "bndbox":{
        "xmin":"",
        "ymin":"",
        "xmax":"",
        "ymax":""
    }
}
elements = {
     "folder":"xml",
     "filename":"",
      "path":"xxxx",
     "source":{
         "database":"Unknown"
     },
      "size":{
          "width":"1280",
          "height":"720",
          "depath":"3"
      },
      "segmented":"0",
      "object":""
}
location = {"xmin":0,"ymin":1,"xmax":2,"ymax":3}

def CreateObject(root,elements,data):
    for key in elements.keys():
        if isinstance(elements[key],dict):
            temp = SubElement(root, key)
            CreateObject(temp,elements[key],data)
        elif key in ["xmin","ymin","xmax","ymax"]:
            node = SubElement(root, key)
            if key in ["xmin","ymin"]:
                node.text = str(data[location[key]])
            elif key == "xmax":
                node.text = str(data[location[key]]+data[0])
            elif key =="ymax":
                node.text = str(data[location[key]]+data[1])
        else:
            node = SubElement(root, key)
            node.text = elements[key]

def createRoot(root,elements,data,name):
    for key in elements.keys():
        if isinstance(elements[key],dict):
            temp = SubElement(root, key)
            createRoot(temp,elements[key],data,name)
        else:
            if key == "filename":
                node = SubElement(root, key)
                node.text = name
            elif key == "object":
                for d in data:
                    temp = SubElement(root, key)
                    CreateObject(temp,object,d)
            else:
                node = SubElement(root, key)
                node.text = elements[key]
def getSampleRecords(file_path = "./FalseAbnormalsRecord.log"):

    file = open(file_path,"r")
    abnormals = []
    line = file.readline()
    while line:
        line = line.replace("\n","")
        abnormals.append(line)
        line = file.readline()

    file.close()

    return abnormals

if __name__ =="__main__":

    samples = getSampleRecords()
    samples_set = dict()
    for sample in samples:
        data = sample.split(" ")
        if not samples_set.__contains__(data[1]):
            samples_set[data[1]] = [[int(data[2]),int(data[3]),int(data[4]),int(data[5])]]
        else:
            samples_set[data[1]].append([int(data[2]),int(data[3]),int(data[4]),int(data[5])])

    for s in samples_set.keys():

        img_path = findImagePath(s)
        if img_path == "":
            continue

        boxes = samples_set[s]
        # generate xml
        root = Element('annotation')
        createRoot(root, elements, boxes,'{}.jpg'.format(s))
        xml = tostring(root, pretty_print=True)  #格式化显示，该换行的换行
        with open(os.path.join("./Annotations",s+".xml"), 'wb') as f:
            f.write(xml)
        # copy img
        dist_dir = "./JPEGImages"
        shutil.copy(img_path,dist_dir)
        print(img_path)



