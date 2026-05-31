import random

import rclpy
from rclpy.node import Node
from operation_interfaces.srv import Operation


class OperationClient(Node):
    def __init__(self):
        super().__init__('operation_client')
        self.client = self.create_client(Operation, 'compute_operation')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for server...')
        self.timer = self.create_timer(2.0, self.send_request)

    def send_request(self):
        a = random.randint(0, 20)
        b = random.randint(0, 20)
        op = random.choice(['+', '-'])
        expr = f'{a}{op}{b}'
        request = Operation.Request()
        request.operation = expr
        future = self.client.call_async(request)
        future.add_done_callback(lambda f: self.handle_response(f, expr))

    def handle_response(self, future, expr):
        try:
            result = future.result().result
            self.get_logger().info(f'Sent: {expr} -> Received: {result}')
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = OperationClient()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
