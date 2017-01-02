#!/bin/bash -xve

apt get install ros-indigo-cv-bridge

#sync and make
rsync -av ./ ~/catkin_ws/src/pimouse_vision_control/

#clone pimouse_ros
cd ~/catkin_ws/src/
git clone https://github.com/citueda/pimouse_ros.git

cd ~/catkin_ws
catkin_make
