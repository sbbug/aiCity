from Algorithm.ResNet.classInter import ClassInter
import cv2
from PIL import Image
import torch
from torchvision import datasets, models, transforms
import os
import torch.nn as nn


def transformType(img):
    transform = transforms.Compose([
        transforms.Resize(224),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    return transform(img)

class_index = {
            "back": 0,
            "car": 1,
            "exposedTrash": 2,
            "illegalStand":3,
            "person":4,
            "shadow":5,
            "uoDoFacility":6,
            "uoRoad":7
        }
if __name__ == "__main__":

    imgs_path = "./input_images"

    classInter = ClassInter(8)

    sotfmax = nn.Softmax()
    for im_path in os.listdir(imgs_path):
        img_path = os.path.join(imgs_path, im_path)


        im = cv2.imread(img_path)

        print(im_path,classInter.getCls(im))

        # with open(img_path, "rb") as im:
        #     img = Image.open(im).convert("RGB")
        #
        # img = transformType(img)
        #
        # img = img.unsqueeze(0)
        #
        # output = classInter(img)
        # # print(output)
        # _, preds = torch.max(sotfmax(output), 1)
        #
        # print(im_path, preds.item(), sotfmax(output))
