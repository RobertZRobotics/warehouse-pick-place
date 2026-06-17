#!/usr/bin/env python3

import subprocess

import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool


class AttachBoxNode(Node):
    def __init__(self):
        super().__init__("attach_box_node")

        self.attach_topic = "/vacuum_gripper/attach"
        self.detach_topic = "/vacuum_gripper/detach"

        self.srv = self.create_service(
            SetBool,
            "set_box_attached",
            self.set_box_attached_callback,
        )

        self.get_logger().info("Attach box node ready.")
        self.get_logger().info("Call /set_box_attached true to attach, false to detach.")

    def publish_gz_empty(self, topic):
        result = subprocess.run(
            [
                "gz", "topic",
                "-t", topic,
                "-m", "gz.msgs.Empty",
                "-p", "",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            self.get_logger().error(
                f"Failed to publish to {topic}: {result.stderr.strip()}"
            )
            return False

        return True

    def set_box_attached_callback(self, request, response):
        if request.data:
            success = self.publish_gz_empty(self.attach_topic)

            response.success = success
            response.message = "Box attached." if success else "Failed to attach box."

            if success:
                self.get_logger().info("Box attached.")

        else:
            success = self.publish_gz_empty(self.detach_topic)

            response.success = success
            response.message = "Box detached." if success else "Failed to detach box."

            if success:
                self.get_logger().info("Box detached.")

        return response


def main(args=None):
    rclpy.init(args=args)
    node = AttachBoxNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()