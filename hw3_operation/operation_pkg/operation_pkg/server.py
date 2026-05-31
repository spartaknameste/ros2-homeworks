import re

import rclpy
from rclpy.node import Node
from operation_interfaces.srv import Operation


class OperationServer(Node):
    def __init__(self):
        super().__init__('operation_server')
        self.srv = self.create_service(Operation, 'compute_operation', self.handle_request)
        self.get_logger().info('Operation server ready')

    def handle_request(self, request, response):
        expr = request.operation.replace(' ', '')
        match = re.match(r'^(-?\d+)([+-])(-?\d+)$', expr)
        if match:
            a = int(match.group(1))
            op = match.group(2)
            b = int(match.group(3))
            response.result = a + b if op == '+' else a - b
        else:
            response.result = 0
            self.get_logger().warn(f'Invalid expression: {request.operation}')
        self.get_logger().info(f'{request.operation} = {response.result}')
        return response


def main(args=None):
    rclpy.init(args=args)
    node = OperationServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
