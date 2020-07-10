import numpy as np


# import cv2
# from matplotlib import pyplot as plt

# import pandas as pd

class FrameCutter:
    def __init__(self, keypoint_list, modelType='MPII', num_action=3, min_score=0.5, partial_min_score=0.5,
                 beta=0.7, feature='y', mask=5, threshold=10, error=70):
        self.modelType = modelType

        if (self.modelType == 'MPII'):
            self.mpii_key = {'Head': 0, 'Neck': 1, 'Right Shoulder': 2,
                             'Right Elbow': 3, 'Right Wrist': 4,
                             'Left Shoulder': 5, 'Left Elbow': 6, 'Left Wrist': 7,
                             'Right Hip': 8, 'Right Knee': 9, 'Right Ankle': 10,
                             'Left Hip': 11, 'Left Knee': 12, 'Left Ankle': 13,
                             'Chest': 14}
        self.posenet_key = {"nose": 0, "leftEye": 1, "righteye": 2,
                            "leftEar": 3, "rightEar": 4, "leftShoulder": 5,
                            "rightShoulder": 6, "leftElbow": 7, "rightElbow": 8,
                            "leftWrist": 9, "rightWrist": 10, "leftHip": 11,
                            "rightHip": 12, "leftKnee": 13, "rightKnee": 14,
                            "leftAnkle": 15, "rightAnkle": 16}
        self.posenet2mpii = {'nose': 'Head', 'leftEye': 'Head', 'righteye': 'Head',
                             'leftEar': 'Head', 'rightEar': 'Head', 'leftShoulder': 'Left Shoulder',
                             'rightShoulder': 'Right Shoulder', 'leftElbow': 'Left Elbow',
                             'rightElbow': 'Right Elbow', 'leftWrist': 'Left Wrist', 'rightWrist': 'Right Wrist',
                             'leftHip': 'Left Hip', 'rightHip': 'Right Hip', 'leftKnee': 'Left Knee',
                             'rightKnee': 'Right Knee', 'leftAnkle': 'Left Ankle', 'rightAnkle': 'Right Ankle'}

        self.num_action = num_action  # 운동의 구분동작

        self.min_score = min_score  # 키포인트 전체 정확도
        self.partial_min_score = partial_min_score  # 키포인트 하나의 정확도
        self.frame = []  # need_init
        self.keypoint_list = keypoint_list
        self.feature = feature
        self.beta = beta

        self.tape = {'value': [], 'gradient': []}  # need_init
        self.mask = mask
        self.threshold = threshold
        self.features = []  # need_init

        self.prev = 0  # need_init
        self.prev_corr = 0
        self.time = 1  # need_init
        self.error = error

    def add_frame(self, frame_json):
        # 전체 키포인트의 정확도가 min_score보다 작으면 넘긴다.
        if frame_json['score'] < self.min_score:
            return

        # 관심 부위들의 평균을 사용
        interested = 0
        for kp in self.keypoint_list:
            if frame_json['keypoints'][self.posenet_key[kp]]['score'] < self.partial_min_score:
                return
            interested += frame_json['keypoints'][self.posenet_key[kp]]['position'][self.feature]
        interested /= len(self.keypoint_list)
        self.frame.append(frame_json)  # 프레임 추가

        # 지수 가중 평균
        curr = self.beta * self.prev + (1 - self.beta) * interested
        # 편향 보정
        curr_corr = curr / (1 - self.beta ** self.time)
        if (self.time > 1):
            self.tape['gradient'].append(curr_corr - self.prev_corr)
            self.tape['value'].append(curr_corr)
        else:
            self.features.append(curr_corr)
        self.prev = curr
        self.prev_corr = curr_corr
        self.time += 1

    def check_rep(self):
        if (len(self.tape['gradient']) < self.mask):
            return False
        if (abs(sum(self.tape['gradient'][-self.mask:])) < self.threshold
                and abs(self.features[-1] - self.tape['value'][-1]) > self.error):
            print(self.tape['gradient'][-self.mask:], abs(sum(self.tape['gradient'][-self.mask:])))
            self.features.append(self.tape['value'][-1])
        if (len(self.features) < self.num_action):
            return False
        else:
            return True

    def initialize(self):
        self.frame = []

        self.tape['value'] = []
        self.tape['gradient'] = []
        self.features = []

        self.prev = 0
        self.time = 1

    # def save_csv(self, path):

    #     df = pd.DataFrame(columns = self.keypoint_list)
    #     for i, data in enumerate(self.frame):
    #         new_data = []
    #         for kp in self.keypoint_list:
    #             new_data.append(data['keypoints'][self.posenet_key[kp]]['position'][self.feature])
    #         df.loc[i] = new_data
    #     df.to_csv(path)

    def get_frames(self):
        return self.frame