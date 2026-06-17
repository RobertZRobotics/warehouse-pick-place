from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import Command, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.actions import AppendEnvironmentVariable
from launch_ros.substitutions import FindPackageShare
from launch.actions import TimerAction, ExecuteProcess
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    ur_type = "ur5e"

    ur_description_path = get_package_share_directory("ur_description")
    ur_description_parent = os.path.dirname(ur_description_path)

    gz_resource_path = AppendEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=ur_description_parent
    )

    world_file = PathJoinSubstitution([
        FindPackageShare("warehouse_pick_place"),
        "worlds",
        "empty_warehouse.sdf",
    ])

    robot_description_content = Command([
        "xacro ",
        PathJoinSubstitution([
            FindPackageShare("warehouse_pick_place"),
            "urdf",
            "ur5e_gz_control.xacro",
        ]),
        " ",
        "ur_type:=", ur_type,
        " ",
        "name:=", "ur5e",
    ])

    robot_description = {
        "robot_description": robot_description_content
    }

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("ros_gz_sim"),
                "launch",
                "gz_sim.launch.py",
            ])
        ),
        launch_arguments={
            "gz_args": ["-r ", world_file],
        }.items(),
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager", "/controller_manager",
        ],
        output="screen",
    )

    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "ur5e_arm_controller",
            "--controller-manager", "/controller_manager",
        ],
        output="screen",
    )

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
        ],
        output="screen",
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[robot_description, {"use_sim_time": True}],
        output="screen",
    )


    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-name", "ur5e",
            "-topic", "robot_description",
            "-x", "0.0",
            "-y", "0.0",
            "-z", "0.0",
        ],
        output="screen",
    )

    move_group = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("warehouse_pick_place_moveit_config"),
                "launch",
                "move_group.launch.py",
            ])
        ),
        launch_arguments={
            'use_sim_time': 'true',
        }.items(),
    )

    rviz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("warehouse_pick_place_moveit_config"),
                "launch",
                "moveit_rviz.launch.py",
            ])
        ),
        launch_arguments={
            'use_sim_time': 'true',
        }.items(),
    )

    spawn_box = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-name", "box1",
            "-file", PathJoinSubstitution([FindPackageShare("warehouse_pick_place"), "models", "small_box.sdf"]),
            "-x", "0.45",
            "-y", "0.0",
            "-z", "0.03",
        ],
        output="screen",
    )

    detach_box_initially = TimerAction(
    period=5.0,
    actions=[
        ExecuteProcess(
            cmd=[
                "gz", "topic",
                "-t", "/vacuum_gripper/detach",
                "-m", "gz.msgs.Empty",
                "-p", ""
            ],
            output="screen",
        )
    ],
    )

    attach_node = Node(
        package="warehouse_pick_place",
        executable="attach_box_node",
        output="screen",
    )

    return LaunchDescription([
        gz_resource_path,
        gz_sim,
        bridge,
        robot_state_publisher,
        spawn_robot,
        spawn_box,
        detach_box_initially,
        TimerAction(
            period=3.0,
            actions=[
                joint_state_broadcaster_spawner,
                arm_controller_spawner,
                move_group,
                rviz,
                attach_node
            ],
        ),
    ])