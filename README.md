# Warehouse Pick and Place

A warehouse pick-and-place simulation built using ROS 2 Jazzy, Gazebo Harmonic, MoveIt 2, and ros2_control.

## Current Features

* UR5e manipulator simulated in Gazebo Harmonic
* Motion planning with MoveIt 2
* Trajectory execution through ros2_control
* Custom vacuum gripper end effector
* Spawnable warehouse box model
* Vacuum attach/detach using Gazebo DetachableJoint
* Integrated RViz and Gazebo simulation
* Unified launch system for simulation and planning

## Project Goals

The long-term objective of this project is to develop an autonomous warehouse pick-and-place system capable of:

* Picking boxes using a vacuum gripper
* Detecting object locations with an overhead camera
* Planning collision-free motions
* Performing autonomous pick-and-place operations

## Requirements

* Ubuntu 24.04
* ROS 2 Jazzy
* Gazebo Harmonic
* MoveIt 2

## Dependencies

Create a ROS 2 workspace if necessary and clone the Universal Robots ROS 2 description package:

```bash
mkdir -p ~/warehouse_ws/src
cd ~/warehouse_ws/src
git clone -b jazzy https://github.com/UniversalRobots/Universal_Robots_ROS2_Description.git ur_description
cd ..
colcon build
```

## Installation

Clone this repository into the same workspace:

```bash
cd ~/warehouse_ws/src
git clone https://github.com/RobertZRobotics/warehouse-pick-place
```

Build the workspace:

```bash
cd ~/warehouse_ws
colcon build
source install/setup.bash
```

## Running

Launch the complete simulation:

```bash
ros2 launch warehouse_pick_place sim.launch.py
```

This launches:

* Gazebo Harmonic
* UR5e robot
* Vacuum gripper
* Warehouse box
* ros2_control
* MoveIt 2
* RViz
* Vacuum attach/detach interface

## Vacuum Gripper Control

The simulation includes a vacuum gripper with attach and detach functionality.

The gripper can currently be controlled through the provided ROS service:

```bash
ros2 service call /set_box_attached std_srvs/srv/SetBool "{data: true}"
```

Attach the box.

```bash
ros2 service call /set_box_attached std_srvs/srv/SetBool "{data: false}"
```

Release the box.

## Future Development

* Automatic vacuum engagement
* Hard-coded pick-and-place sequence
* Multiple warehouse boxes
* Overhead vision system
* Object pose estimation
* Autonomous pick-and-place operations
* Dynamic warehouse task generation
