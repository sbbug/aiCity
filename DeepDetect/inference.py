from DeepDetect.Cascade.mmdetection.mmdet.apis import init_detector, inference_detector
import mmcv
import os
import numpy as np

config_file = '/home/user/code/mmdetection/configs/cascade_rcnn/cascade_rcnn_r101_fpn_1x_coco.py'
checkpoint_file = '/home/user/code/mmdetection/work_dirs/cascade_rcnn_r101_fpn_1x_coco/epoch_24.pth'

if __name__ == "__main__":
    # build the model from a config file and a checkpoint file
    model = init_detector(config_file, checkpoint_file, device='cuda:1')

    data_dir = "/home/user/code/cityManager/Resources/ReportedDataset/images"
    detect_res_dir = "/home/user/code/cityManager/Resources/ReportedDataset/detect_test/20200603"
    for img_name in os.listdir(data_dir):

        img_path = os.path.join(data_dir,img_name)
        result = inference_detector(model, img_path)
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
        print(img_name,bboxes,labels)
        # model.show_result(img_path, result, score_thr=0.7,bbox_color='red',text_color='red',thickness=3,out_file=os.path.join(detect_res_dir,img_name))


