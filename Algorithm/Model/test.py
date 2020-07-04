#test.py
#!/usr/bin/env python3

""" test neuron network performace
print top1 and top5 err on test dataset
of a model

author baiyu
"""
import argparse
import torch
from torch.autograd import Variable
import os
from utils import get_network, get_test_dataloader
from PIL import Image
import torchvision.transforms as transforms
import conf.global_settings as config
def getInput(img_path):
    with open(img_path, "rb") as im:
        img_data = Image.open(im).convert("RGB")

    transform_test = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize(config.MANAGER_TRAIN_MEAN, config.MANAGER_TRAIN_STD)
    ])
    img_data = transform_test(img_data)

    return img_data


if __name__ == '__main__':
    index_class = {0:"ExposedTrash", 1:"IllegalStand",2: "UoDofacilities", 3:"UORoads"}
    parser = argparse.ArgumentParser()
    parser.add_argument('-net', type=str, default="vgg16", help='net type')
    parser.add_argument('-weights', type=str,default="./checkpoint/vgg16-123-best.pth", help='the weights file you want to test')
    parser.add_argument('-gpu', type=bool, default=True, help='use gpu or not')
    img_path = "./images"
    args = parser.parse_args()

    net = get_network(args,use_gpu=args.gpu)
    net.load_state_dict(torch.load(args.weights), args.gpu)
    net.eval()

    image_names = os.listdir(img_path)

    for image_name in image_names:

        print(image_name)
        input_img = getInput(img_path+"/"+image_name)
        input_img = input_img.unsqueeze(0)
        input_img = Variable(input_img).cuda()

        output = net(input_img)
        output = output.squeeze(0)
        print(index_class[int(torch.argmax(output))])

    # for n_iter, (image, label) in enumerate(cifar100_test_loader):
    #     print("iteration: {}\ttotal {} iterations".format(n_iter + 1, len(cifar100_test_loader)))
    #     image = Variable(image).cuda()
    #     label = Variable(label).cuda()
    #     output = net(image)
    #     _, pred = output.topk(5, 1, largest=True, sorted=True)
    #
    #     label = label.view(label.size(0), -1).expand_as(pred)
    #     correct = pred.eq(label).float()




