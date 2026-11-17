
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class MotionSequence(Node):
    def __init__(self):
        super().__init__('motion_sequence')

        self.publisher_ = self.create_publisher(
            Twist, '/turtle1/cmd_vel', 10
        )

        self.count = 0
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = Twist()

        if self.count < 3:
            msg.linear.x = 0.2
            action = 'Moving forward'

        elif self.count < 6:
            msg.angular.z = 0.5
            action = 'Turning left'

        else:
            action = 'Stopping'
            self.timer.cancel()

        self.publisher_.publish(msg)
        self.get_logger().info(action)

        self.count += 1


def main(args=None):
    rclpy.init(args=args)
    node = MotionSequence()

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
