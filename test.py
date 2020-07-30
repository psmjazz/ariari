import json
import os

print(os.getcwd())

with open('ariari/squat_3.json', 'r') as json_file:
    js = json.load(json_file)
    cnt = 0
    for f in js["data"]:
        # print(f['keypoints'][9]['position'], "     ", f['keypoints'][10]['position'])
        ymean = f['keypoints'][9]['position']['y'] + f['keypoints'][10]['position']['y']
        ymean/=2
        print(ymean)
        # ymean = f['keypoints'][9]['position']['x'] + f['keypoints'][10]['position']['x']
        # ymean/=2
        # print(ymean)
        cnt+=1
    print('count : ', cnt)