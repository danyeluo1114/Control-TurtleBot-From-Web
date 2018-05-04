# Control-TurtleBot-From-Web
CIS693_Group1_FinalProject

All command lines needed:

roslaunch LuoD gotodoor_bringup.launch
 
roslaunch LuoD usb_cam-test.launch --screen

rosrun web_video_server web_video_server

rosrun robot_pose_publisher robot_pose_publisher

roslaunch rosbridge_server rosbridge_websocket.launch

roslaunch LuoD gotodoor_navigation.launch

Then open the html file.
