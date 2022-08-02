import argparse
import cv2 as cv
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('videoname')
parser.add_argument('speed')
args =  parser.parse_args()

videoname = args.videoname
speed = int(args.speed)
vc = cv.VideoCapture(videoname)

while True:
    ret, frame = vc.read()
    cv.imshow("capture",frame)
    if cv.waitKey(speed) & 0xFF == ord('q'):
        break
 