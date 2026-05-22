import cv2
import mediapipe as mp

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class GestureDetectorNode(Node):
    def __init__(self):
        super().__init__('gesture_detector_node')

        self.publisher_ = self.create_publisher(String, '/gesture_command', 10)

        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            self.get_logger().error('Could not open webcam.')
        else:
            self.get_logger().info('Webcam opened successfully.')

        self.last_detected_command = "UNKNOWN"
        self.last_published_command = "UNKNOWN"
        self.stable_count = 0

        # Command must be stable for these many frames
        self.required_stable_frames = 8

        self.timer = self.create_timer(0.1, self.timer_callback)

        self.get_logger().info('Gesture detector started.')
        self.get_logger().info('Publishing commands to /gesture_command')

    def count_fingers(self, hand_landmarks):
        finger_tips = [4, 8, 12, 16, 20]
        fingers = []

        # Thumb
        if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # Index, middle, ring, pinky
        for tip in finger_tips[1:]:
            if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)

        return sum(fingers)

    def command_from_fingers(self, finger_count):
        if finger_count == 0:
            return "STOP"
        elif finger_count == 1:
            return "HOME"
        elif finger_count == 2:
            return "PROCESS_1"
        elif finger_count == 3:
            return "PROCESS_2"
        elif finger_count == 4:
            return "PROCESS_3"
        elif finger_count == 5:
            return "PAUSE"
        else:
            return "UNKNOWN"

    def publish_stable_command(self, command):
        if command == "UNKNOWN":
            self.stable_count = 0
            self.last_detected_command = "UNKNOWN"
            return

        if command == self.last_detected_command:
            self.stable_count += 1
        else:
            self.stable_count = 1
            self.last_detected_command = command

        if self.stable_count >= self.required_stable_frames:
            if command != self.last_published_command:
                msg = String()
                msg.data = command
                self.publisher_.publish(msg)

                self.last_published_command = command
                self.get_logger().info(f'Published command: {command}')

    def timer_callback(self):
        ret, frame = self.cap.read()

        if not ret:
            self.get_logger().warn('Could not read webcam frame.')
            return

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = self.hands.process(rgb_frame)

        command = "UNKNOWN"
        finger_count = 0

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

                finger_count = self.count_fingers(hand_landmarks)
                command = self.command_from_fingers(finger_count)

        self.publish_stable_command(command)

        cv2.putText(
            frame,
            f'Fingers: {finger_count}  Command: {command}',
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            '0=STOP  1=HOME  2=P1  3=P2  4=P3  5=PAUSE',
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

        cv2.imshow('RS10N Gesture Control', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.get_logger().info('Closing gesture detector.')
            self.cap.release()
            cv2.destroyAllWindows()
            rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = GestureDetectorNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    if node.cap.isOpened():
        node.cap.release()

    cv2.destroyAllWindows()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
