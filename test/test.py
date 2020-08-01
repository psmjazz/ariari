import cv2
import numpy as np
import os
import json
import glob

def main(path):
    w = 700
    h = 700
    img = np.zeros((w, h))
    
    with open(path, 'r') as json_file:
        js = json.load(json_file)
        cnt = 0
        points = js['feature_pos']
        for frame in js["data"]:
            img.fill(255)
            if(cnt in points):
                img[0:10,0:10] = 0
            for kp in frame['keypoints']:
                if(frame['score'] < 0.2):
                    continue
                y = int(kp['position']['x'])
                x = int(kp['position']['y'])
                img[x-2:x+2, y-2:y+2] = 0
            cv2.imshow('ff', img)
            cv2.waitKey(60)
            cnt+=1
            # print(frame['score'])
    cv2.destroyAllWindows()
        


    


if __name__ == "__main__":
    files = glob.glob('./*.json')
    # print(files)
    for f in files:
        main(f)