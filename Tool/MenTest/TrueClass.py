import os
import xml.etree.ElementTree as ET
import cv2
import uuid

images_path = '/home/user/code/manager/data/VOCdevkit2007/VOC2007/JPEGImages'
xmls_path = '/home/user/code/manager/data/VOCdevkit2007/VOC2007/Annotations'
new_image_path = '/home/user/code/trainData/crop/train/TrueClass'

images = os.listdir(images_path)
xmls = os.listdir(xmls_path)
print(len(xmls))
# count = 813

for xml in xmls:
    if not xml.endswith('.xml'):
        continue
    image_name = f'{xml[:-4]}.jpg'
    xml_path = os.path.join(xmls_path, xml)
    img_path = os.path.join(images_path, image_name)
    print(xml_path)
    tree = ET.parse(xml_path)
    root = tree.getroot()
    for obj in root.findall('object'):
        className = obj.find('name').text
        xmin = int(obj.find('bndbox/xmin').text)
        ymin = int(obj.find('bndbox/ymin').text)
        xmax = int(obj.find('bndbox/xmax').text)
        ymax = int(obj.find('bndbox/ymax').text)
        img = cv2.imread(img_path)
        cut_img = img[ymin:ymax+1, xmin:xmax+1, :]
        new_img_dir = os.path.join(new_image_path, className)
        if os.path.isdir(new_img_dir):
            cut_name = os.path.join(new_img_dir, str(uuid.uuid1())+'.jpg')
            cv2.imwrite(cut_name, cut_img)
            print('success: ', xml)
        else:
            print(xml)
            break
    # break