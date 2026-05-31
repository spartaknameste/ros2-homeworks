import random

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class NumberPublisher(Node):

    def __init__(self):
        super().__init__('number_publisher')
        self.publisher_ = self.create_publisher(Int32, 'random_number', 10)
        self.timer = self.create_timer(1.0, self.publish_number)
        self.get_logger().info('Number publisher started')

    def publish_number(self):
        msg = Int32()
        msg.data = random.randint(1, 100) 
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = NumberPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
