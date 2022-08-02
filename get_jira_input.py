import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('benchmarkid',type=str)
args = parser.parse_args()

relation_txt = ''
pic_src = ''
pic_dst = ''

