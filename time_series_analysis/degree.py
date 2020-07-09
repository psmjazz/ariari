# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
from math import *
import csv

def getAngle(v1x, v1y,v2x, v2y):
    
    if v1x == 0:
        v1x = v1x + 1e-5
    if v2x == 0:
        v2x = v2x + 1e-5
    
    dot = np.dot((v1x,v1y),(v2x,v2y))
    sq1 = sqrt((v1x*v1x)+(v1y*v1y))
    sq2 = sqrt((v2x*v2x)+(v2y*v2y))
    # print(dot, sq1, sq2)
    theta1 = acos( dot / ( sq1 * sq2 ) ) * 180/3.14
    theta2 = acos(np.dot((v1x,v1y),(v2x*-1,v2y*-1))/(sqrt((v1x*v1x)+(v1y*v1y)) * sqrt((v2x*v2x)+(v2y*v2y)))) * 180 /3.14
    print(theta1, theta2)
    if(theta1 > theta2):
        result = theta2
    else:
        result = theta1
    return result

def main():
   f = open('./output/squat_skeleton_10_1.csv', 'r', encoding = 'utf-8')
   rdr = csv.reader(f)
   for line in rdr:
       	if line[0] == '':
       		#print(line[9:15], line[24:30])
       		continue
       	# str로 float으로
       	line = list(map(float, line))
       	rhipx, rkneex, ranklex= line[9:12]
       	rhipy, rkneey, rankley= line[24:27]
       	lhipx, lkneex, lanklex= line[12:15]
       	lhipy, lkneey, lankley= line[27:30]
    
       	# 좌표 중에 0 있으면 걍 건너뜀
       	if rhipx == 0.0 or rkneex == 0.0 or ranklex == 0.0:
       		continue
       	if rhipy == 0.0 or rkneey == 0.0 or rankley == 0.0:
       		continue
       	if lhipx == 0.0 or lkneex == 0.0 or lanklex == 0.0:
       		continue
       	if lhipy == 0.0 or lkneey == 0.0 or lankley == 0.0:
       		continue
       	#print(line)
       	#print(line[9:15], line[24:30])
    
       	right_angle = getAngle(rhipx-rkneex, rhipy-rkneey, ranklex-rkneex, rankley-rkneey)
       	left_angle = getAngle(lhipx-lkneex, lhipy-lkneey, lanklex-lkneex, lankley-lkneey)
       	#print(line)
        print(rhipx, rkneex, ranklex)
        print(rhipy, rkneey, rankley)
       	print("right_angle: " ,right_angle)
       	print("left_angle: " ,left_angle)
       	print("")
   f.close()
   

   

if __name__ == "__main__":
    main()