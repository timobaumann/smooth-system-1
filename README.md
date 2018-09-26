# A callable robot

This setup demonstrates a system in which a robot is called on ("come here"), executes an action (approach the caller), and confirms its action ("I am now with you").

The purpose of this demo system is to show the interaction of the dialog and robot components via ROS. Given this purpose, the robot is completely simulated and confirms that approach has finished after a while.

The information flow is as follows:

Startup
 → dialog is triggered by user request
 → dialog publishes action request
 → robot moves ; meanwhile, dialog waits for robot information
 → robot publishes completion of approach
 → dialog is triggered by completion of approach
 → dialog confirms completion to user via speech.

In this simulation, there is no robot and it does not move. The "robot" merely waits a random amount of time (5-10 seconds) and then confirms that it has completed the approach.

## DialogOS ROS nodes and topics

DialogOS may typically be visible as 2 ROS nodes during execution: 

* one ROS node that enables _running_ the dialog system itself (load dialog model, start dialog, abort dialog). The name of this node is `DialogOS_Control_Node` and it subscribes to the `DialogOS_cmd` topic.
* one ROS node that appears during execution of a dialog model and that enables the _interaction_ of dialog actions and other ROS components. The name of this node is `DialogOS_plugin`; the topics that it uses are determined by the dialog model.

It is possible to only run the dialog system via ROS but not have any ROS interactions within the dialog system (e.g. because the dialog does not involve any interaction with the remainder of the system). It is also possible to manually initiate the dialog via DialogOS and only have the dialog model interact with ROS (this may be simpler when testing out the dialog).

## Robot simulation

For the purpose of the setup, the robot will consist of a very simple ROS node. 
This node listens on the topic `robot_cmd` for the message `approach_user` and, 
upon reception of this message, waits a random amount of time (5-10 seconds) 
before sending on the topic `robot_status` the message `approach_finished`.

See `robotsim.py` for the simulation of the robot. 

For the system to work, please run `roscore` somewhere and also run `robotsim.py`.
(It is convenient these two on a local VM under Ubuntu 16.04 so that you can use any other operating system or a newer Ubuntu for your main system.)

## Startup

Startup (and hence the toplevel control) of the system can be performed in two ways: 

* DialogOS handles top level and a human operator initiates the system by starting the dialog; 
this mode is convenient for testing the dialog model.
* DialogOS is initiated from ROS via its own control topic, 
this is the fully integrated mode of operation.
When DialogOS is controlled via ROS, it does not show a graphical interface. 

### Startup via DialogOS:

Make sure `roscore` and `robotsim.py` are running and you have set 
`ROS_MASTER_URI`and `ROS_IP` so that our nodes can find ROS and communicate properly.

Start DialogOS in standalone mode by calling `.gradlew run` (`gradlew.bat` if you're on Windows).
On the first execution, this will download and build 
all the dependencies into the folder `build/` which may take some time.

A 

### Startup via ROS:

Make sure `roscore` and `robotsim.py` are running and you have set 
`ROS_MASTER_URI`and `ROS_IP` so that our nodes can find ROS and communicate properly.

Start DialogOS in ROS-control mode by calling `./gradlew runViaROS` (`gradlew.bat` if you're on Windows).
On the first execution, this will download and build 
all the dependencies into the folder `build/` which may take some time.

## DialogOS dialog model

Dialog models access ROS via specific DialogOS nodes, in particular `ROSOutputNode`s
for publishing messages onto arbitrary topics, and `ROSInputNode`s for receiving 
messages on arbitrary topics. Start up DialogOS 


