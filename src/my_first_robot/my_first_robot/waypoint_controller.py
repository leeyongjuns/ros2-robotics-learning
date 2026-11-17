
import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class WaypointController(Node):
    def __init__(self):
        super().__init__('waypoint_controller')

        self.waypoints = [
            (3.0, 3.0),
            (8.0, 3.0),
            (8.0, 8.0),
            (3.0, 8.0),
        ]

        self.index = 0
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

        goal_x, goal_y = self.waypoints[self.index]

        dx = goal_x - self.pose.x
        dy = goal_y - self.pose.y

        distance = math.hypot(dx, dy)

        if distance < 0.1:
            self.publisher_.publish(Twist())
            self.index += 1

            self.get_logger().info(
                f'Waypoint {self.index} reached!'
            )

            if self.index >= len(self.waypoints):
                self.finished = True
                self.timer.cancel()
                self.get_logger().info('All waypoints reached!')

            return

        target_angle = math.atan2(dy, dx)

        angle_error = math.atan2(
            math.sin(target_angle - self.pose.theta),
            math.cos(target_angle - self.pose.theta)
        )
        self.get_logger().info(
            f'Waypoint {self.index + 1} | '
            f'Distance: {distance:.3f} | '
            f'Angle error: {angle_error:.3f}'
        )
        cmd = Twist()

        cmd.angular.z = max(-2.0, min(2.0, 4.0 * angle_error))

        if abs(angle_error) < 0.3:
            cmd.linear.x = min(1.5, distance)

        self.publisher_.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = WaypointController()

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
