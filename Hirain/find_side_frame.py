import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('front_frame',type=int)
# parser.add_argument('--picname')
args = parser.parse_args()
front_frame = args.front_frame

front_timestamp_log = '/media/fuqi/d99bf43c-b26e-4e29-88af-f2117b81f4e91/user/yanqing/mona/dataset/hirain/0719-5/front.log'
side_timestamp_log = '/media/fuqi/d99bf43c-b26e-4e29-88af-f2117b81f4e91/user/yanqing/mona/dataset/hirain/0719-5/side.log'
match_timestamp_log = '/media/fuqi/d99bf43c-b26e-4e29-88af-f2117b81f4e91/user/yanqing/mona/dataset/hirain/0719-5/timestamp_match.log'


with open(front_timestamp_log, 'r') as f:
    lines = f.readlines()
    for line in lines:
        _, frame_id, _, timestamp = line.split(' ')
        frame_id = int(frame_id)
        timestamp = int(timestamp)
        if front_frame == frame_id:
            front_timestamp = timestamp
            break

with open(match_timestamp_log, 'r') as f:
    lines = f.readlines()
    for line in lines:
        f_tt, s_tt = line.split(',')
        f_tt = int(f_tt)
        s_tt = int(s_tt)
        if front_timestamp == f_tt:
            side_timestamp = s_tt
            break

with open(side_timestamp_log, 'r') as f:
    lines = f.readlines()
    for line in lines:
        _, frame_id, _, timestamp = line.split(' ')
        frame_id = int(frame_id)
        timestamp = int(timestamp)
        if side_timestamp == timestamp:
            print('get side frame id: ', frame_id)
