# 清空历史数据
cd /ota/ci/result/smoke
rm -r /ota/ci/result/smoke/*
mkdir front_side_back1
mkdir front_side_back2
mkdir fisheye1
mkdir fisheye2

# 修改配置文件：前视+周视+后视冒烟测试
echo "Smoke Test:Modify Front&Side&Back Camera Config File"
cd /ota/ci/$1/config
sed -i 's/"front_enable": false/"front_enable": true/g' app.json
sed -i 's/"side_enable": false/"side_enable": true/g' app.json
sed -i 's/"back_enable": false/"back_enable": true/g' app.json
sed -i 's/"around_enable": true/"around_enable": false/g' app.json
sed -i 's/"is_pure_mode": true/"is_pure_mode": false/g' app.json
sed -i 's/"init_vehicle_status": "parking"/"init_vehicle_status": "driving"/g' app.json
cd /ota/ci/$1/config/camera
sed -i 's/"do_ldc": true/"do_ldc": false/g' front_far.json
sed -i 's/"do_ldc": true/"do_ldc": false/g' front_near.json
sed -i 's/"do_ldc": true/"do_ldc": false/g' side_left_front.json
sed -i 's/"do_ldc": true/"do_ldc": false/g' side_left_rear.json
sed -i 's/"do_ldc": true/"do_ldc": false/g' side_right_front.json
sed -i 's/"do_ldc": true/"do_ldc": false/g' side_right_rear.json
sed -i 's/"do_ldc": true/"do_ldc": false/g' back_middle.json
cd /ota/ci/$1/config/postprocess
sed -i 's/"save": false/"save": true/g' postprocess_common.json
sed -i 's/"save_as_video": true/"save_as_video": false/g' postprocess_common.json
sed -i '14c"save_dir": "\/ota\/ci\/result\/smoke\/front_side_back1\/model_input_frame"' postprocess_common.json
sed -i '19c"save_dir": "\/ota\/ci\/result\/smoke\/front_side_back1\/painted_frame"' postprocess_common.json
sed -i '24c"save_dir": "\/ota\/ci\/result\/smoke\/front_side_back1\/fusion_frame"' postprocess_common.json
sed -i '28c"save_file": "\/ota\/ci\/result\/smoke\/front_side_back1\/vehicle_status.txt"' postprocess_common.json
cd /ota/ci/$1/config/capture
sed -i 's/"save_frame": false/"save_frame": true/g' nv_capture.json
sed -i 's/"save_as_video": true/"save_as_video": false/g' nv_capture.json
sed -i '13c"save_frame_dir": "\/ota\/ci\/result\/smoke\/front_side_back1\/capture_frame\/"' nv_capture.json
sed -i 's/"show_fps": true/"show_fps": false/g' nv_capture.json
sed -i '6c"totol_pic_count": 35,' offline_capture.json
sed -i '15c"pic_dir": "\/ota\/pic\/smoke_pic\/front_far\/",' offline_capture.json
sed -i '22c"pic_dir": "\/ota\/pic\/smoke_pic\/front_near\/",' offline_capture.json
sed -i '85c"pic_dir": "\/ota\/pic\/smoke_pic\/back_middle\/",' offline_capture.json
sed -i '29c"pic_dir": "\/ota\/pic\/smoke_pic\/side_left_front\/",' offline_capture.json
sed -i '36c"pic_dir": "\/ota\/pic\/smoke_pic\/side_left_rear\/",' offline_capture.json
sed -i '43c"pic_dir": "\/ota\/pic\/smoke_pic\/side_right_front\/",' offline_capture.json
sed -i '50c"pic_dir": "\/ota\/pic\/smoke_pic\/side_right_rear\/",' offline_capture.json
# 冒烟测试(图片)：前视+周视+环视
cd /ota/ci/$1
./startoffline.sh

# 冒烟测试(视频)：前视+周视+环视
cd /ota/ci/$1/config/postprocess
sed -i 's/"save": false/"save": true/g' postprocess_common.json
sed -i 's/"save_as_video": false/"save_as_video": true/g' postprocess_common.json
sed -i '14c"save_dir": "\/ota\/ci\/result\/smoke\/front_side_back2\/model_input_frame"' postprocess_common.json
sed -i '19c"save_dir": "\/ota\/ci\/result\/smoke\/front_side_back2\/painted_frame"' postprocess_common.json
sed -i '24c"save_dir": "\/ota\/ci\/result\/smoke\/front_side_back2\/fusion_frame"' postprocess_common.json
sed -i '28c"save_file": "\/ota\/ci\/result\/smoke\/front_side_back2\/vehicle_status.txt"' postprocess_common.json
cd /ota/ci/$1/config/capture
sed -i 's/"save_frame": false/"save_frame": true/g' nv_capture.json
sed -i 's/"save_as_video": false/"save_as_video": true/g' nv_capture.json
sed -i '13c"save_frame_dir": "\/ota\/ci\/result\/smoke\/front_side_back2\/capture_frame\/"' nv_capture.json
cd /ota/ci/$1
./startoffline.sh


echo "Smoke Test:Modify Fisheye Camera Config File"
cd /ota/ci/$1/config
sed -i 's/"front_enable": true/"front_enable": false/g' app.json
sed -i 's/"side_enable": true/"side_enable": false/g' app.json
sed -i 's/"back_enable": true/"back_enable": false/g' app.json
sed -i 's/"around_enable": false/"around_enable": true/g' app.json
sed -i 's/"is_pure_mode": true/"is_pure_mode": false/g' app.json
sed -i 's/"init_vehicle_status": "driving"/"init_vehicle_status": "parking"/g' app.json
cd /ota/ci/$1/config/camera
sed -i 's/"do_ldc": true/"do_ldc": false/g' fish_front.json
sed -i 's/"do_ldc": true/"do_ldc": false/g' fish_back.json
sed -i 's/"do_ldc": true/"do_ldc": false/g' fish_left.json
sed -i 's/"do_ldc": true/"do_ldc": false/g' fish_right.json
cd /ota/ci/$1/config/postprocess
sed -i 's/"is_record_results": false/"is_record_results": true/g' obstacle.json
sed -i 's/"save": false/"save": true/g' postprocess_common.json
sed -i 's/"save_as_video": true/"save_as_video": false/g' postprocess_common.json
sed -i '14c"save_dir": "\/ota\/ci\/result\/smoke\/fisheye1\/model_input_frame"' postprocess_common.json
sed -i '19c"save_dir": "\/ota\/ci\/result\/smoke\/fisheye1\/painted_frame"' postprocess_common.json
# sed -i '24c"save_dir": "\/ota\/ci\/result\/smoke\/fisheye\/fusion_frame"' postprocess_common.json
sed -i '28c"save_file": "\/ota\/ci\/result\/smoke\/fisheye1\/vehicle_status.txt"' postprocess_common.json
sed -i '22c"save": false,' postprocess_common.json
cd /ota/ci/$1/config/capture
sed -i 's/"save_frame": false/"save_frame": true/g' nv_capture.json
sed -i 's/"save_as_video": true/"save_as_video": false/g' nv_capture.json
sed -i '13c"save_frame_dir": "\/ota\/ci\/result\/smoke\/fisheye1\/capture_frame\/"' nv_capture.json
sed -i 's/"show_fps": false/"show_fps": true/g' nv_capture.json
sed -i '5c"pic_suffix": ".bmp",' offline_capture.json
sed -i '6c"totol_pic_count": 6,' offline_capture.json
sed -i '57c"pic_dir": "\/ota\/pic\/smoke_pic\/fish_left\/",' offline_capture.json
sed -i '64c"pic_dir": "\/ota\/pic\/smoke_pic\/fish_front\/",' offline_capture.json
sed -i '71c"pic_dir": "\/ota\/pic\/smoke_pic\/fish_right\/",' offline_capture.json
sed -i '78c"pic_dir": "\/ota\/pic\/smoke_pic\/fish_back\/",' offline_capture.json
cd /ota/ci/$1
./startoffline.sh


cd /ota/ci/$1/config/postprocess
sed -i 's/"save": false/"save": true/g' postprocess_common.json
sed -i 's/"save_as_video": false/"save_as_video": true/g' postprocess_common.json
sed -i '14c"save_dir": "\/ota\/ci\/result\/smoke\/fisheye2\/model_input_frame"' postprocess_common.json
sed -i '19c"save_dir": "\/ota\/ci\/result\/smoke\/fisheye2\/painted_frame"' postprocess_common.json
sed -i '28c"save_file": "\/ota\/ci\/result\/smoke\/fisheye2\/vehicle_status.txt"' postprocess_common.json
sed -i '22c"save": false,' postprocess_common.json
cd /ota/ci/$1/config/capture
sed -i 's/"save_frame": false/"save_frame": true/g' nv_capture.json
sed -i 's/"save_as_video": true/"save_as_video": true/g' nv_capture.json
sed -i '13c"save_frame_dir": "\/ota\/ci\/result\/smoke\/fisheye2\/capture_frame\/"' nv_capture.json
cd /ota/ci/$1
./startoffline.sh