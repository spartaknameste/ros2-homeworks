import time

import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from deviation_interfaces.action import ComputeDeviations


class DeviationActionServer(Node):
    def __init__(self):
        super().__init__('deviation_action_server')
        self.action_server = ActionServer(
            self,
            ComputeDeviations,
            'compute_deviations',
            self.execute_callback)
        self.get_logger().info('Deviation action server ready')

    def execute_callback(self, goal_handle):
        data = list(goal_handle.request.data)
        self.get_logger().info(f'Received data: {data}')

        mean = sum(data) / len(data) if data else 0.0
        self.get_logger().info(f'Mean: {mean}')

        deviations = []
        feedback_msg = ComputeDeviations.Feedback()
        for value in data:
            deviation = value - mean
            deviations.append(deviation)
            feedback_msg.deviation = deviation
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f'Feedback deviation: {deviation}')
            time.sleep(0.5)

        goal_handle.succeed()
        result = ComputeDeviations.Result()
        result.deviations = deviations
        self.get_logger().info(f'Result: {deviations}')
        return result


def main(args=None):
    rclpy.init(args=args)
    node = DeviationActionServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
