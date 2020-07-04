from __future__ import print_function
from PIL import Image
import os
import os.path
import numpy as np
import sys

if sys.version_info[0] == 2:
    import cPickle as pickle
else:
    import pickle

import torch.utils.data as data


class DataManager(data.Dataset):
    """`
    Args:
        root (string): Root directory of dataset where directory
            ``cifar-10-batches-py`` exists or will be saved to if download is set to True.
        train (bool, optional): If True, creates dataset from training set, otherwise
            creates from test set.
        transform (callable, optional): A function/transform that  takes in an PIL image
            and returns a transformed version. E.g, ``transforms.RandomCrop``
        target_transform (callable, optional): A function/transform that takes in the
            target and transforms it.
        download (bool, optional): If true, downloads the dataset from the internet and
            puts it in root directory. If dataset is already downloaded, it is not
            downloaded again.

    """

    def __init__(self, root="/home/user/code/trainData/crop", train=True,
                 transform=None, target_transform=None
                 ):
        self.root = root
        self.transform = transform
        self.target_transform = target_transform
        self.train = train  # training set or test set
        # self.class_index = {"bucket": 0, "foam": 1, "Litter": 2, "PlasticBag": 3,"Sack":4,"Tyre":5,"car":6}
        # self.class_index = {"car": 0, "person": 1, "other": 2}
        self.class_index = {
            "back": 0,
            "car": 1,
            "exposedTrash": 2,
            "illegalStand":3,
            "person":4,
            "shadow":5,
            "uoDoFacility":6,
            "uoRoad":7
        }
        # now load the picked numpy arrays
        if self.train:
            print("start load train data")
            self.train_data = []
            self.train_labels = []
            # load train image path
            train_path = os.path.join(self.root, "train.txt")
            train_file = open(train_path, "r")
            train_set = [line.strip("\n") for line in train_file]

            for img in train_set:
                img_path = os.path.join(self.root, "train", img)

                # with open(img_path,"rb") as im:
                #      img_data = Image.open(im).convert("RGB")

                # 将label映射到一个向量
                start = 0
                end = img.find("/", start + 1)
                img_label = np.array(self.class_index[img[start:end]])

                self.train_data.append(img_path)
                self.train_labels.append(img_label)
            print("end load train")
            # self.train_data = self.train_data.reshape((50000, 3, 32, 32))
            # self.train_data = self.train_data.transpose((0, 2, 3, 1))  # convert to HWC
        else:
            print("start load test data")
            self.test_data = []
            self.test_labels = []
            # load test data path
            test_path = os.path.join(root, "val.txt")
            test_file = open(test_path, "r")
            test_set = [line.strip("\n") for line in test_file]

            for img in test_set:
                img_path = os.path.join(self.root, "val", img)

                # get label
                start = 0
                end = img.find("/", start + 1)
                img_label = np.array(self.class_index[img[start:end]])

                self.test_data.append(img_path)
                self.test_labels.append(img_label)

            print("end load test data")

    def __getitem__(self, index):
        """
        Args:
            index (int): Index

        Returns:
            tuple: (image, target) where target is index of the target class.
        """
        if self.train:
            img_path, target = self.train_data[index], self.train_labels[index]
            with open(img_path, "rb") as im:
                img = Image.open(im).convert("RGB")

        else:
            img_path, target = self.test_data[index], self.test_labels[index]
            with open(img_path, "rb") as im:
                img = Image.open(im).convert("RGB")

        # doing this so that it is consistent with all other datasets
        # to return a PIL Image
        # img = Image.fromarray(img)

        if self.transform is not None:
            img = self.transform(img)

        if self.target_transform is not None:
            target = self.target_transform(target)

        return img, target

    def __len__(self):
        if self.train:
            return len(self.train_data)
        else:
            return len(self.test_data)


if __name__ == "__main__":
    # train_file = open("../dataroot/train.txt", "r")
    # train_set = [line.strip("\n") for line in train_file]
    # print(train_set)
    class_index = {"bucket": 0, "foam": 1, "Litter": 2, "PlasticBag": 3, "Sack": 4, "Tyre": 5}
    img = "foam/10371.jpg"
    start = 0
    end = img.find("/", start + 1)
    img_label = np.array(class_index[img[start:end]])

    print(img_label)
