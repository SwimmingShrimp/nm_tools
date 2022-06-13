import os
import utils
import cv2

src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/DataSet/Shangqi/ori_labled_yuv_30'
for root,dirs,files in os.walk(src):
    dst = root.replace('ori_labled_yuv_30','ori_labled_yuv_30_black')
    if not os.path.exists(dst):
        os.makedirs(dst)
for root,files in utils.walk(src):
    dst = root.replace('ori_labled_yuv_30','ori_labled_yuv_30_black')
    for file_ in  files:
        print(file_)
        basename = os.path.basename(file_)
        img = cv2.imread(file_)
        img = cv2.copyMakeBorder(img, 0, 200, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        img_crop = img[150:1230, 0:1920]
        img_path = dst + '/' + basename
        print(img_path)
        cv2.imwrite(img_path,img_crop,)