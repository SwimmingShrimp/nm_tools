import cv2
import os
import argparse


'''
使用说明：需要配置图片所在文件夹的路径，另外还需要配置视频保存的文件夹路径/视频名称
注意：需要修改压缩图片的分辨率
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('folder_pic',type=str,help='the path of pic_folder')
    parser.add_argument('path_output',type=str,help='the path of video_output')
    args = parser.parse_args()

    fourcc = cv2.VideoWriter.fourcc(*'MP4V')
    video_writer = cv2.VideoWriter(filename=args.path_output, fourcc=fourcc, fps=10, frameSize=(640, 384))

    for (root,_,pics) in os.walk(args.folder_pic):   #pics为列表,而且列表内的元素是无序的
        if len(pics) != 0:
           pics.sort(key=lambda x: int(x.rsplit('_')[-1].split('.')[0]))   #经过这步处理，此时pics已经是内部有序的列表
           print(pics)
           #pics.sort(key=lambda x: int(x.split('.')[0]))
           for pic in pics :
               print(pic)
               path_pic = os.path.join(root,pic)
               img = cv2.imread(path_pic)
               cv2.namedWindow('image',flags=cv2.WINDOW_NORMAL)
               cv2.resizeWindow('image',(1920,1080))
               cv2.imshow('image',img)
               cv2.waitKey(100)
               video_writer.write(img)
               #print(str(i) + '.jpg' + ' done!')
    # video_writer.release()
    # cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
