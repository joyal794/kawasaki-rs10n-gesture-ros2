# Kawasaki RS010N Gesture Control ROS 2 Project

This project simulates a Kawasaki RS010N industrial robot arm in ROS 2 using CAD STL mesh files, RViz visualization, smooth joint control, and webcam-based gesture commands.

## Final Working Status

The Kawasaki RS010N ROS 2 simulation is working with the full 6-axis CAD robot model.

### Completed Features

- Real Kawasaki RS010N CAD STL meshes loaded in RViz
- All 6 robot joints configured and working
- Correct joint origins measured from FreeCAD
- Smooth joint motion using `/joint_states`
- Gesture detector connected to robot motion
- Stable gesture commands published on `/gesture_command`
- Safety joint limits added for all 6 axes
- One-command full demo launch added
- GitHub repository created and updated

## Current Working Joints

```text
joint_1 ✅ Base rotation
joint_2 ✅ Shoulder rotation
joint_3 ✅ Elbow rotation
joint_4 ✅ Wrist rotation
joint_5 ✅ Wrist bend
joint_6 ✅ Tool flange rotation
Gesture Mapping
0 fingers / fist  → STOP
1 finger          → HOME
2 fingers         → PROCESS_1
3 fingers         → PROCESS_2
4 fingers         → PROCESS_3

The thumb is ignored in the latest gesture detector because thumb detection is less stable in webcam-based hand tracking.

## Workspace
rs10n_gesture_ws
## Main Packages
rs10n_description
rs10n_gesture_control
## Project Structure
rs10n_gesture_ws/
├── src/
│   ├── rs10n_description/
│   │   ├── launch/
│   │   │   ├── cad_moving_test.launch.py
│   │   │   ├── cad_robot_only.launch.py
│   │   │   └── full_gesture_demo.launch.py
│   │   ├── meshes/
│   │   │   ├── base.stl
│   │   │   ├── link_1.stl
│   │   │   ├── link_2.stl
│   │   │   ├── link_3.stl
│   │   │   ├── link_4.stl
│   │   │   ├── link_5.stl
│   │   │   └── link_6.stl
│   │   ├── urdf/
│   │   │   ├── rs10n_cad_moving.urdf.xacro
│   │   │   └── backup working URDF files
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
## Requirements
Ubuntu 22.04
ROS 2 Humble
RViz2
Python 3
OpenCV
MediaPipe
xacro
joint_state_publisher_gui

Install useful ROS tools:

sudo apt update
sudo apt install ros-humble-joint-state-publisher-gui ros-humble-xacro

Install Python dependencies if needed:

pip install opencv-python mediapipe
## Build
cd ~/rs10n_gesture_ws
colcon build
source install/setup.bash
## Final One-Command Demo

Use this command for the full gesture control demo:

cd ~/rs10n_gesture_ws
source install/setup.bash
ros2 launch rs10n_description full_gesture_demo.launch.py

This launches:

RViz
robot_state_publisher
joint_motion_node
gesture_detector_node
webcam gesture window
## Manual Demo Run

Use this method if you want to run each node separately.

## Terminal 1: CAD Robot in RViz
cd ~/rs10n_gesture_ws
source install/setup.bash
ros2 launch rs10n_description cad_robot_only.launch.py
## Terminal 2: Joint Motion Node
cd ~/rs10n_gesture_ws
source install/setup.bash
ros2 run rs10n_gesture_control joint_motion
## Terminal 3: Gesture Detector
cd ~/rs10n_gesture_ws
source install/setup.bash
ros2 run rs10n_gesture_control gesture_detector
## Important Launch Files
cad_moving_test.launch.py

Use this only for testing joints with sliders.

ros2 launch rs10n_description cad_moving_test.launch.py

This opens:

RViz
joint_state_publisher_gui
robot_state_publisher

Do not use this during gesture control testing because joint_state_publisher_gui also publishes /joint_states and can cause motion glitching.

cad_robot_only.launch.py

Use this for manual gesture/motion testing.

ros2 launch rs10n_description cad_robot_only.launch.py

This opens only:

RViz
robot_state_publisher
full_gesture_demo.launch.py

Use this for the final full demo.

ros2 launch rs10n_description full_gesture_demo.launch.py
## Test Commands Without Webcam

You can test robot movement manually using ROS topic commands.

ros2 topic pub /gesture_command std_msgs/msg/String "data: 'HOME'" --once
ros2 topic pub /gesture_command std_msgs/msg/String "data: 'PROCESS_1'" --once
ros2 topic pub /gesture_command std_msgs/msg/String "data: 'PROCESS_2'" --once
ros2 topic pub /gesture_command std_msgs/msg/String "data: 'PROCESS_3'" --once
ros2 topic pub /gesture_command std_msgs/msg/String "data: 'STOP'" --once
## Individual Joint Test Commands
ros2 topic pub /gesture_command std_msgs/msg/String "data: 'TEST_J1'" --once
ros2 topic pub /gesture_command std_msgs/msg/String "data: 'TEST_J2'" --once
ros2 topic pub /gesture_command std_msgs/msg/String "data: 'TEST_J3'" --once
ros2 topic pub /gesture_command std_msgs/msg/String "data: 'TEST_J4'" --once
ros2 topic pub /gesture_command std_msgs/msg/String "data: 'TEST_J5'" --once
ros2 topic pub /gesture_command std_msgs/msg/String "data: 'TEST_J6'" --once
## ROS Topics

Check topics:

ros2 topic list

Expected topics include:

/gesture_command
/joint_states
/robot_description
/tf
/tf_static
## Main ROS Topic Flow
gesture_detector_node
        ↓
/gesture_command
        ↓
joint_motion_node
        ↓
/joint_states
        ↓
robot_state_publisher
        ↓
RViz robot movement
## Safety Joint Limits

The motion controller clamps all target positions within Kawasaki RS010N-style joint limits:

joint_1: -180° to +180°
joint_2: -105° to +145°
joint_3: -163° to +150°
joint_4: -270° to +270°
joint_5: -145° to +145°
joint_6: -360° to +360°

This prevents unsafe target commands from exceeding the configured robot range.

## Notes

The original STEP CAD file is not included in this repository.

Only the exported STL mesh files used for ROS visualization are included.

The current URDF uses measured joint origins from FreeCAD for correct Kawasaki RS010N CAD alignment.

## GitHub Update Commands

Use these commands after future changes:

cd ~/rs10n_gesture_ws
git add .
git commit -m "Update robot model"
git pull --rebase origin main
git push
## Author

Joyal Nelson Chakkalakal
Msc.Robotics
