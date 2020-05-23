# -*- coding: utf-8 -*-
"""
Created on Fri May  8 13:38:07 2020

@author: geobo
"""

import os
from scipy import io
import numpy as np
import cv2
from matplotlib import pyplot as plt
import pandas as pd
import csv

# from IPython.core.display import display, HTML

class Cutter:
    def __init__(self, modelType = 'MPII'):
        self.modelType = modelType
        
        if(self.modelType == 'MPII'):
            self.mpii_key  = {'Head' : 0, 'Neck' : 1, 'Right Shoulder' : 2,
                               'Right Elbow':3, 'Right Wrist':4, 
                               'Left Shoulder' : 5, 'Left Elbow' : 6, 'Left Wrist' : 7,
                               'Right Hip' : 8, 'Right Knee':9, 'Right Ankle' : 10, 
                               'Left Hip' : 11, 'Left Knee':12, 'Left Ankle' : 13,
                               'Chest' : 14}
        
    def load_csv(self, path, nan_handling = 'previous_value'):
        self.path = path
        # with open(path, newline = '') as f:
        #     sekeltons = csv.reader(f, )
        self.df = pd.read_csv(path)
        # head = np.array(df['Head']).astype('float32')
        # head = [str(x)[1:-1].split(', ') for x in df['Head']]
        x = []
        y = []
        self.coordinate = dict()
        
        if(nan_handling == 'previous_value'):        
            prev_x = 0
            prev_y = 0
            
            for key, val in self.mpii_key.items():
                kps = self.df[key]
                tmp_x = []
                tmp_y = []
                prev_x = 0
                prev_y = 0
                for kp in kps:
                    if kp != kp:
                        tmp_x.append(prev_x)
                        tmp_y.append(prev_y)
                    else:
                        tmp = list(map(float, kp[1:-1].split(', ')))
                        tmp_x.append(tmp[0])
                        tmp_y.append(tmp[1])
                        prev_x = tmp[0]
                        prev_y = tmp[1]
                x.append(tmp_x); y.append(tmp_y)
        
        # self.x = np.array(self.x)
        # self.y = np.array(self.y)
        self.coordinate['x'] = np.array(x)
        self.coordinate['y'] = np.array(y)
        # 구현 필요 csv 파일 형식에 따라 np.array로
    
    def plot(self, keypoint_list, plot_coordinate):
        for keypoint in keypoint_list:
            plot_kp = self.coordinate[plot_coordinate][self.mpii_key[keypoint]]
            plt.plot(plot_kp, label = keypoint)
            plt.legend()
        plt.show()
    
    def find_cut_frame(self, keypoint_list, beta = 0.7, 
                       feature = 'y', flag = 'up', 
                       plot = False, x_plot_range = None, y_plot_range = None):
        interested = np.zeros(self.coordinate[feature].shape[1])
        for kp in keypoint_list:
            interested += self.coordinate[feature][self.mpii_key[kp]]
        interested /= len(keypoint_list)
        total_avg = np.average(interested)
        
        feature_maxima = []
        feature_minima = []
        prev = 0
        
        weighted_avg = [0]
        for t in range(1, interested.shape[0]):
            curr = beta * weighted_avg[-1] + (1 - beta) * interested[t]
            weighted_avg.append(curr)
            # 극점찾기
            if flag == 'up' and prev > curr and total_avg < prev:
                feature_maxima.append(t-1)
                flag = 'down'
            elif flag == 'down' and prev < curr and total_avg > prev:
                feature_minima.append(t-1)
                flag = 'up'
            elif flag == 'up' and prev > curr:
                flag = 'down'
            elif flag == 'down' and prev < curr:
                flag = 'up'
            prev = curr
        
        # 지수 가중 평균
        for t in range(1, interested.shape[0]):
            weighted_avg[t] = weighted_avg[t] / (1 - beta**t)
            
        # 예측 지점 최적화
        feature_maxima, feature_minima = self.retudction(feature_maxima, feature_minima)
        
        if(plot):
            plt.plot(interested, label = 'interested')
            plt.plot(weighted_avg[1:], label = 'weighted')
            plt.legend()
            for maxi in feature_maxima:
                plt.axvline(x =maxi, color = 'red')
            for mini in feature_minima:
                plt.axvline(x = mini, color = 'green')
            if x_plot_range != None:
                plt.xlim(x_plot_range)
            if y_plot_range != None:
                plt.ylim(y_plot_range)
                
            plt.show()
        
        return feature_maxima, feature_minima
    
    def retudction(self, listA, listB):
        posA = 0
        posB = 0
        resultA =[]
        resultB =[]
        while posA < len(listA) and posB < len(listB):

            if listA[posA] < listB[posB]:
                posEnd = posA
                while listA[posEnd] < listB[posB]:
                    posEnd+=1
                    if posEnd >= len(listA):
                        break
                resultA.append(int(np.average(listA[posA: posEnd])))
                posA = posEnd

            else:
                posEnd = posB
                while listA[posA] >= listB[posEnd]:
                    posEnd+=1
                    if posEnd >= len(listB):
                        break
                resultB.append(int(np.average(listB[posB:posEnd])))
                posB = posEnd
        
        # 남은 한쪽 처리
        if posA < len(listA):
            resultA.append(int(np.average(listA[posA:])))
        else:
            resultB.append(int(np.average(listB[posB:])))
        return resultA, resultB
    
    def cut(self, feature_maxima, feature_minima, subject_name, cutting = 'feature_minima'):
        
        x = self.coordinate['x'].T
        y = self.coordinate['y'].T
        if self.modelType == 'MPII':
            column_of_x = [f'{part} x' for part in self.mpii_key.keys()]
            column_of_y = [f'{part} y' for part in self.mpii_key.keys()]

        if cutting == 'feature_minima':
            feature_minima.insert(0,0)
            feature_minima.append(len(self.df))
            check_pos = 0 # feature_maxima가 끊고자 하는 구간 사이에 있는지 확인
            for i in range(1, len(feature_minima)):
                if (feature_minima[i-1] < feature_maxima[check_pos] 
                    and feature_minima[i] > feature_maxima[check_pos]):
                    splited_x = x[feature_minima[i-1]: feature_minima[i]]
                    splited_y = y[feature_minima[i-1]: feature_minima[i]]
                    splited_xy = np.concatenate((splited_x, splited_y), axis = 1)
                    splited_df = pd.DataFrame(splited_xy, columns = column_of_x + column_of_y)
                    check_pos+=1
                    splited_df.to_csv(f'{subject_name}_{check_pos}.csv')
                    
                if(check_pos >= len(feature_maxima)):
                    break

        elif cutting == 'feature_maxima':
            feature_maxima.insert(0,0)
            feature_maxima.append(len(self.df))
            check_pos = 0
            for i in range(1, len(feature_maxima)):
                if (feature_maxima[i-1] < feature_minima[check_pos]
                    and feature_maxima[i] > feature_minima[check_pos]):
                    splited_x = x[feature_minima[i-1]: feature_minima[i]]
                    splited_y = y[feature_minima[i-1]: feature_minima[i]]
                    splited_xy = np.concatenate((splited_x, splited_y), axis = 1)
                    splited_df = pd.DataFrame(splited_xy, columns = column_of_x + column_of_y)
                    check_pos+=1
                    splited_df.to_csv(f'{subject_name}_{check_pos}.csv')
                    
                if(check_pos >= len(feature_minima)):
                    break

# directory = os.getcwd()
if __name__ == '__main__':
    cutter = Cutter()
    
    for i in range(15, 19):
        file_name = f'input/squat_skeleton_{i}.csv'
        output_prefix = f'output/squat_skeleton_{i}'
        cutter.load_csv(file_name)
        fmax, fmin = cutter.find_cut_frame(['Right Hip', 'Left Hip'], flag = 'up',  plot =True)
        cutter.cut(fmax, fmin, output_prefix)
        while True:
            ok = input('cut? : ')
            if ok == 'y' or ok == 'Y':
                cutter.cut(fmax, fmin, output_prefix)
                break
            elif ok == 'n' or ok == 'N':
                break
            else:
                continue
        
    # file_name = 'input/squat_skeleton_2.csv'
    # output_prefix = 'output/squat_skeleton_2'
    # cutter.load_csv(file_name)
    # # cutter.plot(['Right Hip', 'Left Hip'], 'y')
    # fmax, fmin = cutter.find_cut_frame(['Right Hip', 'Left Hip'], flag = 'up',  beta = 0.9, plot =True)
    # print(fmax, fmin)
    
    # cutter.cut(fmax[:2], fmin[:3], output_prefix)