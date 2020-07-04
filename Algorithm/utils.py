# import cv2
# import os
# import numpy as np
# from skimage.feature import hog
# import parameters
#
# # 加载数据集
# def loadData(data_path):
#     '''
#     :param data_path: 图像数据所在目录
#     :return: 返回图像hog特征矩阵 图像标签
#     '''
#     data_label = []
#     data = []
#     file_list = os.listdir(data_path)
#     n = len(file_list)
#     for i in range(n):
#
#         # 获取标签数据
#         data_label.append( [int(file_list[i].split("_")[0])] )
#
#         # 获取图片特征
#         image = cv2.imread(os.path.join(data_path, file_list[i]))
#
#         # 提取hog特征
#         fd = getImageHog(image)
#         # 添加到data列表
#         data.append(fd)
#
#     # 数据类型转换
#     data = np.array(data)
#     data_labels = np.array(data_label)
#
#     return data.astype(np.float32),data_labels.astype(np.float32)
#
# # 获取单张图像的hog特征矩阵
# def loadSingle(image):
#     '''
#     :param image: RGB图像
#     :return: 单张图像矩阵
#     '''
#
#     return np.array([getImageHog(image)]).astype(np.float32)
#
# # 获取图像的hog特征
# def getImageHog(image):
#     '''
#     :param image: 输入目标图像
#     :return: 目标图像的hog特征向量
#     '''
#     resize_w = 128
#     resize_h = 64
#
#     image = cv2.resize(image, (resize_w, resize_h))
#
#     # 获取hog特征
#     fd = hog(image, orientations=9, pixels_per_cell=(4, 4),
#              cells_per_block=(1, 1), visualize=False)
#
#     return fd
#
