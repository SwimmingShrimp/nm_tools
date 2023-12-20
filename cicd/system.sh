cd /dat/ci/result
rm -rf ./benchmark/*
cd /dat/ci/$1/config
sed -i 's/"is_pure_mode": false/"is_pure_mode": true/g' app.json
sed -i 's/"front_enable": false/"front_enable": true/g' app.json
sed -i 's/"side_enable": false/"side_enable": true/g' app.json
sed -i 's/"back_enable": false/"back_enable": true/g' app.json
sed -i 's/"around_enable": true/"around_enable": false/g' app.json
sed -i 's/"init_vehicle_status": "parking"/"init_vehicle_status": "driving"/g' app.json
cd /dat/ci/$1/config/camera
sed -i 's/"do_ldc": false/"do_ldc": true/g' front_far.json
sed -i 's/"do_ldc": false/"do_ldc": true/g' front_near.json
sed -i 's/"do_ldc": false/"do_ldc": true/g' side_left_front.json
sed -i 's/"do_ldc": false/"do_ldc": true/g' side_left_rear.json
sed -i 's/"do_ldc": false/"do_ldc": true/g' side_right_front.json
sed -i 's/"do_ldc": false/"do_ldc": true/g' side_right_rear.json
sed -i 's/"do_ldc": false/"do_ldc": true/g' back_middle.json
cd /dat/ci/$1/config/postprocess
sed -i 's/"is_record_results": true/"is_record_results": false/g' obstacle.json
sed -i 's/"save": true/"save": false/g' postprocess_common.json
sed -i 's/"save_as_video": true/"save_as_video": false/g' postprocess_common.json
cd /dat/ci/$1/config/capture
sed -i 's/"save_frame": true/"save_frame": false/g' nv_capture.json
sed -i 's/"save_as_video": true/"save_as_video": false/g' nv_capture.json
sed -i '17s/"slot_position": 1/"slot_position": 0/g' nv_capture.json
sed -i '23s/"slot_position": 0/"slot_position": 1/g' nv_capture.json
sed -i 's/"show_fps": true/"show_fps": false/g' nv_capture.json
cd /dat/ci/$1
export LD_LIBRARY_PATH=./lib:./lib/opencv:$LD_LIBRARY_PATH
nohup ./bin/sensor_camera_orin >> /dat/ci/result/system/fps_front_side_back.log & sleep 100;kill -2 $!

# cd /dat/ci/$1/config
# sed -i 's/"front_enable": true/"front_enable": false/g' app.json 
# sed -i 's/"side_enable": true/"side_enable": false/g' app.json
# sed -i 's/"back_enable": true/"back_enable": false/g' app.json
# sed -i 's/"around_enable": false/"around_enable": true/g' app.json
# sed -i 's/"is_pure_mode": true/"is_pure_mode": false/g' app.json
# sed -i 's/"init_vehicle_status": "driving"/"init_vehicle_status": "parking"/g' app.json
# cd /dat/ci/$1
# export LD_LIBRARY_PATH=./lib:./lib/opencv:$LD_LIBRARY_PATH
# nohup ./bin/sensor_camera_orin >> /dat/ci/result/system/fps_fisheye.log & & kill -2 $!
