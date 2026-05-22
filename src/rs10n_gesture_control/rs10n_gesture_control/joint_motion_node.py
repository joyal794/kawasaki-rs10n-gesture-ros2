import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import JointState


class JointMotionNode(Node):
    def __init__(self):
        super().__init__('joint_motion_node')

        # Listen for gesture/process commands
        self.command_sub = self.create_subscription(
            String,
            '/gesture_command',
            self.command_callback,
            10
        )

        # Publish joint positions to RViz
        self.joint_pub = self.create_publisher(
            JointState,
            '/joint_states',
            10
        )

        # These names must match your URDF joint names
        self.joint_names = [
            'joint_1',
            'joint_2',
            'joint_3',
            'joint_4',
            'joint_5',
            'joint_6'
        ]

        # Current robot position
        self.current_positions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        # Target robot position
        self.target_positions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        # Movement speed
        self.motion_speed = 0.02

        self.stopped = False
        self.paused = False

        # Timer updates robot movement every 0.02 second
        self.timer = self.create_timer(0.02, self.update_motion)

        self.get_logger().info('Joint motion node started.')
        self.get_logger().info('Waiting for commands on /gesture_command')

    def deg(self, value):
        return math.radians(value)

    def command_callback(self, msg):
        command = msg.data
        self.get_logger().info(f'Received command: {command}')

        if command == "HOME":
            self.target_positions = [
                self.deg(0),
                self.deg(0),
                self.deg(0),
                self.deg(0),
                self.deg(0),
                self.deg(0)
            ]
            self.stopped = False
            self.paused = False
            self.get_logger().info('Moving to HOME')

        elif command == "PROCESS_1":
            self.target_positions = [
                self.deg(30),
                self.deg(25),
                self.deg(-35),
                self.deg(20),
                self.deg(30),
                self.deg(0)
            ]
            self.stopped = False
            self.paused = False
            self.get_logger().info('Moving to PROCESS_1')

        elif command == "PROCESS_2":
            self.target_positions = [
                self.deg(-35),
                self.deg(35),
                self.deg(-25),
                self.deg(-20),
                self.deg(25),
                self.deg(45)
            ]
            self.stopped = False
            self.paused = False
            self.get_logger().info('Moving to PROCESS_2')

        elif command == "PAUSE":
            self.paused = True
            self.get_logger().warn('Robot PAUSED')

        elif command == "STOP":
            self.stopped = True
            self.get_logger().error('Robot STOPPED')

        else:
            self.get_logger().warn('Unknown command ignored')

    def update_motion(self):
        # Move slowly toward target position
        if not self.stopped and not self.paused:
            for i in range(len(self.current_positions)):
                error = self.target_positions[i] - self.current_positions[i]

                if abs(error) > self.motion_speed:
                    if error > 0:
                        self.current_positions[i] += self.motion_speed
                    else:
                        self.current_positions[i] -= self.motion_speed
                else:
                    self.current_positions[i] = self.target_positions[i]

        # Publish joint states
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names
        msg.position = self.current_positions

        self.joint_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = JointMotionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
