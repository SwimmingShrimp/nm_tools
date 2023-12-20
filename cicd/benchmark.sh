cd /ota/ci/$1/config
sed -i 's/"front_enable": false/"front_enable": true/g' app.json
sed -i 's/"side_enable": true/"side_enable": false/g' app.json
sed -i 's/"back_enable": true/"back_enable": false/g' app.json
sed -i 's/"around_enable": true/"around_enable": false/g' app.json
sed -i 's/"is_pure_mode": false/"is_pure_mode": true/g' app.json
sed -i 's/"init_vehicle_status": "parking"/"init_vehicle_status": "driving"/g' app.json
sed -i '14c"log_level": 1' app.json
cd /ota/ci/$1/config/camera
sed -i 's/"do_ldc": true/"do_ldc": false/g' front_far.json
sed -i 's/"do_ldc": true/"do_ldc": false/g' front_near.json
sed -i 's/"do_ldc": true/"do_ldc": false/g' side_left_front.json
sed -i 's/"do_ldc": true/"do_ldc": false/g' side_left_rear.json
sed -i 's/"do_ldc": true/"do_ldc": false/g' side_right_front.json
sed -i 's/"do_ldc": true/"do_ldc": false/g' side_right_rear.json
sed -i 's/"do_ldc": true/"do_ldc": false/g' back_middle.json
cd /ota/ci/$1/config/postprocess
sed -i 's/"is_record_results": false/"is_record_results": true/g' obstacle.json
sed -i 's/"debug_mode": false/"debug_mode": true/g' obstacle.json
sed -i 's/"save": true/"save": false/g' postprocess_common.json
sed -i 's/"save_as_video": true/"save_as_video": false/g' postprocess_common.json
cd /ota/ci/$1/config/capture
sed -i 's/"save_frame": true/"save_frame": false/g' nv_capture.json
sed -i 's/"show_fps": true/"show_fps": false/g' nv_capture.json
sed -i '5c"pic_suffix": ".jpg",' offline_capture.json
cd /ota/ci/$1/config/camera
sed -i '10c"rot_x_alfa": 88.3,' front_far.json
sed -i '11c"rot_y_beta": -0.9,' front_far.json
sed -i '12c"rot_z_gama": 93.2,' front_far.json
sed -i '13c"trans_x0": 2.238,' front_far.json
sed -i '14c"trans_y0": -0.06,' front_far.json
sed -i '15c"trans_z0": 1.2' front_far.json
sed -i '4c"fx": 7163.03712,' front_far.json
sed -i '5c"fy": 7163.03712,' front_far.json
sed -i '6c"cx": 1919.5,' front_far.json
sed -i '7c"cy": 1079.5' front_far.json
sed -i '10c"rot_x_alfa": 88.0,' front_near.json
sed -i '11c"rot_y_beta": -3.0,' front_near.json
sed -i '12c"rot_z_gama": 92.0,' front_near.json
sed -i '13c"trans_x0": 2.038,' front_near.json
sed -i '14c"trans_y0": 0.06,' front_near.json
sed -i '15c"trans_z0": 1.21' front_near.json
sed -i '4c"fx": 1981.63361862,' front_near.json
sed -i '5c"fy": 1981.63361862,' front_near.json
sed -i '6c"cx": 1919.0,' front_near.json
sed -i '7c"cy": 1079.0' front_near.json
cd /ota/ci/result
rm -rf ./benchmark/*

front_2d_day_6278() {
    echo "Execute front_2d_day_6278 Benchmark"
    cd /ota/ci/$1/config/capture
    sed -i '15c"pic_dir": "\/ota\/pic\/front_2d_day_6278\/front_far\/",' offline_capture.json
    sed -i '22c"pic_dir": "\/ota\/pic\/front_2d_day_6278\/front_near\/",' offline_capture.json
    sed -i '6c"totol_pic_count": 6278,' offline_capture.json
    cd /ota/ci/$1
    ./startoffline.sh
    mv image_record/image_record_json/camera_fusion /ota/ci/result/benchmark/front_2d_day
    rm -r image_record
}
 
front_2d_night_2027(){
    echo "Execute front_2d_night_2027 Benchmark"
    cd /ota/ci/$1/config/capture
    sed -i '15c"pic_dir": "\/ota\/pic\/front_2d_night_2027\/front_far\/",' offline_capture.json
    sed -i '22c"pic_dir": "\/ota\/pic\/front_2d_night_2027\/front_near\/",' offline_capture.json
    sed -i '6c"totol_pic_count": 2027,' offline_capture.json
    cd /ota/ci/$1
    ./startoffline.sh
    mv image_record/image_record_json/camera_fusion /ota/ci/result/benchmark/front_2d_night
    rm -r image_record
}

front_k3_day_4674(){
    echo "Execute front_k3_day_4674 Benchmark"
    cd /ota/ci/$1/config/capture
    sed -i '15c"pic_dir": "\/ota\/pic\/front_k3_day_4674\/front_far\/",' offline_capture.json
    sed -i '22c"pic_dir": "\/ota\/pic\/front_k3_day_4674\/front_near\/",' offline_capture.json
    sed -i '6c"totol_pic_count": 4674,' offline_capture.json
    cd /ota/ci/$1
    ./startoffline.sh
    mv image_record/image_record_json/camera_fusion /ota/ci/result/benchmark/front_k3_day
    rm -r image_record
}

front_k3_night_1804(){
    echo "Execute front_k3_night_1804 Benchmark"
    cd /ota/ci/$1/config/capture
    sed -i '15c"pic_dir": "\/ota\/pic\/front_k3_night_1804\/front_far\/",' offline_capture.json
    sed -i '22c"pic_dir": "\/ota\/pic\/front_k3_night_1804\/front_near\/",' offline_capture.json
    sed -i '6c"totol_pic_count": 1804,' offline_capture.json
    cd /ota/ci/$1
    ./startoffline.sh
    mv image_record/image_record_json/camera_fusion /ota/ci/result/benchmark/front_k3_night
    rm -r image_record
}

front_barrier_day_1004(){
    echo "Execute front_barrier_day_1004 Benchmark"
    cd /ota/ci/$1/config/capture
    sed -i '15c"pic_dir": "\/ota\/pic\/front_barrier_day_1004\/front_far\/",' offline_capture.json
    sed -i '22c"pic_dir": "\/ota\/pic\/front_barrier_day_1004\/front_near\/",' offline_capture.json
    sed -i '6c"totol_pic_count": 1004,' offline_capture.json
    cd /ota/ci/$1
    ./startoffline.sh
    mv image_record/image_record_json/camera_fusion /ota/ci/result/benchmark/front_barrier_day
    rm -r image_record
}

front_barrier_night_441(){
    echo "Execute front_barrier_night_441 Benchmark"
    cd /ota/ci/$1/config/capture
    sed -i '15c"pic_dir": "\/ota\/pic\/front_barrier_night_441\/front_far\/",' offline_capture.json
    sed -i '22c"pic_dir": "\/ota\/pic\/front_barrier_night_441\/front_near\/",' offline_capture.json
    sed -i '6c"totol_pic_count": 441,' offline_capture.json
    cd /ota/ci/$1
    ./startoffline.sh
    mv image_record/image_record_json/camera_fusion /ota/ci/result/benchmark/front_barrier_night
    rm -r image_record
}

front_tsr_6532(){
    echo "Execute front_tsr_6532 Benchmark"
    cd /ota/ci/$1/config/capture
    sed -i '15c"pic_dir": "\/ota\/pic\/front_tsr_6532\/front_far\/",' offline_capture.json
    sed -i '22c"pic_dir": "\/ota\/pic\/front_tsr_6532\/front_near\/",' offline_capture.json
    sed -i '6c"totol_pic_count": 6532,' offline_capture.json
    cd /ota/ci/$1
    ./startoffline.sh
    mv image_record/image_record_json/camera_fusion /ota/ci/result/benchmark/front_tsr
    rm -r image_record
}

front_tl_1000(){
    echo "Execute front_tl_1000 Benchmark"
    cd /ota/ci/$1/config/capture
    sed -i '15c"pic_dir": "\/ota\/pic\/front_tl_1000\/front_far\/",' offline_capture.json
    sed -i '22c"pic_dir": "\/ota\/pic\/front_tl_1000\/front_near\/",' offline_capture.json
    sed -i '6c"totol_pic_count": 1000,' offline_capture.json
    cd /ota/ci/$1
    ./startoffline.sh
    mv image_record/image_record_json/camera_fusion /ota/ci/result/benchmark/front_tl
    rm -r image_record
}

ihc_day(){
    echo "Execute ihc_day_717 Benchmark"
    cd /ota/ci/$1/config
    sed -i 's/"front_enable": false/"front_enable": true/g' app.json
    sed -i 's/"side_enable": true/"side_enable": false/g' app.json
    sed -i 's/"back_enable": true/"back_enable": false/g' app.json
    sed -i 's/"around_enable": true/"around_enable": false/g' app.json
    cd /ota/ci/$1/config
    sed -i '14c"log_level": 0' app.json
    cd /ota/ci/$1/config/capture
    sed -i '15c"pic_dir": "\/ota\/pic\/ihc_add50\/ihc_day_717\/front_far\/",' offline_capture.json
    sed -i '22c"pic_dir": "\/ota\/pic\/ihc_add50\/ihc_day_717\/front_near\/",' offline_capture.json
    sed -i '6c"totol_pic_count": 717,' offline_capture.json
    cd /ota/ci/$1
    rm nmlog_defualt.*
    ./startoffline.sh
    mkdir /ota/ci/result/benchmark/ihc_day
    cp nmlog_defualt.log /ota/ci/result/benchmark/ihc_day
    rm -r image_record
    cd /ota/ci/$1/config
    sed -i '14c"log_level": 2' app.json
}

ihc_monight(){
    echo "Execute ihc_monight_749 Benchmark"
    cd /ota/ci/$1/config
    sed -i 's/"front_enable": false/"front_enable": true/g' app.json
    sed -i 's/"side_enable": true/"side_enable": false/g' app.json
    sed -i 's/"back_enable": true/"back_enable": false/g' app.json
    sed -i 's/"around_enable": true/"around_enable": false/g' app.json
    cd /ota/ci/$1/config
    sed -i '14c"log_level": 0' app.json
    cd /ota/ci/$1/config/capture
    sed -i '15c"pic_dir": "\/ota\/pic\/ihc_add50\/ihc_monight_749\/front_far\/",' offline_capture.json
    sed -i '22c"pic_dir": "\/ota\/pic\/ihc_add50\/ihc_monight_749\/front_near\/",' offline_capture.json
    sed -i '6c"totol_pic_count": 749,' offline_capture.json
    cd /ota/ci/$1
    rm nmlog_defualt.*
    ./startoffline.sh
    mkdir /ota/ci/result/benchmark/ihc_monight
    cp nmlog_defualt.log /ota/ci/result/benchmark/ihc_monight
    rm -r image_record
    cd /ota/ci/$1/config
    sed -i '14c"log_level": 2' app.json
}

ihc_night(){
    echo "Execute ihc_night_731 Benchmark"
    cd /ota/ci/$1/config
    sed -i 's/"front_enable": false/"front_enable": true/g' app.json
    sed -i 's/"side_enable": true/"side_enable": false/g' app.json
    sed -i 's/"back_enable": true/"back_enable": false/g' app.json
    sed -i 's/"around_enable": true/"around_enable": false/g' app.json
    cd /ota/ci/$1/config
    sed -i '14c"log_level": 0' app.json
    cd /ota/ci/$1/config/capture
    sed -i '15c"pic_dir": "\/ota\/pic\/ihc_add50\/ihc_night_731\/front_far\/",' offline_capture.json
    sed -i '22c"pic_dir": "\/ota\/pic\/ihc_add50\/ihc_night_731\/front_near\/",' offline_capture.json
    sed -i '6c"totol_pic_count": 731,' offline_capture.json
    cd /ota/ci/$1
    rm nmlog_defualt.*
    ./startoffline.sh
    mkdir /ota/ci/result/benchmark/ihc_night
    cp nmlog_defualt.log /ota/ci/result/benchmark/ihc_night
    rm -r image_record
    cd /ota/ci/$1/config
    sed -i '14c"log_level": 2' app.json
}

ihc_no_obstacle(){
    echo "Execute night_no_obstacle_250 Benchmark"
    cd /ota/ci/$1/config
    sed -i 's/"front_enable": false/"front_enable": true/g' app.json
    sed -i 's/"side_enable": true/"side_enable": false/g' app.json
    sed -i 's/"back_enable": true/"back_enable": false/g' app.json
    sed -i 's/"around_enable": true/"around_enable": false/g' app.json
    cd /ota/ci/$1/config
    sed -i '14c"log_level": 0' app.json
    cd /ota/ci/$1/config/capture
    sed -i '15c"pic_dir": "\/ota\/pic\/ihc_add50\/night_no_obstacle_250\/front_far\/",' offline_capture.json
    sed -i '22c"pic_dir": "\/ota\/pic\/ihc_add50\/night_no_obstacle_250\/front_near\/",' offline_capture.json
    sed -i '6c"totol_pic_count": 250,' offline_capture.json
    cd /ota/ci/$1
    rm nmlog_defualt.*
    ./startoffline.sh
    mkdir /ota/ci/result/benchmark/night_no_obstacle
    cp nmlog_defualt.log /ota/ci/result/benchmark/night_no_obstacle
    rm -r image_record
    cd /ota/ci/$1/config
    sed -i '14c"log_level": 2' app.json
}

side_2d_day(){
    echo "Execute side_2d_day_3350 Benchmark"
    cd /ota/ci/$1/config
    sed -i 's/"front_enable": true/"front_enable": false/g' app.json
    sed -i 's/"side_enable": false/"side_enable": true/g' app.json
    sed -i 's/"back_enable": true/"back_enable": false/g' app.json
    sed -i 's/"around_enable": true/"around_enable": false/g' app.json
    cd /ota/ci/$1/config/capture
    sed -i '29c"pic_dir": "\/ota\/pic\/side_2d_day_3350\/side_left_front\/",' offline_capture.json
    sed -i '36c"pic_dir": "\/ota\/pic\/side_2d_day_3350\/side_left_rear\/",' offline_capture.json
    sed -i '43c"pic_dir": "\/ota\/pic\/side_2d_day_3350\/side_right_front\/",' offline_capture.json
    sed -i '50c"pic_dir": "\/ota\/pic\/side_2d_day_3350\/side_right_rear\/",' offline_capture.json
    sed -i '6c"totol_pic_count": 3350,' offline_capture.json
    cd /ota/ci/$1/config/postprocess
    sed -i '75a"disable_obstacle_tracking":true,' obstacle.json
    cd /ota/ci/$1
    ./startoffline.sh
    mv image_record/image_record_json/camera_fusion /ota/ci/result/benchmark/side_2d_day
    rm -r image_record
}
 
side_2d_night(){
    echo "Execute side_2d_night_799 Benchmark"
    cd /ota/ci/$1/config
    sed -i 's/"front_enable": true/"front_enable": false/g' app.json
    sed -i 's/"side_enable": false/"side_enable": true/g' app.json
    sed -i 's/"back_enable": true/"back_enable": false/g' app.json
    sed -i 's/"around_enable": true/"around_enable": false/g' app.json
    cd /ota/ci/$1/config/capture
    sed -i '29c"pic_dir": "\/ota\/pic\/side_2d_night_799\/side_left_front\/",' offline_capture.json
    sed -i '36c"pic_dir": "\/ota\/pic\/side_2d_night_799\/side_left_rear\/",' offline_capture.json
    sed -i '43c"pic_dir": "\/ota\/pic\/side_2d_night_799\/side_right_front\/",' offline_capture.json
    sed -i '50c"pic_dir": "\/ota\/pic\/side_2d_night_799\/side_right_rear\/",' offline_capture.json
    sed -i '6c"totol_pic_count": 799,' offline_capture.json
    cd /ota/ci/$1/config/postprocess
    sed -i '75a"disable_obstacle_tracking":true,' obstacle.json
    cd /ota/ci/$1
    ./startoffline.sh
    mv image_record/image_record_json/camera_fusion /ota/ci/result/benchmark/side_2d_night
    rm -r image_record
}

side_3d_case1(){
    echo "Execute side_3d_case1 Benchmark"
    cd /ota/ci/$1/config
    sed -i 's/"front_enable": true/"front_enable": false/g' app.json
    sed -i 's/"side_enable": false/"side_enable": true/g' app.json
    sed -i 's/"back_enable": true/"back_enable": false/g' app.json
    sed -i 's/"around_enable": true/"around_enable": false/g' app.json
    cd /ota/ci/$1/config/capture
    sed -i '29c"pic_dir": "\/ota\/pic\/side_3d_case1\/side_left_front\/",' offline_capture.json
    sed -i '36c"pic_dir": "\/ota\/pic\/side_3d_case1\/side_left_rear\/",' offline_capture.json
    sed -i '43c"pic_dir": "\/ota\/pic\/side_3d_case1\/side_right_front\/",' offline_capture.json
    sed -i '50c"pic_dir": "\/ota\/pic\/side_3d_case1\/side_right_rear\/",' offline_capture.json
    sed -i '6c"totol_pic_count": 1000,' offline_capture.json
    cd /ota/ci/$1
    ./startoffline.sh
    mv image_record/image_record_json/camera_fusion /ota/ci/result/benchmark/side_3d_case1
    rm -r image_record
}
side_3d_case2(){
    echo "Execute side_3d_case2 Benchmark"
    cd /ota/ci/$1/config
    sed -i 's/"front_enable": true/"front_enable": false/g' app.json
    sed -i 's/"side_enable": false/"side_enable": true/g' app.json
    sed -i 's/"back_enable": true/"back_enable": false/g' app.json
    sed -i 's/"around_enable": true/"around_enable": false/g' app.json
    cd /ota/ci/$1/config/capture
    sed -i '29c"pic_dir": "\/ota\/pic\/side_3d_case2\/side_left_front\/",' offline_capture.json
    sed -i '36c"pic_dir": "\/ota\/pic\/side_3d_case2\/side_left_rear\/",' offline_capture.json
    sed -i '43c"pic_dir": "\/ota\/pic\/side_3d_case2\/side_right_front\/",' offline_capture.json
    sed -i '50c"pic_dir": "\/ota\/pic\/side_3d_case2\/side_right_rear\/",' offline_capture.json
    sed -i '6c"totol_pic_count": 1000,' offline_capture.json
    cd /ota/ci/$1
    ./startoffline.sh
    mv image_record/image_record_json/camera_fusion /ota/ci/result/benchmark/side_3d_case2
    rm -r image_record
}

cipv_city(){
    echo "Execute cipv_city_2000 Benchmark"
    cd /ota/ci/$1/config
    sed -i 's/"front_enable": false/"front_enable": true/g' app.json
    sed -i 's/"side_enable": true/"side_enable": false/g' app.json
    sed -i 's/"back_enable": true/"back_enable": false/g' app.json
    sed -i 's/"around_enable": true/"around_enable": false/g' app.json
    cd /ota/ci/$1/config/capture
    sed -i '15c"pic_dir": "\/ota\/pic\/cipv_city_2000\/front_far\/",' offline_capture.json
    sed -i '22c"pic_dir": "\/ota\/pic\/cipv_city_2000\/front_near\/",' offline_capture.json
    sed -i '6c"totol_pic_count": 2000,' offline_capture.json    
    cd /ota/ci/$1
    ./startoffline.sh
    mv image_record/image_record_json/camera_fusion /ota/ci/result/benchmark/cipv_city
    rm -r image_record 
}

front_3d_city(){
    echo "Execute front_3d_city_2994 Benchmark"
    cd /ota/ci/$1/config
    sed -i 's/"front_enable": false/"front_enable": true/g' app.json
    sed -i 's/"side_enable": true/"side_enable": false/g' app.json
    sed -i 's/"back_enable": true/"back_enable": false/g' app.json
    sed -i 's/"around_enable": true/"around_enable": false/g' app.json
    cd /ota/ci/$1/config/capture
    sed -i '15c"pic_dir": "\/ota\/pic\/front_3d_city_2994\/front_far\/",' offline_capture.json
    sed -i '22c"pic_dir": "\/ota\/pic\/front_3d_city_2994\/front_near\/",' offline_capture.json
    sed -i '6c"totol_pic_count": 2994,' offline_capture.json
    cd /ota/ci/$1
    ./startoffline.sh
    mv image_record/image_record_json/camera_fusion /ota/ci/result/benchmark/front_3d_city
    rm -r image_record
}

cipv_highway(){
    echo "Execute cipv_highway_4000 Benchmark"
    cd /ota/ci/$1/config
    sed -i 's/"front_enable": false/"front_enable": true/g' app.json
    sed -i 's/"side_enable": true/"side_enable": false/g' app.json
    sed -i 's/"back_enable": true/"back_enable": false/g' app.json
    sed -i 's/"around_enable": true/"around_enable": false/g' app.json
    cd /ota/ci/$1/config/capture
    sed -i '15c"pic_dir": "\/ota\/pic\/cipv_highway_4000\/front_far\/",' offline_capture.json
    sed -i '22c"pic_dir": "\/ota\/pic\/cipv_highway_4000\/front_near\/",' offline_capture.json
    sed -i '6c"totol_pic_count": 4000,' offline_capture.json
    cd /ota/ci/$1/config/camera
    sed -i '11c"rot_y_beta": -0.45,' front_far.json
    cd /ota/ci/$1
    ./startoffline.sh
    mv image_record/image_record_json/camera_fusion /ota/ci/result/benchmark/cipv_highway
    rm -r image_record
}

front_3d_highway(){
    echo "Execute front_3d_highway_2680 Benchmark"
    cd /ota/ci/$1/config
    sed -i 's/"front_enable": false/"front_enable": true/g' app.json
    sed -i 's/"side_enable": true/"side_enable": false/g' app.json
    sed -i 's/"back_enable": true/"back_enable": false/g' app.json
    sed -i 's/"around_enable": true/"around_enable": false/g' app.json
    cd /ota/ci/$1/config/capture
    sed -i '15c"pic_dir": "\/ota\/pic\/front_3d_highway_2680\/front_far\/",' offline_capture.json
    sed -i '22c"pic_dir": "\/ota\/pic\/front_3d_highway_2680\/front_near\/",' offline_capture.json
    sed -i '6c"totol_pic_count": 2680,' offline_capture.json
    cd /ota/ci/$1/config/camera
    sed -i '11c"rot_y_beta": -0.45,' front_far.json
    cd /ota/ci/$1
    ./startoffline.sh
    mv image_record/image_record_json/camera_fusion /ota/ci/result/benchmark/front_3d_highway
    rm -r image_record
}

'''非连续帧benchmark运行
### front2d_roaduser'''
# front_2d_day_6278 $1
# front_2d_night_2027 $1
# front_k3_day_4674 $1
# front_k3_night_1804 $1
'''front_barrier'''
# front_barrier_day_1004 $1
# front_barrier_night_441 $1
'''TSR'''
# front_tsr_6532 $1
'''TL'''
front_tl_1000 $1
'''IHC'''
# ihc_day $1
# ihc_monight $1
# ihc_night $1
# ihc_no_obstacle $1
'''side_2d'''
# side_2d_day $1
# side_2d_night $1

'''连续帧benchmark运行
side_3d'''
# side_3d_case1 $1
# side_3d_case2 $1
'''front_3d'''
cipv_city $1
front_3d_city $1
cipv_highway $1
front_3d_highway $1