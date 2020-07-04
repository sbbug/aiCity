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
import numpy as np
np.set_printoptions(threshold=np.inf)
class VggFeature(object):

    class arg:
        net = "vgg16"
        model_path = getProjectContext()+VGG_MODEL_PATH
        gpu = True

    Net = None
    def __init__(self):
        super(VggFeature, self).__init__()
        VggFeature.loadModel()

        self.index_class = {0: "暴露垃圾", 1: "占道无证经营、跨门营业", 2: "乱设或损坏户外设施", 3: "占道无证经营、跨门营业"}
        self.img_path = "./images"

        self.transform_test = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
            transforms.Normalize(config.MANAGER_TRAIN_MEAN, config.MANAGER_TRAIN_STD)
        ])
        self.extractFeature = self.Net.features


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

    def getFeature(self,input):

        input = self.getImageInput(input)
        input = input.unsqueeze(0)
        input = Variable(input).cuda()
        output = self.extractFeature(input)
        output = output.view(output.size()[0], -1)

        return output

    def normalization(self,data):
        _range = np.max(data) - np.min(data)
        return (data - np.min(data)) / _range


if __name__ =="__main__":

    vggFeature = VggFeature()

    img1 = cv2.imread("./images/000033.jpg")
    img2 = cv2.imread("./images/001122.jpg")

    f1 = vggFeature.getFeature(img1)
    f2 = vggFeature.getFeature(img2)

    f1 = f1.detach().cpu().numpy()
    f2 = f2.detach().cpu().numpy()

    # f1 = normalization(f1[0])
    # f2 = normalization(f2[0])
    res = {}
    res['feature'] = f1[0].tolist()
    file = open("w.txt","w")
    file.write(str(res))
    file.close()

    file = open("w.txt", "r")
    res = file.readline()
    res = eval(res)
    file.close()
    f2 = res['feature']
    print(f1)
    print(f2)

    print("distance",np.sqrt(np.sum(np.square(f1[0]-f2[0]))))