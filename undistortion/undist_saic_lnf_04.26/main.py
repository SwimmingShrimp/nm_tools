import argparse
import inspect
import os
import sys

from pathlib import Path
import xml.etree.ElementTree as ET

import cv2
import numpy as np
import yaml

class Undistortion:
    def __init__(self, intrinsic_fpath, imsize=(1920, 1280)):
        self.imsize = imsize
        self.intrinsics = {'left_front': None,
                           'left_rear': None,
                           'right_front': None,
                           'right_rear': None
                           }
        self.undistort_maps  = {'left_front': None,
                                'left_rear': None,
                                'right_front': None,
                                'right_rear': None
                               }
        self.scaled_undistort_maps  = {'left_front': None,
                                        'left_rear': None,
                                        'right_front': None,
                                        'right_rear': None
                                        }
        self._load_intrinsic_paras(intrinsic_fpath)


    def undistort(self, img, cam_name):
        imh, imw = img.shape[:-1]
        assert(imw==self.imsize[0] and imh==self.imsize[1])
        mtx, dist = self.intrinsics[cam_name]
        # imsize = img.shape[:2][::-1]
        # mtx_new, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, imsize, alpha, imsize)
        print(mtx)
        mtx_new = mtx.copy()
        # mtx_new[0, 2] -= 100
        print(mtx_new)
        dst = cv2.undistort(img, mtx, dist, None, mtx_new)

    def remap(self, img, cam_name):
        map1, map2 = self.undistort_maps[cam_name]
        # dst = cv2.remap(img, map1, map2, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)
        dst = cv2.remap(img, map1, map2, cv2.INTER_CUBIC, cv2.BORDER_CONSTANT)
        return dst

    def scale_remap(self, img, cam_name):
        imh, imw = img.shape[:-1]
        assert(imw==self.imsize[0]*self.scale and imh==self.imsize[1]*self.scale)
        map1, map2 = self.scaled_undistort_maps[cam_name]
        dst = cv2.remap(img, map1, map2, cv2.INTER_CUBIC, cv2.BORDER_CONSTANT)
        return dst


    def init_undistort_map(self):
        imsize_new = self.imsize
        for cam_name in self.intrinsics:
            mtx, dist = self.intrinsics[cam_name]
            # mtx_new, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, imsize_new, 0, self.imsize, 1)
            mtx_new = np.array([[805.54, 0, 960],
                                [0, 805.54, 640],
                                [0, 0, 1]])
            # 数据采集车
            if cam_name == 'left_front':
                mtx_new[0, 2] += 80
            if cam_name == 'left_rear':
                mtx_new[0, 2] -= 20
            if cam_name == 'right_front':
                mtx_new[0, 2] -= 80
            if cam_name == 'right_rear':
                mtx_new[0, 2] -= 50
            # 实车
            # if cam_name == 'left_front':
            #     mtx_new[0, 2] += 190
            # if cam_name == 'left_rear':
            #     mtx_new[0, 2] += 230
            # if cam_name == 'right_front':
            #     mtx_new[0, 2] -= 160
            # if cam_name == 'right_rear':
            #     mtx_new[0, 2] -= 260
            print('NewCameraMatrix - {}\n        {}'.format(cam_name, mtx_new))
            # CV_16SC2 ?
            map1, map2 = cv2.initUndistortRectifyMap(mtx, dist, None, mtx_new, imsize_new, cv2.CV_32FC1)
            self.undistort_maps[cam_name] = (map1, map2)

    def scale_undistort_map(self, scale=0.5):
        self.scale = scale
        scale_w, scale_h = int(self.imsize[0] * self.scale), int(self.imsize[1] * self.scale)
        for cam_name in self.undistort_maps:
            map1, map2 = self.undistort_maps[cam_name]
            # scaled_map1 = np.zeros((scale_h, scale_w), dtype=np.float32)
            # scaled_map2 = np.zeros((scale_h, scale_w), dtype=np.float32)
            # for i in range(scale_h):
            #     for j in range(scale_w):
            #         scaled_map1[i, j] = map1[int(i*2), int(j*2)] * self.scale
            #         scaled_map2[i, j] = map2[int(i*2), int(j*2)] * self.scale
            scaled_map1 = cv2.resize(map1, (scale_w, scale_h)) * self.scale
            scaled_map2 = cv2.resize(map2, (scale_w, scale_h)) * self.scale
            self.scaled_undistort_maps[cam_name] = (scaled_map1, scaled_map2)

    def save_scaled_undistort_map(self, savep='undistort_maps'):
        def FillMiddle(ad_offset, offset, height, width):
            ad_offset[int(height / 2), :int(width / 2)] = (offset[int(height / 2), :int(width / 2)] + \
                                                        offset[int(height / 2) - 1, :int(width / 2)]) / 2.0
            ad_offset[int(height / 2), int(width / 2) + 1:] = (offset[int(height / 2), int(width / 2):] + \
                                                            offset[int(height / 2) - 1, int(width / 2):]) / 2.0
            ad_offset[:int(height / 2), int(width / 2)] = (offset[:int(height / 2), int(width / 2)] + \
                                                        offset[:int(height / 2), int(width / 2) - 1]) / 2.0
            ad_offset[int(height / 2) + 1:, int(width / 2)] = (offset[int(height / 2):, int(width / 2)] + \
                                                            offset[int(height / 2):, int(width / 2) - 1]) / 2.0
            ad_offset[int(height / 2), int(width / 2)] = (ad_offset[int(height / 2) - 1, int(width / 2)] + \
                                                        ad_offset[int(height / 2) + 1, int(width / 2)] + \
                                                        ad_offset[int(height / 2), int(width / 2) - 1] + \
                                                        ad_offset[int(height / 2), int(width / 2) + 1]) / 4.0
        
        if not Path(savep).exists():
            Path(savep).mkdir(parents=True, exist_ok=True)

        m = 3
        m_step = 2 ** m
        for cam_name in self.scaled_undistort_maps:
            map1, map2 = self.scaled_undistort_maps[cam_name]

            map_savefp = ''
            if cam_name == 'left_front':
                map_savefp = '{}/nearside_mirror_map.txt'.format(savep)
            elif cam_name == 'left_rear':
                map_savefp = '{}/nearside_wing_map.txt'.format(savep)
            elif cam_name == 'right_front':
                map_savefp = '{}/offside_mirror_map.txt'.format(savep)
            elif cam_name == 'right_rear':
                map_savefp = '{}/offside_wing_map.txt'.format(savep)
            else:
                assert(False)

            with open(map_savefp, 'w+') as fp:
                offset_x = np.zeros(map1.shape)
                offset_y = np.zeros(map2.shape)
                height, width = map1.shape
                for i in range(height):
                    for j in range(width):
                        offset_x[i, j] = (map1[i, j] - j) * 8
                        offset_y[i, j] = (map2[i, j] - i) * 8

                ad_offset_x = np.zeros((map1.shape[0] + 1, map1.shape[1] + 1))
                ad_offset_y = np.zeros((map2.shape[0] + 1, map2.shape[1] + 1))
                # fill adjust offset
                # 1st Quadrant
                ad_offset_x[:int(height / 2), int(width / 2) + 1:] = offset_x[:int(height / 2), int(width / 2):]
                ad_offset_y[:int(height / 2), int(width / 2) + 1:] = offset_y[:int(height / 2), int(width / 2):]

                # 2nd Quadrant
                ad_offset_x[:int(height / 2), :int(width / 2)] = offset_x[:int(height / 2), :int(width / 2)]
                ad_offset_y[:int(height / 2), :int(width / 2)] = offset_y[:int(height / 2), :int(width / 2)]

                # 3rd Quadrant
                ad_offset_x[int(height / 2) + 1:, :int(width / 2)] = offset_x[int(height / 2):, :int(width / 2)]
                ad_offset_y[int(height / 2) + 1:, :int(width / 2)] = offset_y[int(height / 2):, :int(width / 2)]

                # 4th Quadrant
                ad_offset_x[int(height / 2) + 1:, int(width / 2) + 1:] = offset_x[int(height / 2):, int(width / 2):]
                ad_offset_y[int(height / 2) + 1:, int(width / 2) + 1:] = offset_y[int(height / 2):, int(width / 2):]

                FillMiddle(ad_offset_x, offset_x, height, width)
                FillMiddle(ad_offset_y, offset_y, height, width)

                for i in range(0, height + 1, m_step):
                    for j in range(0, width + 1, m_step):
                        fp.write(str(int(round(ad_offset_x[i, j]))) + ' ' + str(int(round(ad_offset_y[i, j]))) + '\n')

    def _load_intrinsic_paras(self, intrinsic_fpath):
        if not os.path.isfile(intrinsic_fpath):
            assert(False)

        if intrinsic_fpath.endswith('.xml'):  # xml
            tree = ET.parse(intrinsic_fpath)
            root = tree.getroot()
            spd = root.find('spd')   
            self.intrinsics['left_front'] = self._get_K_D(spd, 'nearside_mirror', mode='xml')
            self.intrinsics['left_rear'] = self._get_K_D(spd, 'nearside_wing', mode='xml')
            self.intrinsics['right_front'] = self._get_K_D(spd, 'offside_mirror', mode='xml')
            self.intrinsics['right_rear'] = self._get_K_D(spd, 'offside_wing', mode='xml')
        else:  # yaml
            with open(intrinsic_fpath, 'r') as f:
                intrinsics = yaml.load(f, Loader=yaml.Loader)
                self.intrinsics['left_front'] = self._get_K_D(intrinsics, 'left_front', mode='dict')
                self.intrinsics['left_rear'] = self._get_K_D(intrinsics, 'left_rear', mode='dict')
                self.intrinsics['right_front'] = self._get_K_D(intrinsics, 'right_front', mode='dict')
                self.intrinsics['right_rear'] = self._get_K_D(intrinsics, 'right_rear', mode='dict')

    def _get_K_D(self, intrinsics, cam_alias, mode):
        if mode == 'xml':
            fx = eval(intrinsics.find('{}_fx'.format(cam_alias)).text)
            fy = eval(intrinsics.find('{}_fy'.format(cam_alias)).text)
            cx = eval(intrinsics.find('{}_cx'.format(cam_alias)).text)
            cy = eval(intrinsics.find('{}_cy'.format(cam_alias)).text)
            k1 = eval(intrinsics.find('{}_k1'.format(cam_alias)).text)
            k2 = eval(intrinsics.find('{}_k2'.format(cam_alias)).text)
            k3 = eval(intrinsics.find('{}_k3'.format(cam_alias)).text)
            k4 = eval(intrinsics.find('{}_k4'.format(cam_alias)).text)
            k5 = eval(intrinsics.find('{}_k5'.format(cam_alias)).text)
            k6 = eval(intrinsics.find('{}_k6'.format(cam_alias)).text)
            p1 = eval(intrinsics.find('{}_p1'.format(cam_alias)).text)
            p2 = eval(intrinsics.find('{}_p2'.format(cam_alias)).text)
        if mode == 'dict':
            fx = intrinsics[cam_alias]['fx']
            fy = intrinsics[cam_alias]['fy']
            cx = intrinsics[cam_alias]['cx']
            cy = intrinsics[cam_alias]['cy']
            k1 = intrinsics[cam_alias]['k1']
            k2 = intrinsics[cam_alias]['k2']
            k3 = intrinsics[cam_alias]['k3']
            k4 = intrinsics[cam_alias]['k4']
            k5 = intrinsics[cam_alias]['k5']
            k6 = intrinsics[cam_alias]['k6']
            p1 = intrinsics[cam_alias]['p1']
            p2 = intrinsics[cam_alias]['p2']

        mtx = np.array([[fx, 0, cx],
                        [0, fy, cy],
                        [0, 0, 1]])
        dist = np.array([k1, k2, p1, p2, k3, k4, k5, k6])
        return mtx, dist

