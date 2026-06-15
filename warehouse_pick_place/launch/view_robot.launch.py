from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution


def generate_launch_description():
    ur_type = "ur5e"
    packagepath = FindPackageShare("warehouse_pick_place")

    rvizconfig = PathJoinSubstitution([packagepath, 'rviz', 'default.rviz'])

    robot_description_content = Command([
        "xacro ",
        PathJoinSubstitution([
            FindPackageShare("ur_description"),
            "urdf",
            "ur.urdf.xacro"
        ]),
        " ",
        "ur_type:=", ur_type,
        " ",
        "name:=", "ur5e",
    ])

    robot_description = {
        "robot_description": robot_description_content
    }

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[robot_description],
        output="screen",
    )

    joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        output="screen",
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', rvizconfig],
        output="screen",
    )

    return LaunchDescription([
        robot_state_publisher,
        joint_state_publisher_gui,
        rviz,
    ])