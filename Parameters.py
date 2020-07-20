'''
项目中需要用到的常量定义
'''
CAMERAS_CONFIG = "Resources/Config/detectCamera.json"
NEW_CAMERAS_CONFIG = "Resources/Config/newDetectCamera.json"
DETECT_CAMERAS_CONFIG = "Resources/Config/detectCamera_test.json"
# DETECT_CAMERAS_CONFIG= "Resources/Config/detectCamera.json"
IMAGE_CONFIG = "Resources/Config/"
IMAGE_CONFIG_TPL = "Resources/Config/camera_tpl.json"
IMAGE_TEMPLATE = "Resources/ImageTemplate/"
CAMERA_LOG = "Resources/ReportLog/FakeAbnormal/"
CAMERA_REPORTED = "Resources/ReportLog/ReportedAbnormal/"
CACHE = "Resources/Cache/"
ERROR_LOG = "Resources/ErrorLog/error.log"
# 对方系统服务器ip地址
SERVER_IP = "139.226.172.145"

REPORTED_DATASET_PATH = "Resources/ReportedDataset/images"

LOG_REFRESH_FRE = 1800

abnormalMinTimeThreshold = 60  # the abnormal exists for about 10min ,then reported
debug = True
# 定义模板更细参数，当异常区域与图像重叠区域大于这个值时更新
TPL_UPDATE_TURE_THREOLD = 0.45

TPL_UPDATE_FALSE_THREOLD = 0.35

#
DIFF_REGION_NUM = 8
# 帧差算法时最小轮廓面积
MIN_ABNORMAL_AREA_THRESHOLD = 1500
# 当前检测到的真异常与已经重复上报的异常重叠区域阈值
REPORT_IOU_REPORTED_THRESHOLD = 0.5  # 0.2
TRAIN_DIR = "Algorithm/dataset/train/"
TEST_DIR = "Algorithm/dataset/test/"

LABELS = ["", "暴露垃圾", "", "乱设或损坏户外设施", "擅自占用道路堆物、施工"]
VGG_LABELS = {0: "ExposedTrash", 1: "IllegalStand", 2: "UoDofacilities", 3: "UORoads"}

# the url of  getting feedback
FEEDBACK_URL = "http://aicity.hualinfo.com:7902/video/event/feedback"

# 获取事件列表的url
EVENT_URL = "http://aicity.hualinfo.com:7902/video/event/category"

# EVENT_URL = "http://frp.uqaigth.top/video/event/category"

# 添加事件列表
ADD_EVENT_URL = "http://aicity.hualinfo.com:7902/video/event/problem"
# ADD_EVENT_URL = "http://frp.uqaigth.top/video/event/problem"

# 图像上传接口
UPLOAD_IMG_URL = "http://aicity.hualinfo.com:7905/file/video/upload/image"

# 摄像头录入接口
ADD_CAMERA_URL = "http://aicity.hualinfo.com:7902/video/camera"
# ADD_CAMERA_URL = "http://frp.uqaigth.top/video/camera"

# 2019-07-3
VGG_MODEL_PATH = "Algorithm/Model/checkpoint/vgg16-160-regular.pth"

FPN_MODEL_PATH = "DeepDetect/FPN/outputs/fineTune/20190907/model-50000.pth"

# abnormal box area threshold
AREA_THRESHOLD = 200 * 200
# ANCHORS=[[0, 0, 320, 180], [0, 180, 320, 180], [0, 360, 320, 180], [0, 540, 320, 180], [320, 0, 320, 180], [320, 180, 320, 180], [320, 360, 320, 180], [320, 540, 320, 180], [640, 0, 320, 180], [640, 180, 320, 180], [640, 360, 320, 180], [640, 540, 320, 180], [960, 0, 320, 180], [960, 180, 320, 180], [960, 360, 320, 180], [960, 540, 320, 180]]
ANCHORS = [[480, 470, 320, 450], [0, 0, 640, 600], [640, 0, 640, 600], [320, 300, 640, 600],
           [320, 300, 640, 600], [320, 0, 640, 600], [0, 300, 640, 600], [640, 300, 640, 600],
           [160, 150, 320, 300], [480, 150, 320, 300], [740, 150, 320, 300], [160, 450, 320, 300],
           [480, 450, 320, 300], [740, 450, 320, 300], [1267, 466, 209, 244], [1060, 200, 220, 160],
           [934, 154, 324, 295], [700, 680, 500, 400], [400, 90, 312, 150], [531, 204, 178, 132], [223, 138, 387, 322],
           ]

