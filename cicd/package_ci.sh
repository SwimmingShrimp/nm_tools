#!/bin/bash

function build()
{
    echo "start build"
    ./scripts/build.sh -p aarch64 -o qnx -v 7.1.0 -r release
}

function copy_files()
{
    project_root_path=$1
    pack_name=$2

    echo "project_root_path :$project_root_path"
    echo "pack_name :$pack_name"

    #copy bin
    mkdir -p $pack_name/bin
    cp $project_root_path/build_out/release/aarch64_qnx/bin/sensor_camera_orin $pack_name/bin/sensor_camera_orin
    cp $project_root_path/build_out/release/aarch64_qnx/bin/sensor_camera_orin_offline $pack_name/bin/sensor_camera_orin_offline
    cp $project_root_path/build_out/release/aarch64_qnx/bin/nvcapture_image_saver $pack_name/bin/nvcapture_image_saver

    #copy lib
    mkdir -p $pack_name/lib/opencv
    cp -d $project_root_path/thirdparty/dbow2/lib/aarch64-qnx/*.so* $pack_name/lib/
    cp -d $project_root_path/thirdparty/opencv/lib/aarch64-qnx/*.so* $pack_name/lib/opencv/
    cp -d $project_root_path/thirdparty/nullmax/lib/aarch64-qnx/*.so* $pack_name/lib/
    cp -d $project_root_path/thirdparty/protobuf/lib/aarch64-qnx/*.so* $pack_name/lib/
    cp -d $project_root_path/thirdparty/spdlog/lib/aarch64-qnx/*.so* $pack_name/lib/
    cp -d $project_root_path/thirdparty/ceres/lib/aarch64-qnx/*.so* $pack_name/lib/
    cp -d $project_root_path/thirdparty/opengv/lib/aarch64-qnx/*.so* $pack_name/lib/

    #copy config
    cp -r $project_root_path/config $pack_name/
    cp -r $project_root_path/model $pack_name/
    cp -r $project_root_path/package_info/source_pic/ $pack_name/
    cp -r $project_root_path/package_info/ReleaseNote.txt $pack_name/
    cp -r $project_root_path/package_info/readme.md $pack_name/
    cp -r $project_root_path/package_info/start.sh $pack_name/
    cp -r $project_root_path/package_info/startoffline.sh $pack_name/
    cp -r $project_root_path/package_info/camera_config/* $pack_name/config/
}

function update_config()
{
    package_dir=$1
    #sed -i 's/\/dat\/model/model/g' $package_dir/config/model/model.json
    #sed -i 's/10.10.9.255/172.16.1.255/g' $package_dir/config/ipc/ipc.json
}

cur_path=`pwd`
project_root_path=${cur_path%scripts}
package_dir=$1

echo "Start packing perception:$package_dir"

build

copy_files $project_root_path $package_dir

update_config $package_dir

zip -ry "$package_dir.zip" $package_dir

echo "Package perception finished:$package_dir"
