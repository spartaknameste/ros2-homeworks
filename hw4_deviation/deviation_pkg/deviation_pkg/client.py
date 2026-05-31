import random

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from deviation_interfaces.action import ComputeDeviations


class DeviationActionClient(Node):
    def __init__(self):
        super().__init__('deviation_action_client')
        self.action_client = ActionClient(self, ComputeDeviations, 'compute_deviations')

    def send_goal(self, data):
        goal_msg = ComputeDeviations.Goal()
        goal_msg.data = data
        self.action_client.wait_for_server()
        self.get_logger().info(f'Sending data: {data}')
        send_goal_future = self.action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback)
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return
        self.get_logger().info('Goal accepted')
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Feedback deviation: {feedback_msg.feedback.deviation}')

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result deviations: {list(result.deviations)}')
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = DeviationActionClient()
    data = [round(random.uniform(0.0, 50.0), 1) for _ in range(6)]
    node.send_goal(data)
    rclpy.spin(node)


if __name__ == '__main__':
    main()
