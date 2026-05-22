import cv2
import mediapipe as mp

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class GestureDetectorNode(Node):
    def __init__(self):
        super().__init__('gesture_detector_node')

        # This topic is already used by your joint_motion_node
        self.publisher_ = self.create_publisher(String, '/gesture_command', 10)

        # MediaPipe hand detector
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        # Laptop webcam
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            self.get_logger().error('Could not open webcam.')
        else:
            self.get_logger().info('Webcam opened successfully.')

        # Used to avoid accidental commands
        self.last_command = "UNKNOWN"
        self.stable_count = 0

        # Run camera check every 0.1 second
        self.timer = self.create_timer(0.1, self.timer_callback)

    def count_fingers(self, hand_landmarks):
        """
        Counts how many fingers are open.
        0 fingers = fist
        1 finger  = HOME
        2 fingers = PROCESS_1
        3 fingers = PROCESS_2
        5 fingers = STOP
        """

        finger_tips = [4, 8, 12, 16, 20]
        fingers = []

        # Thumb check
        # This simple method may depend on left/right hand.
        if hand_landmarks.landmark[finger_tips[0]].x < hand_landmarks.landmark[finger_tips[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other 4 fingers
        # If fingertip is above middle joint, finger is open
        for tip in finger_tips[1:]:
            if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)

        return sum(fingers)

    def command_from_fingers(self, finger_count):
        if finger_count == 0:
            return "PAUSE"
        elif finger_count == 1:
            return "HOME"
        elif finger_count == 2:
            return "PROCESS_1"
        elif finger_count == 3:
            return "PROCESS_2"
        elif finger_count == 5:
            return "STOP"
        else:
            return "UNKNOWN"

    def publish_stable_command(self, command):
        """
        Publish command only if same gesture is detected several times.
        This prevents accidental robot movement.
        """

        if command == self.last_command:
            self.stable_count += 1
        else:
            self.stable_count = 0
            self.last_command = command

        # 5 stable frames = command accepted
        if self.stable_count == 5 and command != "UNKNOWN":
            msg = String()
            msg.data = command
            self.publisher_.publish(msg)
            self.get_logger().info(f'Published command: {command}')

    def timer_callback(self):
        ret, frame = self.cap.read()

        if not ret:
            self.get_logger().warn('Could not read webcam frame.')
            return

        # Mirror image, like selfie camera
        frame = cv2.flip(frame, 1)

        # Convert OpenCV BGR image to RGB for MediaPipe
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

        # Show text on camera window
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
            '0=PAUSE  1=HOME  2=P1  3=P2  5=STOP',
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.imshow('RS10N Gesture Control', frame)

        # Press q to quit webcam window
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
