# Warehouse Pick and Place

A warehouse pick-and-place simulation built using ROS 2 Jazzy, Gazebo Harmonic, MoveIt 2, and ros2_control.

## Current Features

* UR5e manipulator simulated in Gazebo Harmonic
* Motion planning with MoveIt 2
* Trajectory execution through ros2_control
* Integrated RViz and Gazebo simulation
* Unified launch system for simulation and planning

## Project Goals

The long-term objective of this project is to develop a warehouse pick-and-place system capable of:

* Picking boxes using a vacuum gripper
* Detecting object locations with an overhead camera
* Planning collision-free motions
* Performing autonomous pick-and-place operations

## Requirements

* Ubuntu 24.04
* ROS 2 Jazzy
* Gazebo Harmonic

## Dependencies

Clone the Universal Robots ROS 2 description package into the same workspace:

```bash
cd ~/warehouse_ws/src
git clone -b jazzy https://github.com/UniversalRobots/Universal_Robots_ROS2_Description.git ur_description
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

* Gazebo simulation
* UR5e robot
* ros2_control
* MoveIt 2
* RViz

## Future Development

* Vacuum gripper
* Object spawning
* Object attachment
* Cartesian pick-and-place motions
* Overhead vision system
* Autonomous warehouse task execution
