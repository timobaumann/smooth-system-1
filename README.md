# A callable robot

This setup demonstrates a system in which a robot is called on ("come here"), 
executes an action (approach the caller), performs some (semi-incremental) 
dialog while the action is going on, and confirms its action once it is 
informed about the completion ("I am now with you").

The purpose of this demo system is to show the interaction of the dialog and 
robot components via ROS. Given this purpose, the robot is completely simulated, 
periodically sends messages about the expected remaining duration of the action 
and eventually confirms that approach has finished.

The information flow is as follows:

Startup
 → dialog is triggered by user request ("robot, come here")
 → dialog publishes action request
 → robot moves ; meanwhile, dialog waits for robot information
 → robot publishes expectation of remaining time
 → if time remains to talk about some topic, the dialog system talks about this
 → the above two points repeat
 → eventually, robot publishes completion of approach
 → dialog is triggered by completion of approach
 → dialog confirms completion to user via speech.

In this simulation, there is no robot and it does not move. The "robot" merely 
waits a random amount of time (5-10 seconds), sends updates every second and 
then confirms that it has completed the approach.

## DialogOS ROS nodes and topics

DialogOS may typically be visible as 2 ROS nodes during execution: 

* one ROS node that _enables running_ the dialog system itself (load dialog 
model, start dialog, abort dialog). The name of this node is `DialogOS_Control` 
and it subscribes to the `DialogOS_cmd` topic.
* one ROS node that appears _during execution_ of a dialog model and that 
enables the interaction of dialog actions and other ROS components. The name 
of this node is `DialogOS_plugin`; the topics that it uses are determined by 
the dialog model.

It is possible to only run the dialog system via ROS but not have any 
ROS interactions within the dialog system (e.g. because the dialog does not 
involve any interaction with the remainder of the system). It is also possible 
to manually initiate the dialog via DialogOS and only have the dialog model 
interact with ROS (this may be simpler when testing and refining the dialog).

## Robot simulation

For the purpose of the setup, the robot will consist of a very simple ROS node. 
This node listens on the topic `robot_cmd` for the message `approach_user` and, 
upon reception of this message, waits for a random amount of time (5-10 seconds) 
before sending on the topic `robot_status` the message `approach_finished`.

See `robotsim.py` for the simulation of the robot. 

For the system to work, please run `roscore` somewhere and also run `robotsim.py`.
(It is convenient to run these two on a local VM under Ubuntu 16.04 so that 
you can use any other operating system or an uptodate Ubuntu for your main system.)

## Startup

Startup (and hence the toplevel control) of the system can be performed in two ways: 

* DialogOS handles top level and a human operator initiates the system by selecting
the dialog model and starting the dialog via the graphical interface; 
this mode is convenient for testing the dialog model. 
In this case, `DialogOS_control` is not started.
* DialogOS is initiated from ROS via its own control topic, 
this is the fully integrated mode of operation.
When DialogOS is controlled via ROS, it does not show a graphical interface
_unless_ you instruct it to do so via the java property `dialogos.showGUI`.

### Startup via DialogOS:

Make sure `roscore` and `robotsim.py` are running and you have set 
`ROS_MASTER_URI`and `ROS_IP` so that our nodes can find ROS and communicate properly.

Start DialogOS in standalone mode by calling `.gradlew run` (`gradlew.bat` if you're on Windows).
On the first execution, this will download and build 
all the dependencies into the folder `build/` which may take some time.

Using the graphical interface, open the dialog model `model.dos` into DialogOS.
As you will see, the dialog consists of the (linear) flow outlined at the top:
once started, the system listens for "robot come here", sends a message to ROS,
waits for the response (that should arrive within 5-10 seconds) and answers "I'm here now."

Click on the _start_ button to execute this dialog. 

### Startup via ROS:

Make sure `roscore` and `robotsim.py` are running and you have set 
`ROS_MASTER_URI`and `ROS_IP` so that our nodes can find ROS and communicate properly.

Start DialogOS in ROS-control mode by calling `./gradlew runViaROS` (`gradlew.bat` if you're on Windows).
On the first execution, this will download and build 
all the dependencies into the folder `build/` which may take some time.

DialogOS needs to be instructed to load a dialog model first, then instructed 
to start the dialog (similarly to what we did via GUI in standalone mode).

We will use `rostopic` to issue commands to ROS. These could of course also 
be generated based on robot perception.

* `rostopic pub /DialogOS_cmd std_msgs/String "LOAD model.dos"`; press Ctrl-C.
* notice that the terminal running DialogOS shows some status messages about 
loading the model; once finished:
* `rostopic pub /DialogOS_cmd std_msgs/String "START"`
* say "robot come here", hear "I'm here now." after a while.
* you can re-start once the dialog is finished. 
* it may be instructive to listen in on the relevant topics (`/robot_cmd` and `/robot_status`)
via `rostopic echo`.

## DialogOS dialog model

Dialog models access ROS via specific DialogOS nodes, in particular 
`ROSOutputNode`s for publishing messages onto arbitrary topics, and 
`ROSInputNode`s for receiving messages on arbitrary topics. Our simple example 
first uses one output node and later uses an input node. The input is received 
into variable. Notice that we don't actually check the content of the input -- 
this should be done for a more complete example, using DialogOS-Script.