# ANCHORS = [[0,0,1280,720]]
START_TIME = "07:00"
END_TIME = "18:00"

NETWORK = True

FALSE_ABNORMAL_PATH = "Resources/ReportLog/FalseAbnormal"

WINDOW_QSS = "UI/resources/css/theme.qss"

# cameras needed to be detected
# #[5,6,8,26,27,28,29,30,11,24]
DETECT_CAMERAS = [
    "camera_5",
    # "camera_6",
    "camera_8",
    "camera_12",
    "camera_26",
    "camera_27",
    "camera_28",
    "camera_29",
    "camera_30",
    "camera_11",
    "camera_24"

]
# DETECT_CAMERAS = [
#                     "camera_30",
#                     "camera_29"
#                  ]
SHOW_REPORTED_ABNORMAL = False
OUTPUT_LOG = "Resources/Log"
# target_camera = [5,6,8,26,27,28,29,30,11,24] # targetting cameras needed to detected

CAM_ANCHORS = {
    # "camera_5":[[20, 362, 237, 144], [5, 474, 306, 163], [16, 564, 365, 150], [846, 309, 244, 116], [900, 351, 329, 128], [895, 274, 362, 221], [163, 385, 223, 293]],
    # "camera_5":[[249, 423, 215, 294], [25, 360, 295, 354], [627, 374, 216, 72], [827, 438, 340, 134]],
    "camera_5": [[0, 0, 1280, 720]],
    # "camera_6":[[0,0,1280,720]],
    # "camera_8":[[232, 186, 230, 178], [89, 245, 375, 277], [13, 391, 284, 312]],
    "camera_8": [[0, 0, 1280, 720]],
    "camera_12": [[0, 0, 1280, 720]],
    # "camera_26":[[6, 349, 266, 261], [24, 256, 437, 191], [306, 204, 412, 159], [1036, 184, 166, 214], [975, 408, 288, 230], [981, 314, 263, 189]],
    "camera_26": [[0, 0, 1280, 720]],
    # "camera_26":[[900, 167, 230, 538]],
    "camera_27": [[0, 0, 1280, 720]],
    "camera_28": [[0, 0, 1280, 720]],
    # "camera_28":[[628, 207, 207, 198], [932, 291, 160, 171]],
    # "camera_29":[[629, 72, 245, 202], [701, 131, 229, 197], [830, 31, 240, 208], [514, 84, 251, 174], [585, 7, 297, 193],[159, 246, 253, 203], [354, 308, 406, 202], [347, 49, 313, 218], [431, 171, 318, 210], [609, 17, 381, 280], [655, 217, 354, 258], [931, 126, 313, 291], [690, 414, 271, 213], [915, 378, 301, 208]],
    "camera_29": [[0, 0, 1280, 720]],
    # "camera_30":[[205, 437, 115, 123], [174, 419, 130, 106],[257, 463, 147, 161], [200, 413, 117, 129], [138, 367, 126, 149], [168, 489, 160, 123],[104, 354, 168, 138], [174, 411, 209, 177],[39, 321, 180, 122], [137, 381, 206, 151], [223, 446, 287, 187], [244, 598, 239, 113], [42, 404, 222, 222], [11, 571, 295, 93], [11, 231, 77, 340]],
    "camera_30": [[0, 0, 1280, 720]],
    # "camera_11":[[716, 551, 121, 163]],
    "camera_11": [[0, 0, 1280, 720]],
    # "camera_24":[[9, 219, 193, 155], [141, 212, 239, 182], [680, 256, 330, 197], [816, 256, 317, 220], [988, 252, 279, 238], [368, 293, 318, 172]]
    "camera_24": [[0, 0, 1280, 720]],
    "camera_51": [[0, 0, 1280, 720]]
}

