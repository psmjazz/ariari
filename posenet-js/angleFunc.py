from math import *
import numpy as np
import csv

def getAngle(v1x, v1y,v2x, v2y):
   if v1x == 0:
      v1x = v1x + 1e-5
   if v2x == 0:
      v2x = v2x + 1e-5
   theta1 = acos(np.dot((v1x,v1y),(v2x,v2y))/(sqrt((v1x*v1x)+(v1y*v1y)) * sqrt((v2x*v2x)+(v2y*v2y))))
   # theta2 = acos(np.dot((v1x,v1y),(v2x*-1,v2y*-1))/(sqrt((v1x*v1x)+(v1y*v1y)) * sqrt((v2x*v2x)+(v2y*v2y))))
   # if(theta1 > theta2):
   #  result = theta2
   # else:
   #  result = theta1
   return theta1

def getElbowAngle(v1x, v1y,v2x, v2y):
   return getAngle(v1x, v1y,v2x, v2y)

def getKneeAngle(v1x, v1y,v2x, v2y):
   return getAngle(v1x, v1y,v2x, v2y)

def getNeckAngle(v1x, v1y,v2x, v2y):
   return getAngle(v1x, v1y,v2x, v2y)
 

def main():
   f = open('/Users/parkyoungin/ariari/time_series_analysis/output/squat_skeleton_10_1.csv', 'r', encoding = 'utf-8')
   rdr = csv.reader(f)
   for line in rdr:
      if line[0] == '':
         continue
      # str로 float으로
      line = list(map(float, line))
      Head_x, Neck_x, rShoulder_x, rElbow_x, rWrist_x = line[1:6]
      Head_y, Neck_y, rShoulder_y, rElbow_y, rWrist_y = line[16:21]
      lShoulder_x, lElbow_x, lWrist_x = line[6:9]
      lShoulder_y, lElbow_y, lWrist_y = line[21:24]
      rhip_x, rknee_x, rankle_x= line[9:12]
      rhip_y, rknee_y, rankle_y= line[24:27]
      lhip_x, lknee_x, lankle_x= line[12:15]
      lhip_y, lknee_y, lankle_y= line[27:30]

      # 좌표 중에 0 있으면 걍 건너뜀
      if rhip_x == 0.0 or rknee_x == 0.0 or rankle_x == 0.0:
         continue
      if rhip_y == 0.0 or rknee_y == 0.0 or rankle_y == 0.0:
         continue
      if lhip_x == 0.0 or lknee_x == 0.0 or lankle_x == 0.0:
         continue
      if lhip_y == 0.0 or lknee_y == 0.0 or lankle_y == 0.0:
         continue
      #print(line)
      #print(line[9:15], line[24:30]

      right_NeckAngle = getNeckAngle(Head_x-Neck_x, Head_y-Neck_y, rShoulder_x-Neck_x, rShoulder_y-Neck_y)
      left_NeckAngle = getNeckAngle(Head_x-Neck_x, Head_y-Neck_y, lShoulder_x-Neck_x, lShoulder_y-Neck_y)

      right_ElbowAngle = getElbowAngle(rShoulder_x-rElbow_x, rShoulder_y-rElbow_y, rWrist_x-rElbow_x, rWrist_y-rElbow_y)
      left_ElbowAngle = getElbowAngle(lShoulder_x-lElbow_x, lShoulder_y-lElbow_y, lWrist_x-lElbow_x, lWrist_y-lElbow_y)

      right_KneeAngle = getKneeAngle(rhip_x-rknee_x, rhip_y-rknee_y, rankle_x-rknee_x, rankle_y-rknee_y)
      left_KneeAngle = getKneeAngle(lhip_x-lknee_x, lhip_y-lknee_y, lankle_x-lknee_x, lankle_y-lknee_y)

      #print(line)

      print("right_Neck angle: " ,right_NeckAngle * 180/pi)
      print("left_Neck angle: " ,left_NeckAngle * 180/pi)
      print("")

      # print("right_Elbow angle: " ,right_ElbowAngle * 180/pi)
      # print("left_Elbow angle: " ,left_ElbowAngle * 180/pi)
      # print("")

      # print("right_Knee angle: " ,right_KneeAngle * 180/pi)
      # print("left_Knee angle: " ,left_KneeAngle * 180/pi)
      # print("")

   f.close()


if __name__ == "__main__":
   main()
