#!/usr/bin/python
import argparse
import eval_2d_side
import eval_3d_side
import eval_2d_front

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('lablepath', type=str, help='标注文件路径')
    parser.add_argument('percepath', type=str, help='感知文件路径')
    parser.add_argument('evaltype', type=str, help='评测类别，比如side2d,sidesubclass,side3d...')
    parser.add_argument('--oripicpath', type=str, help='标注原图的图片路径')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    lable_path = args.lablepath
    perce_path = args.percepath
    ori_pic_path = args.oripicpath
    eval_type = args.evaltype
    if eval_type == 'side2d':
        eval_2d_side = eval_2d_side.Eval2DSide(lable_path,perce_path,ori_pic_path)
        eval_2d_side.proc_json_data()
        eval_2d_side.match_lable_perce()
        eval_2d_side.eval_2d_side_recall()
        eval_2d_side.eval_2d_side_precision()
        if ori_pic_path:
            eval_2d_side.draw_recall_pic()
            eval_2d_side.draw_precision_pic()

    if eval_type == 'subclass':
        eval_subclass_side = eval_2d_side.Eval2DSide(lable_path,perce_path,ori_pic_path)
        eval_subclass_side.proc_json_data()
        eval_subclass_side.match_lable_perce()
        eval_subclass_side.eval_subsclass_side_recall()
        eval_subclass_side.eval_subsclass_side_precision()
        if ori_pic_path:
            eval_2d_side.draw_recall_pic()
            eval_2d_side.draw_precision_pic()

    if eval_type == 'side3d':
        eval_3d_side = eval_3d_side.Eval3DSide(lable_path,perce_path)
        eval_3d_side.proc_json_data()
    if eval_type == 'front2d':
        eval_2d_front = eval_2d_front.Eval2DFront(lable_path,perce_path,ori_pic_path)
        eval_2d_front.proc_json_data()
        eval_2d_front.match_lable_perce()
        eval_2d_front.eval_2d_front_recall()
        eval_2d_front.eval_2d_front_precision()
        if ori_pic_path:
            eval_2d_front.draw_recall_pic()
            eval_2d_front.draw_precision_pic()




