import os
import xml.etree.ElementTree as ET
import cv2

path_to_annotations_dir = "/home/user/code/trainData/xml"
path_to_image_dir = "/home/user/code/trainData/image"
save_dir = "/home/user/code/trainData/crop/"
save_person_dir = "/home/user/code/trainData/crop/"

if __name__ == "__main__":

    image_ids = []

    for xml_name in os.listdir(path_to_annotations_dir):
        image_ids.append(xml_name.split(".")[0])

    i = 0
    for image_id in image_ids:

        path_to_annotation_xml = os.path.join(path_to_annotations_dir, f'{image_id}.xml')
        path_to_annotation_img = os.path.join(path_to_image_dir, f'{image_id}.jpg')

        image = cv2.imread(path_to_annotation_img)

        tree = ET.ElementTree(file=path_to_annotation_xml)
        root = tree.getroot()

        for tag_object in root.iterfind('object'):
            left = int(next(tag_object.iterfind('bndbox/xmin')).text)
            top = int(next(tag_object.iterfind('bndbox/ymin')).text)
            right = int(next(tag_object.iterfind('bndbox/xmax')).text)
            bottom = int(next(tag_object.iterfind('bndbox/ymax')).text)

            crop = image[top:bottom,left:right, :]

            name = next(tag_object.iterfind('name')).text

            cv2.imwrite(os.path.join(save_dir,name,str(i)+".jpg"),crop)

            i+=1

            print(name)
