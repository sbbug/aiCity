import random
from PIL import ImageDraw
from torchvision.transforms import transforms
from Parameters import FPN_MODEL_PATH, ANCHORS, CAM_ANCHORS,CLS_THRESH
from DeepDetect.Cascade.mmdetection.mmdet.apis import init_detector, inference_detector
import cv2
import os
import time
import numpy as np
from Parameters import NEW_LAABEL_TO_OLD_LABEL

class CascadeDetection(object):
    # cascade config
    class CascadeConfig:

        config_file = '/home/user/code/mmdetection/configs/cascade_rcnn/cascade_rcnn_r101_fpn_1x_coco.py'
        checkpoint_file = '/home/user/code/mmdetection/work_dirs/cascade_rcnn_r101_fpn_1x_coco/epoch_17.pth'
        cuda_device = 'cuda:0'
        classes = (
            'luan_dui_wu_liao',
            'bao_lu_la_ji',
            'ling_san_la_ji',
            'kua_men_ying_ye',
            'luan_la_tiao_fu',
            'luan_she_guang_gao_pai',
            'gu_ding_tan_fan',
            'liu_dong_tan_fan',
            'cheng_san_jing_ying',
            'luan_shai_yi_wu'
        )
        score_thr = 0.8

    def __init__(self):
        # cascade model
        self.model = init_detector(self.CascadeConfig.config_file, self.CascadeConfig.checkpoint_file,
                                   device=self.CascadeConfig.cuda_device)

    def getBoxsAndLabels(self, result):
        '''
        :param result:
        :return:
        '''
        if isinstance(result, tuple):
            bbox_result, segm_result = result
            if isinstance(segm_result, tuple):
                segm_result = segm_result[0]  # ms rcnn
        else:
            bbox_result, segm_result = result, None
        bboxes = np.vstack(bbox_result)
        labels = [
            np.full(bbox.shape[0], i, dtype=np.int32)
            for i, bbox in enumerate(bbox_result)
        ]
        labels = np.concatenate(labels)

        return bboxes, labels

    # define a function detect input frame
    def detectAbnormalsBySinlgeScale(self, frame, camID):
        '''
        :param frame: need to te detected
        :return: abnormal set
        '''

        result = inference_detector(self.model, frame)

        bboxes, labels = self.getBoxsAndLabels(result)

        res_info = []
        for bbox, cls in zip(bboxes, labels):

            if bbox[4] < self.CascadeConfig.score_thr:
                continue

            category = self.CascadeConfig.classes[cls]
            category = NEW_LAABEL_TO_OLD_LABEL[category]

            if category=='other':continue

            object = {}
            object['type'] = category
            object['score'] = round(bbox[4], 2)
            # for per class ,they have  a own thresh
            if CLS_THRESH[category]>object['score']:
                continue
            object['x'] = int(bbox[0])
            object['y'] = int(bbox[1])
            object['w'] = int(bbox[2] - bbox[0])
            object['h'] = int(bbox[3] - bbox[1])
            object['cam_id'] = camID
            # print(object)
            res_info.append(object)
            if False:
                # cv2.rectangle(frame, topLeft, bottomRight, (0, 255, 255), 2)
                #
                # cv2.putText(masked, abnormal["type"], topLeft, cv2.FONT_HERSHEY_SIMPLEX, 1,
                #             (0, 255, 255), 2)
                cv2.rectangle(
                    frame,(object['x'], object['y']), (object['x'] + object['w'], object['y'] + object['h']),
                    (0, 255, 255), 2)
                cv2.putText(frame,str(object['type']),(object['x'] + 10, object['y'] + 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                          1.2,(0, 255, 255), 2)
        if False:
            cv2.imshow("res",frame)
            cv2.waitKey(-1)
        return res_info

    # define a function modify the box location
    def modifyBoxLocation(self, anchor_abnormals, anchor):

        for abnormal in anchor_abnormals:
            abnormal['x'] = abnormal['x'] + anchor[0]
            abnormal['y'] = abnormal['y'] + anchor[1]

        return anchor_abnormals

    # define a function that filter the bigger box
    def filterBiggerBox(self, anchor_abnormals):
        temp = []
        for anchor_abnormal in anchor_abnormals:
            if anchor_abnormal['w'] * anchor_abnormal['h'] < 40000:
                temp.append(anchor_abnormal)
        return temp

    # cal box iou
    def calIOU(self, anchor_a, anchor_b):

        x1 = max(anchor_a['x'], anchor_b['x'])
        y1 = max(anchor_a['y'], anchor_b['y'])

        x2 = min(anchor_a['x'] + anchor_a['w'], anchor_b['x'] + anchor_b['w'])
        y2 = min(anchor_a['y'] + anchor_a['h'], anchor_b['y'] + anchor_b['h'])

        w = max(0, x2 - x1)
        h = max(0, y2 - y1)

        inter = w * h

        anchor_a_area = anchor_a['w'] * anchor_a['h']
        anchor_b_area = anchor_b['w'] * anchor_b['h']

        return inter / (anchor_a_area + anchor_b_area - inter)

    # define a function that filter extra box
    def filterExtraBox(self, anchor_anbormals):

        if len(anchor_anbormals) == 0:
            return []

        target_anchors = []
        # sort
        anchor_anbormals.sort(key=lambda anchor: (-anchor['score']))

        while len(anchor_anbormals) != 0:
            # add the highest score to target_anchor
            max_score = anchor_anbormals[0]
            target_anchors.append(max_score)

            temp = []
            for anchor_anbormal in anchor_anbormals:

                if self.calIOU(anchor_anbormal, max_score) < 0.05:
                    temp.append(anchor_anbormal)

            anchor_anbormals = temp
            anchor_anbormals.sort(key=lambda anchor: (-anchor['score']))

        return target_anchors

    # define a function mutil-scale detect
    def detectAbnormalsByMutilScale(self, frame, camID, img_path=""):
        # print(frame.shape,"---------------")
        all_abnormals = []
        temp_frame = frame.copy()
        temp_frame = cv2.cvtColor(temp_frame, cv2.COLOR_BGR2RGB)

        if CAM_ANCHORS.__contains__(camID):

            for anchor in CAM_ANCHORS[camID]:
                roi = frame[anchor[1]:anchor[1] + anchor[3], anchor[0]:anchor[0] + anchor[2], :]
                anchor_abnormals = self.detectAbnormalsBySinlgeScale(roi, camID)
                # modify location
                anchor_abnormals = self.modifyBoxLocation(anchor_abnormals, anchor)
                for anchor_abnormal in anchor_abnormals:
                    anchor_abnormal['cam_id'] = camID
                    # add time field       revised by Hongwei Sun 20191212
                    anchor_abnormal['time'] = int(time.time())
                    all_abnormals.append(anchor_abnormal)
        else:  # http camera
            anchor_abnormals = self.detectAbnormalsBySinlgeScale(frame, camID)
            # modify location
            anchor_abnormals = self.modifyBoxLocation(anchor_abnormals, [0, 0, 1920, 1080])
            for anchor_abnormal in anchor_abnormals:
                anchor_abnormal['cam_id'] = camID
                # add time field       revised by Hongwei Sun 20191212
                anchor_abnormal['time'] = int(time.time())
                all_abnormals.append(anchor_abnormal)

        # filter bigger box
        all_abnormals = self.filterBiggerBox(all_abnormals)
        # nms
        all_abnormals = self.filterExtraBox(all_abnormals)

        if img_path != "":
            temp_frame = transforms.Image.fromarray(temp_frame)
            draw = ImageDraw.Draw(temp_frame)
            for anbormal in all_abnormals:
                color = random.choice(['red', 'green', 'blue', 'yellow', 'purple', 'white'])
                draw.rectangle(
                    ((anbormal['x'], anbormal['y']), (anbormal['x'] + anbormal['w'], anbormal['y'] + anbormal['h'])),
                    outline=color, width=4)
                draw.text((anbormal['x'] + 10, anbormal['y'] + 10),
                          text=f'{anbormal["type"]:s} {anbormal["score"]:.3f}', fill=color)

            if img_path != "":
                save_image_path = img_path + "_det.jpg"
                temp_frame.save(save_image_path)
                print(f'Output image is saved to {save_image_path}')

        return all_abnormals

    # single-scale detect
    def detectAbnormals(self, frame, camID, img_path=""):
        '''
        :param frame: type numpy
        :param camID: camid
        :return:
        '''
        if frame is None or camID is None:
            return []

        abnormals = self.detectAbnormalsBySinlgeScale(frame, camID)
        abnormals = self.filterBiggerBox(abnormals)
        # debug
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = transforms.Image.fromarray(frame)
        draw = ImageDraw.Draw(image)

        if img_path != "":
            for abnormal in abnormals:
                color = random.choice(['red', 'green', 'blue', 'yellow', 'purple', 'white'])
                draw.rectangle(
                    ((abnormal['x'], abnormal['y']), (abnormal['x'] + abnormal['w'], abnormal['y'] + abnormal['h'])),
                    outline=color, width=4)
                draw.text((abnormal['x'] + 10, abnormal['y'] + 10),
                          text=f'{abnormal["type"]:s} {abnormal["score"]:.3f}',
                          fill=color)
            save_image_path = img_path + "_det.jpg"
            image.save(save_image_path)
            print(f'Output image is saved to {save_image_path}')

        return abnormals


if __name__ == '__main__':

    model = CascadeDetection()

    data_dir = "/home/user/code/cityManager/Resources/ReportedDataset/images"
    detect_res_dir = "/home/user/code/cityManager/Resources/ReportedDataset/detect_test/20200603"
    for img_name in os.listdir(data_dir):
        img_path = os.path.join(data_dir, img_name)
        im_data = cv2.imread(img_path)
        im_data = cv2.resize(im_data,(1280,720))
        model.detectAbnormalsBySinlgeScale(im_data,"123")
