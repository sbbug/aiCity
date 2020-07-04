import argparse
import torch
from torch.autograd import Variable
import os
from Algorithm.Model.utils import get_network, get_test_dataloader
from PIL import Image
import torchvision.transforms as transforms
import Algorithm.Model.conf.global_settings as config
import cv2
from Functions import getProjectContext
from Parameters import VGG_MODEL_PATH
class Vgg(object):

    class arg:
        net = "vgg16"
        model_path = getProjectContext()+VGG_MODEL_PATH
        gpu = True

    Net = None
    def __init__(self):
        super(Vgg, self).__init__()
        Vgg.loadModel()

        self.index_class = {0: "暴露垃圾", 1: "占道无证经营、跨门营业", 2: "乱设或损坏户外设施", 3: "占道无证经营、跨门营业"}
        self.img_path = "./images"

        self.transform_test = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
            transforms.Normalize(config.MANAGER_TRAIN_MEAN, config.MANAGER_TRAIN_STD)
        ])

    @classmethod
    def loadModel(self):
        '''
        :return:
        '''
        if self.Net is None:
            self.Net = get_network(self.arg, use_gpu=self.arg.gpu)
            print(__file__)
            self.Net.load_state_dict(torch.load(self.arg.model_path), self.arg.gpu)
            self.Net.eval()
            print("load model finished")


    def getInput(self,img_path):
        with open(img_path, "rb") as im:
            img_data = Image.open(im).convert("RGB")

        img_data = self.transform_test(img_data)

        return img_data

    def getClass(self):

        image_names = os.listdir(self.img_path)

        for image_name in image_names:
            print(image_name)
            input_img = self.getInput(self.img_path + "/" + image_name)
            input_img = input_img.unsqueeze(0)
            input_img = Variable(input_img).cuda()

            output = self.Net(input_img)
            output = output.squeeze(0)
            print(self.index_class[int(torch.argmax(output))])
    def getImageInput(self,image):

        img_data = Image.fromarray(image.astype('uint8')).convert('RGB')
        img_data = self.transform_test(img_data)

        return img_data

    def getAbnormalType(self,input):

        input = self.getImageInput(input)
        input = input.unsqueeze(0)
        input = Variable(input).cuda()
        output = self.Net(input)
        output = output.squeeze(0)
        print(self.index_class[int(torch.argmax(output))])

        return int(torch.argmax(output))



if __name__ =="__main__":

    VGG = Vgg()

    img = cv2.imread("./images/102.jpg")

    print(VGG.getAbnormalType(img))