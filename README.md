# Kawasaki RS010N Gesture Control ROS 2 Project
Main Packages
rs10n_description
rs10n_gesture_control
Project Structure
rs10n_gesture_ws/
├── src/
│   ├── rs10n_description/
│   │   ├── launch/
│   │   ├── meshes/
│   │   │   ├── base.stl
│   │   │   ├── link_1.stl
│   │   │   ├── link_2.stl
│   │   │   ├── link_3.stl
│   │   │   ├── link_4.stl
│   │   │   ├── link_5.stl
│   │   │   └── link_6.stl
│   │   ├── urdf/
│   │   └── package.xml
│   │
│   └── rs10n_gesture_control/
│       ├── rs10n_gesture_control/
│       │   ├── gesture_detector_node.py
│       │   └── joint_motion_node.py
│       ├── package.xml
│       └── setup.py
│
├── README.md
└── .gitignore
Requirements
Ubuntu 22.04
ROS 2 Humble
RViz2
joint_state_publisher_gui
Python 3

Install useful ROS tools:

sudo apt update
sudo apt install ros-humble-joint-state-publisher-gui ros-humble-xacro
Build
cd ~/rs10n_gesture_ws
colcon build
source install/setup.bash
Run CAD Moving Test
cd ~/rs10n_gesture_ws
source install/setup.bash
ros2 launch rs10n_description cad_moving_test.launch.py

This opens RViz and Joint State Publisher GUI.

Current working joints:

joint_1 ✅
joint_2 ✅
joint_3 ✅
joint_4 fixed
joint_5 fixed
joint_6 fixed
Run Robot Only Launch
cd ~/rs10n_gesture_ws
source install/setup.bash
ros2 launch rs10n_description robot_only.launch.py
Run Gesture Control

Terminal 1:

cd ~/rs10n_gesture_ws
source install/setup.bash
ros2 launch rs10n_description robot_only.launch.py

Terminal 2:

cd ~/rs10n_gesture_ws
source install/setup.bash
ros2 run rs10n_gesture_control joint_motion

Terminal 3:

cd ~/rs10n_gesture_ws
source install/setup.bash
ros2 run rs10n_gesture_control gesture_detector
Check ROS Topics
ros2 topic list

Expected topics may include:

/joint_states
/robot_description
/tf
/tf_static
Notes

The original STEP CAD file is not included in this repository.

Only the exported STL mesh files used for ROS visualization are included.

The current URDF uses measured joint origins from FreeCAD for correct Kawasaki RS010N CAD alignment.

GitHub Update Commands

Use these commands after future changes:

cd ~/rs10n_gesture_ws
git add .
git commit -m "Update robot model"
git push
Author

Joyal Nelson
