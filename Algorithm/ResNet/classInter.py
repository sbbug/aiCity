from torchvision import datasets, models, transforms
import torch.nn as nn
import torch
import Algorithm.ResNet.resnet50 as resnet50
from PIL import Image
import torch.utils.model_zoo as model_zoo
import numpy as np
from Functions import getProjectContext


class ClassInter(nn.Module):

    def __init__(self, num_classes=6):
        super(ClassInter, self).__init__()

        self.model = resnet50.resnet50(pretrained=False, num_classes=num_classes)

        print("loading resnet model")

        self.model.load_state_dict(torch.load(getProjectContext() + "/Algorithm/ResNet/outputs/resnet50.pth"))

        print("finished resnet model")

        self.device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")

        self.model = self.model.to(self.device)

        self.model.eval()

        self.softmax = nn.Softmax()

        # self.class_index = {"car": 0, "person": 1, "other": 2}
        self.class_index = {
            "back": 0,
            "car": 1,
            "exposedTrash": 2,
            "illegalStand": 3,
            "person": 4,
            "shadow": 5,
            "uoDoFacility": 6,
            "uoRoad": 7
        }
        self.index_class = {
            0: "back",
            1: "car",
            2: "exposedTrash",
            3: "illegalStand",
            4: "person",
            5: "shadow",
            6: "uoDoFacility",
            7: "uoRoad"
        }
        # self.index_class = {0: "car", 1: "person", 2: "other"}

    def forward(self, x):
        x = x.to(self.device)

        return self.model(x)

    def transformType(self, img):
        transform = transforms.Compose([
            transforms.Resize(224),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        return transform(img)

    def getCls(self, img):
        '''
        :param img: numpy type
        :return:
        '''
        img = Image.fromarray(np.uint8(img))

        img = self.transformType(img)

        img = img.unsqueeze(0)

        output = self.forward(img)

        _, preds = torch.max(self.softmax(output), 1)

        cls_idx = preds.item()

        return self.index_class[cls_idx]