# the class of process
DATA = {
    7: '暴露垃圾',
    8: '废弃车辆',
    9: '乱设或损坏户外设施',
    10: '擅自占用道路堆物、施工',
    11: '架空线',
    12: '占道无证经营、跨门营业',
    14: '道路破损',
    16: '跨门营业',
    17: '机动车、非机动车乱停放',
    18: '毁绿占绿',
    19: '其他（仔细描述该问题，上传清晰准确的图片，及时和平台信息员沟通）'
}

HTTP_CAMERAS = [

    '516c070a92fb4a48a151c63d0323201b',
    'd639bee04e534be99623cf411afd4073',
    '43b6b986841d4295aa5ac8396c4db7b5',
    'ed3e2688852844359af981217f2e9342',
    '17e137dfb81b40bcb20fecdf17dcce9e',
    'f2a12d10362944f4bebb7294a1d1f14b',
    'baa0f29d69e1418ea14041f25144f8ae',
    '811549517d6f44e69e01b33201805c40',
    'ed1d5be49cc6401dacac12194c436c16',
    '4d4a75ca0a4e4f19ab1c644493c48440',
    'a3432a0debdb46468f68dcae074e5a72',
    '92bd2c9a830745788ada1592ef04a8e4',
    '907bf08e4b9b4a2e9f5c8234c04e472a',
    '8eda7cc53aaf4099b5caf329cf99a3e7',
    '120dd0641f4948c084c5e322aab5d294',
    'c5a35c2150e3449f89de768b5cd48c90',
    'c1ffdb2fa1b54fa6b7239b9cef2cc76f',
    '9239ce924217427f918fcc7b27ca4e40',
    'c3901115284f408ea13abda093076f4a',
    '93010fb1a9cf40138b13783a46a6c6b0',
    'aa16eb3f92e6482ab86982fe84a3ebef',
    '59fdf03427c344979186938a8d10d500',
    'ab9f4812ab2446f0b856ab716015a377',
    'ba8d8a7a20a64abbb0699664f1f118f4',

]
HTTP_CAMERAS_SPECIAL_TASK = {
    '516c070a92fb4a48a151c63d0323201b_1': [],
    '516c070a92fb4a48a151c63d0323201b_2': [],
    '516c070a92fb4a48a151c63d0323201b_3': [],

    'd639bee04e534be99623cf411afd4073_1': [],
    'd639bee04e534be99623cf411afd4073_2': [],
    'd639bee04e534be99623cf411afd4073_3': [],
    'd639bee04e534be99623cf411afd4073_4': [],

    '43b6b986841d4295aa5ac8396c4db7b5_1': [],
    '43b6b986841d4295aa5ac8396c4db7b5_2': [],

    'ed3e2688852844359af981217f2e9342_1': [],
    'ed3e2688852844359af981217f2e9342_2': [],
    'ed3e2688852844359af981217f2e9342_3': [],

    '17e137dfb81b40bcb20fecdf17dcce9e_1': [],
    '17e137dfb81b40bcb20fecdf17dcce9e_2': [],
    '17e137dfb81b40bcb20fecdf17dcce9e_3': [],
    '17e137dfb81b40bcb20fecdf17dcce9e_4': [],

    'f2a12d10362944f4bebb7294a1d1f14b_1': [],
    'f2a12d10362944f4bebb7294a1d1f14b_2': [],
    'f2a12d10362944f4bebb7294a1d1f14b_3': [],

    'baa0f29d69e1418ea14041f25144f8ae_1': [],
    'baa0f29d69e1418ea14041f25144f8ae_2': [],
    'baa0f29d69e1418ea14041f25144f8ae_3': [],

    '811549517d6f44e69e01b33201805c40_1': [],
    '811549517d6f44e69e01b33201805c40_2': [],
    '811549517d6f44e69e01b33201805c40_3': [],

    'ed1d5be49cc6401dacac12194c436c16_1': [],
    'ed1d5be49cc6401dacac12194c436c16_2': [],
    'ed1d5be49cc6401dacac12194c436c16_3': [],

    '4d4a75ca0a4e4f19ab1c644493c48440_1': [],
    '4d4a75ca0a4e4f19ab1c644493c48440_2': [],
    '4d4a75ca0a4e4f19ab1c644493c48440_3': [],

    'a3432a0debdb46468f68dcae074e5a72_1': [],
    'a3432a0debdb46468f68dcae074e5a72_2': [],
    'a3432a0debdb46468f68dcae074e5a72_3': [],

    '92bd2c9a830745788ada1592ef04a8e4_1': [],
    '92bd2c9a830745788ada1592ef04a8e4_2': [],
    '92bd2c9a830745788ada1592ef04a8e4_3': [],
    '92bd2c9a830745788ada1592ef04a8e4_4': [],

    '907bf08e4b9b4a2e9f5c8234c04e472a_1': [],
    '907bf08e4b9b4a2e9f5c8234c04e472a_2': [],
    '907bf08e4b9b4a2e9f5c8234c04e472a_3': [],

    '8eda7cc53aaf4099b5caf329cf99a3e7_1': [],
    '8eda7cc53aaf4099b5caf329cf99a3e7_2': [],
    '8eda7cc53aaf4099b5caf329cf99a3e7_3': [],

    '120dd0641f4948c084c5e322aab5d294_1': [],
    '120dd0641f4948c084c5e322aab5d294_2': [],
    '120dd0641f4948c084c5e322aab5d294_3': [],
    '120dd0641f4948c084c5e322aab5d294_4': [],

    'c5a35c2150e3449f89de768b5cd48c90_1': [],
    'c5a35c2150e3449f89de768b5cd48c90_2': [],
    'c5a35c2150e3449f89de768b5cd48c90_3': [],

    'c1ffdb2fa1b54fa6b7239b9cef2cc76f_1': [],
    'c1ffdb2fa1b54fa6b7239b9cef2cc76f_2': [],
    'c1ffdb2fa1b54fa6b7239b9cef2cc76f_3': [],

    '9239ce924217427f918fcc7b27ca4e40_1': [],
    '9239ce924217427f918fcc7b27ca4e40_2': [],
    '9239ce924217427f918fcc7b27ca4e40_3': [],

    'c3901115284f408ea13abda093076f4a_1': [],
    'c3901115284f408ea13abda093076f4a_2': [],
    'c3901115284f408ea13abda093076f4a_3': [],

    '93010fb1a9cf40138b13783a46a6c6b0_1': [],
    '93010fb1a9cf40138b13783a46a6c6b0_2': [],
    '93010fb1a9cf40138b13783a46a6c6b0_3': [],

    'aa16eb3f92e6482ab86982fe84a3ebef_1': [],
    'aa16eb3f92e6482ab86982fe84a3ebef_2': [],
    'aa16eb3f92e6482ab86982fe84a3ebef_3': [],

    '59fdf03427c344979186938a8d10d500_1': [],
    '59fdf03427c344979186938a8d10d500_2': [],
    '59fdf03427c344979186938a8d10d500_3': [],

    'ab9f4812ab2446f0b856ab716015a377_1': [],
    'ab9f4812ab2446f0b856ab716015a377_2': [],
    'ab9f4812ab2446f0b856ab716015a377_3': [],

    'ba8d8a7a20a64abbb0699664f1f118f4_1': [],
    'ba8d8a7a20a64abbb0699664f1f118f4_2': [],
    'ba8d8a7a20a64abbb0699664f1f118f4_3': []
}
# 'ExposedTrash': 1, 'UoDOFacilities': 2, 'IllegalStand':
NEW_LAABEL_TO_OLD_LABEL = {
    'bao_lu_la_ji': 'ExposedTrash',
    'luan_dui_wu_liao': 'UORoads',
    'luan_she_guang_gao_pai': 'UoDOFacilities',
    'gu_ding_tan_fan': 'IllegalStand',
    'luan_shai_yi_wu': 'other',
    'liu_dong_tan_fan': 'IllegalStand',
    'ling_san_la_ji': 'other',
    'luan_la_tiao_fu': 'UoDOFacilities',
    'kua_men_ying_ye': 'other',
    'cheng_san_jing_ying': 'IllegalStand'
}

NEED_MASKED = [
    'c3901115284f408ea13abda093076f4a_3',
    'ba8d8a7a20a64abbb0699664f1f118f4_2'
]

# per class thresh_score
CLS_THRESH = {
    "ExposedTrash": 0.90,
    "UoDOFacilities": 0.8,
    "IllegalStand": 0.93,
    "UORoads": 0.8
}

if __name__ == "__main__":
    # print(VGGLABELS[0])
    pass