def get_fname(fname, cam_name):
    idx = fname[:-4].split('_')[-1]
    imfmt = fname[-4:]
    if cam_name in ['left_front', '']:
        camid = '2'
    elif cam_name in ['left_rear', '']:
        camid = '4'
    elif cam_name in ['right_front', '']:
        camid = '3'
    elif cam_name in ['right_rear', '']:
        camid = '1'
    else:
        assert(False), 'cam_name:{} is not defined'.format(cam_name)
    fname = 'frame_vc{}_{}{}'.format(camid, idx, imfmt)
    return fname


# def handle_4cam():
#     args = parse_args()
#     undist = Undistortion(intrinsic_fpath=args.intrinsic, imsize=(1920, 1280))
#     undist.init_undistort_map()
#     undist.scale_undistort_map(scale = args.imsize[0]/1920)
#     # undist.save_scaled_undistort_map()
    
#     cv2.namedWindow('view', cv2.WINDOW_NORMAL)
#     imlist = sorted(os.listdir(os.path.join(args.imgp, 'left_front')), key=lambda fname:int(fname[:-4].split('_')[-1]))
#     for fname in imlist:
#         ims = []
#         for cam_name in ['left_front', 'left_rear', 'right_front', 'right_rear']:
#             fname = get_fname(fname, cam_name)
#             imfp = os.path.join(args.imgp, cam_name, fname)
#             if os.path.exists(imfp):
#                 im = cv2.imread(imfp)
#             else:
#                 im = np.zeros((args.imsize[1], args.imsize[0], 3), dtype=np.uint8)
#             img_undist = undist.remap(im.copy(), cam_name)
#             ims.append(img_undist)
#         # imshow = cv2.vconcat([cv2.hconcat([ims[0], ims[2]]),
#         #                       cv2.hconcat([ims[1], ims[3]])])
#         cv2.imshow('view', imshow)
#         key = cv2.waitKey(0)
#         if key == ord('q'):
#             break

