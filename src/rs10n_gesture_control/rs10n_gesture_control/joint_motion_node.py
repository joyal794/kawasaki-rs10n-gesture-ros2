import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import JointState


class JointMotionNode(Node):
    def __init__(self):
        super().__init__('joint_motion_node')

        self.command_sub = self.create_subscription(
            String,
            '/gesture_command',
            self.command_callback,
            10
        )

        self.joint_pub = self.create_publisher(
            JointState,
            '/joint_states',
            10
        )

        self.joint_names = [
            'joint_1',
            'joint_2',
            'joint_3',
            'joint_4',
            'joint_5',
            'joint_6'
        ]

        self.current_positions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.target_positions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        # rad per update cycle
        self.motion_speed = 0.0015

        self.stopped = False
        self.paused = False

        self.timer = self.create_timer(0.02, self.update_motion)

        self.get_logger().info('Kawasaki RS010N joint motion node started')
        self.get_logger().info('Listening on /gesture_command')

    def deg(self, value):
        return math.radians(value)

    def set_target_deg(self, j1, j2, j3, j4, j5, j6, name):
        self.target_positions = [
            self.deg(j1),
            self.deg(j2),
            self.deg(j3),
            self.deg(j4),
            self.deg(j5),
            self.deg(j6)
        ]
        self.stopped = False
        self.paused = False
        self.get_logger().info(f'Moving to {name}: {[j1, j2, j3, j4, j5, j6]} deg')

    def command_callback(self, msg):
        command = msg.data.strip().upper()
        self.get_logger().info(f'Received command: {command}')

        if command == "HOME":
            self.set_target_deg(
                0, 0, 0, 0, 0, 0,
                "HOME"
            )

        elif command == "PROCESS_1":
            self.set_target_deg(
                30, 25, -35, 20, 30, 0,
                "PROCESS_1"
            )

        elif command == "PROCESS_2":
            self.set_target_deg(
                -35, 35, -25, -30, 25, 45,
                "PROCESS_2"
            )

        elif command == "PROCESS_3":
            self.set_target_deg(
                60, 15, -45, 90, -20, 120,
                "PROCESS_3"
            )

        elif command == "TEST_J1":
            self.set_target_deg(45, 0, 0, 0, 0, 0, "TEST_J1")

        elif command == "TEST_J2":
            self.set_target_deg(0, 45, 0, 0, 0, 0, "TEST_J2")

        elif command == "TEST_J3":
            self.set_target_deg(0, 0, 45, 0, 0, 0, "TEST_J3")

        elif command == "TEST_J4":
            self.set_target_deg(0, 0, 0, 90, 0, 0, "TEST_J4")

        elif command == "TEST_J5":
            self.set_target_deg(0, 0, 0, 0, 45, 0, "TEST_J5")

        elif command == "TEST_J6":
            self.set_target_deg(0, 0, 0, 0, 0, 180, "TEST_J6")

        elif command == "PAUSE":
            self.paused = True
            self.get_logger().warn('Robot PAUSED')

        elif command == "RESUME":
            self.paused = False
            self.stopped = False
            self.get_logger().info('Robot RESUMED')

        elif command == "STOP":
            self.stopped = True
            self.get_logger().error('Robot STOPPED')

        else:
            self.get_logger().warn(f'Unknown command ignored: {command}')

    def update_motion(self):
        if not self.stopped and not self.paused:
            for i in range(len(self.current_positions)):
                error = self.target_positions[i] - self.current_positions[i]

                if abs(error) > self.motion_speed:
                    self.current_positions[i] += self.motion_speed if error > 0 else -self.motion_speed
                else:
                    self.current_positions[i] = self.target_positions[i]

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
