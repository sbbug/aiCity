'''
1564022287 ExposedTrash 674 718 121 165 17b739b1-ef8c-3f04-84e8-570204fdbcd5
生成voc格式的xml
'''
from lxml.etree import SubElement
from Tool.TrueAbnormalStore.findImagePath import findImagePath
import shutil
object = {
    "name":"",
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
location = {"name":1,"xmin":2,"ymin":3,"xmax":4,"ymax":5}

def CreateObject(root,elements,data):
    for key in elements.keys():
        if isinstance(elements[key],dict):
            temp = SubElement(root, key)
            CreateObject(temp,elements[key],data)
        elif key in ["name","xmin","ymin","xmax","ymax"]:
            node = SubElement(root, key)
            node.text = data[location[key]]
        else:
            node = SubElement(root, key)
            node.text = elements[key]

def createRoot(root,elements,data):
    for key in elements.keys():
        if isinstance(elements[key],dict):
            temp = SubElement(root, key)
            createRoot(temp,elements[key],data)
        else:
            if key == "filename":
                node = SubElement(root, key)
                node.text = data[6]
            elif key == "object":
                temp = SubElement(root, key)
                CreateObject(temp,object,data)
            else:
                node = SubElement(root, key)
                node.text = elements[key]
def getSampleRecords(file_path = "./trueAbnormalsRecord.log"):

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

    for sample in samples:
        data = sample.split(" ")
        img_path = findImagePath(data[6])

        if img_path == "":
            continue
        # generate xml
        # root = Element('annotation')
        # createRoot(root, elements, data)
        # xml = tostring(root, pretty_print=True)  #格式化显示，该换行的换行
        # with open(os.path.join("./Annotations",data[6]+".xml"), 'wb') as f:
        #     f.write(xml)
        # copy img
        dist_dir = "./JPEGImages"
        shutil.copy(img_path,dist_dir)
        print(img_path)

