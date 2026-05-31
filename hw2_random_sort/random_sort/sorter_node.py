import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, Int32MultiArray


class SorterNode(Node):

    def __init__(self):
        super().__init__('sorter_node')
        self.numbers = []
        self.subscription = self.create_subscription(
            Int32, 'random_number', self.number_callback, 10)
        self.publisher_ = self.create_publisher(
            Int32MultiArray, 'sorted_array', 10)
        self.get_logger().info('Sorter node started')

    def number_callback(self, msg):
        self.numbers.append(msg.data)
        self.numbers.sort()

        out = Int32MultiArray()
        out.data = list(self.numbers)
        self.publisher_.publish(out)

        self.get_logger().info(f'Received: {msg.data} -> Sorted: {self.numbers}')


def main(args=None):
    rclpy.init(args=args)
    node = SorterNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
