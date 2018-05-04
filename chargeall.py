#!/usr/bin/env python

import rospy
import roslaunch

class GoCharge():
    def __init__(self):
	rospy.init_node('go_charge', anonymous=True)
	rospy.on_shutdown(self.shutdown)

	uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
	roslaunch.configure_logging(uuid)
	launch1 = roslaunch.parent.ROSLaunchParent(uuid, ["/home/dluo/catkin_ws/src/LuoD/Launch/kobuki_auto_docking_minimal.launch"])

	launch1.start()

	launch2 = roslaunch.parent.ROSLaunchParent(uuid, ["/home/dluo/catkin_ws/src/LuoD/Launch/kobuki_auto_docking_activate.launch"])

	launch2.start()

	#launch.shutdown()

    def shutdown(self):
        rospy.loginfo("Stop")
        rospy.sleep(1)

if __name__=="__main__":
    try:
     	turtlebot = GoCharge()
      	rospy.spin()
    except rospy.ROSInterruptException: pass
rospy.loginfo("Ctrl-C caught. Quitting")
