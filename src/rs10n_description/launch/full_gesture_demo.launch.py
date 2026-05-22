from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution


def generate_launch_description():
    urdf_file = PathJoinSubstitution([
        FindPackageShare('rs10n_description'),
        'urdf',
        'rs10n_cad_moving.urdf.xacro'
    ])

    robot_description = {
        'robot_description': Command(['xacro ', urdf_file])
    }

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[robot_description],
        output='screen'
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen'
    )

    joint_motion = Node(
        package='rs10n_gesture_control',
        executable='joint_motion',
        name='joint_motion_node',
        output='screen'
    )

    gesture_detector = Node(
        package='rs10n_gesture_control',
        executable='gesture_detector',
        name='gesture_detector_node',
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher,
        rviz,
        joint_motion,
        gesture_detector
    ])
