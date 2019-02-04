#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from random import randint
from time import sleep

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + ": I heard " + data.data)
    distance = randint(5,10)
    mypub('approach_initiated')
    for i in range(distance):
        sleep(1)
        mypub('approach_ETA({})'.format(distance-i))
        rospy.loginfo(rospy.get_caller_id() + ": distance travelled {}{}".format("+"*i, "-"*(distance-i-1)))
    rospy.loginfo(rospy.get_caller_id() + ": simulated approach finished")
    mypub('approach_finished')

def mypub(message):
    rospy.loginfo(rospy.get_caller_id() + ": published message '" + message + "'.")
    pub.publish(message)

def run():
    rospy.init_node('robot')
    global pub
    pub = rospy.Publisher('robot_status', String, queue_size=10)
    rospy.Subscriber('robot_cmd', String, callback)
    while not rospy.is_shutdown():
        rospy.sleep(1)

if __name__ == '__main__':
    try:
        run()
    except rospy.ROSInterruptException:
        pass
