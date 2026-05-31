import time

import pytest
import rclpy
from rclpy.executors import SingleThreadedExecutor
from std_msgs.msg import Int32, Int32MultiArray

from random_sort.sorter_node import SorterNode


@pytest.fixture(scope='module')
def ros_context():
    rclpy.init()
    yield
    rclpy.shutdown()


def test_sorter_publishes_sorted_array(ros_context):
    sorter = SorterNode()
    test_node = rclpy.create_node('test_topic_node')
    publisher = test_node.create_publisher(Int32, 'random_number', 10)

    received = []
    test_node.create_subscription(
        Int32MultiArray, 'sorted_array',
        lambda msg: received.append(list(msg.data)), 10)

    executor = SingleThreadedExecutor()
    executor.add_node(sorter)
    executor.add_node(test_node)

    deadline = time.time() + 1.0
    while time.time() < deadline:
        executor.spin_once(timeout_sec=0.1)

    for value in [5, 1, 3, 2, 4]:
        msg = Int32()
        msg.data = value
        publisher.publish(msg)
        deadline = time.time() + 0.5
        while time.time() < deadline:
            executor.spin_once(timeout_sec=0.1)

    assert received
    last = received[-1]
    assert last == sorted(last)
    assert set(last) == {1, 2, 3, 4, 5}

    sorter.destroy_node()
    test_node.destroy_node()
