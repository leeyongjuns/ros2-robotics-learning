
import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class GoToGoal(Node):
    def __init__(self):
        super().__init__('go_to_goal')

        self.declare_parameter('goal_x', 5.5)
        self.declare_parameter('goal_y', 8.0)

        self.goal_x = self.get_parameter('goal_x').value
        self.goal_y = self.get_parameter('goal_y').value
        self.pose = None
        self.finished = False

        self.publisher_ = self.create_publisher(
            Twist, '/turtle1/cmd_vel', 10
        )

        self.subscription = self.create_subscription(
            Pose, '/turtle1/pose', self.pose_callback, 10
        )

        self.timer = self.create_timer(0.1, self.control_callback)

    def pose_callback(self, msg):
        self.pose = msg

    def control_callback(self):
        if self.pose is None or self.finished:
            return

        dx = self.goal_x - self.pose.x
        dy = self.goal_y - self.pose.y

        distance = math.sqrt(dx**2 + dy**2)
        target_angle = math.atan2(dy, dx)

        angle_error = target_angle - self.pose.theta
        angle_error = math.atan2(
            math.sin(angle_error),
            math.cos(angle_error)
        )

        cmd = Twist()

        if distance < 0.1:
            self.finished = True
            self.publisher_.publish(cmd)
            self.get_logger().info('Goal reached!')
            self.timer.cancel()
            return

        cmd.angular.z = max(-2.0, min(2.0, 4.0 * angle_error))

        if abs(angle_error) < 0.3:
            cmd.linear.x = min(1.5, 1.0 * distance)

        self.publisher_.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = GoToGoal()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.publisher_.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
