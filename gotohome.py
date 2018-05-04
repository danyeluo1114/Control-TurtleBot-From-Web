#!/usr/bin/env python

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Twist, Pose, Point, Quaternion
from std_msgs.msg import String
from sound_play.libsoundplay import SoundClient

class GoToHome():
    #define the constructor of the class
    def  __init__(self):
        #initialize the ROS node with a name voice_teleop
        rospy.init_node('go_to_home', anonymous=True)

 	self.goal_sent = False
	# What to do if shut down (e.g. Ctrl-C or failure)
	rospy.on_shutdown(self.shutdown)	
	# Tell the action client that we want to spin a thread by default
	self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
	rospy.loginfo("Wait for the action server to come up")

	# Allow up to 5 seconds for the action server to come up
	self.move_base.wait_for_server(rospy.Duration(5))

        # Publish the Twist message to the cmd_vel topic
        #self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        # Subscribe to the /gohome topic to receive 'go home'commands from the web page.
        rospy.Subscriber('/gohome', String, self.go_home_callback)

        #create a Rate object to sleep the process at 5 Hz
        #rate = rospy.Rate(5)

        # Initialize the Twist message we will publish.
        #self.cmd_vel = Twist()
        #make sure to make the robot stop by default
        #self.cmd_vel.linear.x=0;
        #self.cmd_vel.angular.z=0;



        # A mapping from keywords or phrases to commands
        #we consider the following simple commands, which you can extend on your own
        self.commands =             [
				'gohome'
                                ]
	
 	#self.voice = rospy.get_param("~voice", "voice_kal_diphone")
   	
	#Create the sound client object
	#self.soundhandel = SoundClient()
        #rospy.loginfo("Ready to receive voice commands")
        # We have to keep publishing the cmd_vel message if we want the robot to keep moving.
        #while not rospy.is_shutdown():
            #self.cmd_vel_pub.publish(self.cmd_vel)
            #rate.sleep()


    def go_home_callback(self, msg):
        # Get the motion command from the recognized phrase
        command = msg.data
        if (command in self.commands):
            if command == 'gohome':
                # Send a goal
        	self.goal_sent = True
		goal1 = MoveBaseGoal()
		goal1.target_pose.header.frame_id = 'map'
		goal1.target_pose.header.stamp = rospy.Time.now()
        	goal1.target_pose.pose = Pose(Point(-0.628, 0.536, 0.000),Quaternion(0.000, 0.000, 0.000, 1.000))

		# Start moving
        	self.move_base.send_goal(goal1)

		# Allow TurtleBot up to 60 seconds to complete task
		success = self.move_base.wait_for_result(rospy.Duration(60)) 

        	state = self.move_base.get_state()
        	result = False

        	if success and state == GoalStatus.SUCCEEDED:
            	# Achieved goal number#1!
            		self.goal_sent = False
        	else:
            		self.move_base.cancel_goal()
  
        else: #command not found
            #print 'command not found: '+command
            self.cmd_vel.linear.x = 0.0
            self.cmd_vel.angular.z = 0.0
        #print ("linear speed : " + str(self.cmd_vel.linear.x))
        #print ("angular speed: " + str(self.cmd_vel.angular.z))
    
    def shutdown(self):
        if self.goal_sent:
            self.move_base.cancel_goal()
        rospy.loginfo("Stop")
        rospy.sleep(1)

if __name__=="__main__":
    try:
      turtlebot = GoToHome()
      rospy.spin()
    except rospy.ROSInterruptException: pass
rospy.loginfo("Ctrl-C caught. Quitting")
