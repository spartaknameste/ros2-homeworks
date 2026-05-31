import time

import pytest
import rclpy
from rclpy.action import ActionClient
from rclpy.executors import SingleThreadedExecutor

from deviation_pkg.server import DeviationActionServer
from deviation_interfaces.action import ComputeDeviations


@pytest.fixture(scope='module')
def ros_context():
    rclpy.init()
    yield
    rclpy.shutdown()


def test_action_computes_deviations(ros_context):
    server = DeviationActionServer()
    client_node = rclpy.create_node('test_action_client')
    action_client = ActionClient(client_node, ComputeDeviations, 'compute_deviations')

    executor = SingleThreadedExecutor()
    executor.add_node(server)
    executor.add_node(client_node)

    deadline = time.time() + 0.5
    while time.time() < deadline:
        executor.spin_once(timeout_sec=0.1)

    assert action_client.wait_for_server(timeout_sec=5.0)

    feedback = []
    goal = ComputeDeviations.Goal()
    goal.data = [2.0, 4.0, 6.0]
    send_future = action_client.send_goal_async(
        goal, feedback_callback=lambda fb: feedback.append(fb.feedback.deviation))

    deadline = time.time() + 5.0
    while not send_future.done() and time.time() < deadline:
        executor.spin_once(timeout_sec=0.1)

    goal_handle = send_future.result()
    assert goal_handle.accepted

    result_future = goal_handle.get_result_async()
    deadline = time.time() + 10.0
    while not result_future.done() and time.time() < deadline:
        executor.spin_once(timeout_sec=0.1)

    deadline = time.time() + 1.0
    while time.time() < deadline:
        executor.spin_once(timeout_sec=0.1)

    assert result_future.done()
    result = result_future.result().result
    assert list(result.deviations) == pytest.approx([-2.0, 0.0, 2.0])
    assert len(feedback) == 3

    server.destroy_node()
    client_node.destroy_node()
