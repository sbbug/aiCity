# -*- coding: utf-8 -*-

from __future__ import print_function

import torch
from torchvision.models.resnet import Bottleneck, BasicBlock, ResNet
import torch.utils.model_zoo as model_zoo
import numpy as np
import scipy.misc
import os
from Functions import distance,getProjectContext
import imageio


# configs for histogram
RES_model = 'resnet18'  # model type
pick_layer = 'avg'  # extract feature of this layer
d_type = 'cosine'  # distance type

depth = 3  # retrieved depth, set to None will count the ap for whole database1

use_gpu = torch.cuda.is_available()
means = np.array([103.939, 116.779, 123.68]) / 255.  # mean of three channels in the order of BGR

# cache dir
cache_dir = 'cache'
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

# from https://github.com/pytorch/vision/blob/master/torchvision/models/resnet.py
model_urls = {
    'resnet18': 'https://download.pytorch.org/models/resnet18-5c106cde.pth',
    'resnet152': 'https://download.pytorch.org/models/resnet152-b121ed2d.pth',
}


class ResidualNet(ResNet):
    def __init__(self, model=RES_model, pretrained=True):
        if model == "resnet152":
            super().__init__(Bottleneck, [3, 8, 36, 3], 1000)
            if pretrained:
                self.load_state_dict(model_zoo.load_url(model_urls['resnet152']))
        if model == "resnet18":
            super().__init__(BasicBlock, [2, 2, 2, 2], 1000)
            if pretrained:
                self.load_state_dict(model_zoo.load_url(model_urls['resnet18']))
        elif model == "resnet34":
            super().__init__(BasicBlock, [3, 4, 6, 3], 1000)
            if pretrained:
                self.load_state_dict(model_zoo.load_url(model_urls['resnet34']))

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)  # x after layer4, shape = N * 512 * H/32 * W/32
        max_pool = torch.nn.MaxPool2d((x.size(-2), x.size(-1)), stride=(x.size(-2), x.size(-1)), padding=0,
                                      ceil_mode=False)
        Max = max_pool(x)  # avg.size = N * 512 * 1 * 1
        Max = Max.view(Max.size(0), -1)  # avg.size = N * 512
        avg_pool = torch.nn.AvgPool2d((x.size(-2), x.size(-1)), stride=(x.size(-2), x.size(-1)), padding=0,
                                      ceil_mode=False, count_include_pad=True)
        avg = avg_pool(x)  # avg.size = N * 512 * 1 * 1
        avg = avg.view(avg.size(0), -1)  # avg.size = N * 512
        fc = self.fc(avg)  # fc.size = N * 1000
        output = {
            'max': Max,
            'avg': avg,
            'fc': fc
        }
        return output


class ResNetFeat(object):

    def __init__(self):
        self.res_model = ResidualNet(model=RES_model)
        self.res_model.eval()
        if use_gpu:
            self.res_model = self.res_model.cuda()

    def make_samples(self, db):

        samples = []

        data = db.get_data()
        for d in data.itertuples():
            d_img, d_cls = getattr(d, "img"), getattr(d, "cls")
            img = scipy.imageio.imread(d_img, mode="RGB")
            img = img[:, :, ::-1]  # switch to BGR
            img = np.transpose(img, (2, 0, 1)) / 255.
            img[0] -= means[0]  # reduce B's mean
            img[1] -= means[1]  # reduce G's mean
            img[2] -= means[2]  # reduce R's mean
            img = np.expand_dims(img, axis=0)
            try:
                if use_gpu:
                    inputs = torch.autograd.Variable(torch.from_numpy(img).cuda().float())
                else:
                    inputs = torch.autograd.Variable(torch.from_numpy(img).float())
                d_hist = self.res_model(inputs)[pick_layer]  # pick_layer = avg
                d_hist = d_hist.data.cpu().numpy().flatten()
                d_hist /= np.sum(d_hist)  # normalize
                print()
                samples.append({
                    'img': d_img,
                    'cls': d_cls,
                    'hist': d_hist
                })
            except:
                pass

        return samples

    def make_sample(self, img_path):
        '''
        :param img_path:
        :return:
        '''
        img = imageio.imread(img_path)
        img = img[:, :, ::-1]  # switch to BGR
        img = np.transpose(img, (2, 0, 1)) / 255.
        img[0] -= means[0]  # reduce B's mean
        img[1] -= means[1]  # reduce G's mean
        img[2] -= means[2]  # reduce R's mean
        img = np.expand_dims(img, axis=0)
        try:
            if use_gpu:
                inputs = torch.autograd.Variable(torch.from_numpy(img).cuda().float())
            else:
                inputs = torch.autograd.Variable(torch.from_numpy(img).float())
            d_hist = self.res_model(inputs)[pick_layer]  # pick_layer = avg
            d_hist = d_hist.data.cpu().numpy().flatten()
            d_hist /= np.sum(d_hist)  # normalize
            print()

            return {
                'hist': d_hist
            }
        except:
            pass


if __name__ == "__main__":


    model = ResNetFeat()

    target_img = getProjectContext()+"/Resources/NewCameraTpl/target/tar.jpg"

    target_hist = model.make_sample(target_img)

    db_path = getProjectContext()+"/Resources/NewCameraTpl"

    cls_dir = os.listdir(db_path)

    res = list()

    print("start...")

    for cls in cls_dir:
        cls_path = os.path.join(db_path, cls)

        for img in os.listdir(cls_path):
            img_path = os.path.join(cls_path,img)

            b_hist = model.make_sample(img_path)

            # print(cls,distance(target_hist['hist'], b_hist['hist'], d_type=d_type))

            res.append({
                "cls":cls,
                "dis":distance(target_hist['hist'], b_hist['hist'], d_type=d_type)
            })

    results = sorted(res, key=lambda x: x['dis'])
    top_5 = dict()
    for res in results[:5]:
        if top_5.__contains__(res['cls']):
            top_5[res['cls']]+=1
        else:
            top_5[res['cls']]=1

    print(top_5)
    res = max(top_5, key=lambda k: top_5[k])
    print(res)