def get_cam_name(fp):
    cam_name = ''
    if 'RearRight' in fp or 'right_rear' in fp:
        cam_name = 'right_rear'
    elif 'RearLeft' in fp or 'left_rear' in fp:
        cam_name = 'left_rear'
    elif 'FrontRight' in fp or 'right_front' in fp:
        cam_name = 'right_front'
    elif 'FrontLeft' in fp or 'left_front' in fp:
        cam_name = 'left_front'
    else:
        assert(False)
    return cam_name

def parse_args():
    parser = argparse.ArgumentParser('Undistortion Tool')
    parser.add_argument('--imgp', type=str, 
                        default='data/images/saic', 
                        help='path of distorted images')
    parser.add_argument('--intrinsic', type=str, 
                        default='data/paras/saic/multi_cam_calibration_params_decrypt.xml')
    parser.add_argument('--dst', type=str, 
                        default='data/savep')
    parser.add_argument('--stream', action='store_true')
    # parser.add_argument('--imsize', nargs='+', default=[960, 640])
    args = parser.parse_args()
    args.stream = int(args.stream)
    print(args)
    return args

def main():
    args = parse_args()
    undist = Undistortion(intrinsic_fpath=args.intrinsic, imsize=(1920, 1280))
    undist.init_undistort_map()
    
    cv2.namedWindow('view', cv2.WINDOW_NORMAL)
    cnt = 0
    for rt, _, fnames in os.walk(args.imgp):
        if len(fnames) == 0: continue
        for fname in fnames:
            if fname[-4:] not in ['.jpg', '.png', '.bmp']: continue
            cnt += 1
            imfp = os.path.join(rt, fname)
            print('==> cnt: {} imgfp: {}'.format(cnt, imfp))

            cam_name = get_cam_name(imfp)
            im = cv2.imread(imfp)
            assert(im.shape[0] == 1280)
            im_undist = undist.remap(im.copy(), cam_name)
            imp_dst = Path(args.dst) / Path(rt).relative_to(args.imgp)
            imfp_dst = imp_dst / Path(fname).with_suffix('.jpg')
            if not imp_dst.exists():
                imp_dst.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(imfp_dst.as_posix(), im_undist)
            cv2.imshow('view', np.hstack([im, im_undist]))
            key = cv2.waitKey(args.stream)
            if key == ord('q'):
                sys.exit()
    cv2.destroyAllWindow()


if __name__ == '__main__':
    main()
            