from math import *
import numpy as np
import csv

def torso_normalization(line, mean_torso):
   new_line = []
   for i in range(1,30):
      new_line.append(line[i]/mean_torso)

   return new_line


def get_MeanTorso(Neck_x, Neck_y, rhip_x, rhip_y, lhip_x, lhip_y):
   Neck_point = [Neck_x, Neck_y]
   rhip_point = [rhip_x, rhip_y]
   lhip_point = [lhip_x, lhip_y]

   # 왜 dist 함수가 없다고 하는걸까...
   # left_torso_dist = dist(Neck_point, rhip_point)
   # right_torso_dist = dist(Neck_point, lhip_point)

   left_torso_dist = sqrt(pow(Neck_x-rhip_x,2)+pow(Neck_y-rhip_y,2))
   right_torso_dist = sqrt(pow(Neck_x-lhip_x,2)+pow(Neck_y-lhip_y,2))

   mean_torso = (left_torso_dist+right_torso_dist)/2

   return mean_torso


def main():
   f = open('/Users/parkyoungin/ariari/time_series_analysis/output/squat_skeleton_10_1.csv', 'r', encoding = 'utf-8')
   rdr = csv.reader(f)
   for line in rdr:
      if line[0] == '':
         continue
      # str로 float으로
      line = list(map(float, line))

      Neck_x, Neck_y = line[17], line[2]
      rhip_x, rhip_y = line[9], line[24]
      lhip_x, lhip_y = line[12], line[27]
      mean_torso = get_MeanTorso(Neck_x, Neck_y, rhip_x, rhip_y, lhip_x, lhip_y)
      new_line = torso_normalization(line, mean_torso)
      print(new_line)
      print("")

   f.close()


if __name__ == "__main__":
   main()
