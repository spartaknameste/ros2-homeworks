import time

import pytest
import rclpy
from rclpy.executors import SingleThreadedExecutor

from operation_pkg.server import OperationServer
from operation_interfaces.srv import Operation


@pytest.fixture(scope='module')
def ros_context():
    rclpy.init()
    yield
    rclpy.shutdown()


def call_service(operation):
    server = OperationServer()
    client_node = rclpy.create_node('test_service_client')
    client = client_node.create_client(Operation, 'compute_operation')

    executor = SingleThreadedExecutor()
    executor.add_node(server)
    executor.add_node(client_node)

    deadline = time.time() + 0.5
    while time.time() < deadline:
        executor.spin_once(timeout_sec=0.1)

    assert client.wait_for_service(timeout_sec=5.0)

    request = Operation.Request()
    request.operation = operation
    future = client.call_async(request)

    deadline = time.time() + 5.0
    while not future.done() and time.time() < deadline:
        executor.spin_once(timeout_sec=0.1)

    assert future.done()
    result = future.result().result

    server.destroy_node()
    client_node.destroy_node()
    return result


def test_addition(ros_context):
    assert call_service('7+3') == 10


def test_subtraction(ros_context):
    assert call_service('10-4') == 6
