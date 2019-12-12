import rospy
import json
import copy
import time
import math
from geometry_msgs.msg import Pose2D
from std_msgs.msg import Float32MultiArray, Empty, String, Int16


# GLOBALS 
pose2d_sparki_odometry = None #Pose2D message object, contains x,y,theta members in meters and radians
#TODO: Track servo angle in radians
servo_angle = None
#TODO: Track IR sensor readings (there are five readings in the array: we've been using indices 1,2,3 for left/center/right)
ir_readings = None
## PART 3
#TODO: Create data structure to hold map representation
global world_map
world_map = {}
for i in range(50):
  world_map[i] = [0]*50 
# TODO: Use these variables to hold your publishers and subscribers
publisher_motor = None
publisher_odom = None
publisher_ping = None
publisher_servo = None
subscriber_odometry = None
subscriber_state = None
state_dict = {"light_sensors": [0,700,700,700,0], "ping": -1}
publisher_map = None

# CONSTANTS 
IR_THRESHOLD = 300 # IR sensor threshold for detecting black track. Change as necessary.
CYCLE_TIME = 0.1 # In seconds

def main():
  global publisher_motor, publisher_ping, publisher_servo, publisher_odom
  global IR_THRESHOLD, CYCLE_TIME
  global pose2d_sparki_odometry
  global world_map
  global state_dict
  #TODO: Init your node to register it with the ROS core
  rospy.init_node("Lab4")
  init()
  count = 0
  while not rospy.is_shutdown():
    #TODO: Implement CYCLE TIME
    start_cycle = time.time()
    #TODO: Implement line following code here
    #      To create a message for changing motor speed, use Float32MultiArray()
    #      (e.g., msg = Float32MultiArray()     msg.data = [1.0,1.0]      publisher.pub(msg))
    sensors = state_dict['light_sensors']
    if "ping" in state_dict:
      ping = state_dict["ping"]
    else:
      ping = -1
    servoMSG = Int16(80)
    publisher_servo.publish(servoMSG)
    
    #print(pose2d_sparki_odometry)
    ## adding code to set motor command based on light sensor data
    msg = Float32MultiArray()
    msg.data = [0,0.5]
    if sensors[1]<IR_THRESHOLD: #left sensor
      msg.data = [-1,1]
      
    if sensors[3]<IR_THRESHOLD: #right sensor
      msg.data = [1,-1]
      
    if sensors[2]<IR_THRESHOLD: #center sensor
      msg.data = [1,1]
    
      
    ##send message to sparki
    publisher_motor.publish(msg)
    
    publisher_ping.publish(Empty())
    if ping > 0:
      x_r,y_r = convert_ultrasonic_to_robot_coords(ping*100)
      x_w,y_w = convert_robot_coords_to_world(x_r, y_r)
      populate_map_from_ping(x_w, y_w)
      
    if count == 100:
      publisher_map.publish(Empty())
      display_map()
      print()
      print(pose2d_sparki_odometry)
      count = 0
    count+=1
    #TODO: Implement CYCLE TIME
    end_cycle = time.time()
    CYCLE_TIME = (end_cycle - start_cycle)*1000
    if CYCLE_TIME < 50:
      time.sleep((50-CYCLE_TIME)/1000)


def init():
  global publisher_motor, publisher_ping, publisher_servo, publisher_odom, publisher_map
  global subscriber_odometry, subscriber_state
  global pose2d_sparki_odometry
  #TODO: Set up your publishers and subscribers
  subscriber_state = rospy.Subscriber('/sparki/state', String, callback_update_state)
  publisher_motor = rospy.Publisher('/sparki/motor_command', Float32MultiArray, queue_size=10)#quesize might cause Issues
  subscriber_odometry = rospy.Subscriber('/sparki/odometry', Pose2D, callback_update_odometry)
  ## setting up the rest of the publishers and subscribers
  publisher_servo = rospy.Publisher('/sparki/set_servo', Int16, queue_size=10)
  publisher_odom = rospy.Publisher('/sparki/set_odometry', Pose2D, queue_size=10)
  publisher_ping = rospy.Publisher('/sparki/ping_command', Empty, queue_size=10)
  publisher_map = rospy.Publisher('/sparki/render_sim', Empty, queue_size=10)
  #TODO: Set up your initial odometry pose (pose2d_sparki_odometry) as a new Pose2D message object
  pose2d_sparki_odometry = Pose2D() 
  pose2d_sparki_odometry.x = 0.0
  pose2d_sparki_odometry.y = 0.0
  pose2d_sparki_odometry.theta = 0.0
  #TODO: Set sparki's servo to an angle pointing inward to the map (e.g., 45)
  servoMSG = Int16(80)
  publisher_servo.publish(servoMSG)
  
def callback_update_odometry(data):
  # Receives geometry_msgs/Pose2D message
  global pose2d_sparki_odometry
  #TODO: Copy this data into your local odometry variable
  pose2d_sparki_odometry = data

def callback_update_state(data):
  global state_dict
  state_dict = json.loads(data.data) # Creates a dictionary object from the JSON string received from the state topic
  #TODO: Load data into your program's local state variables

#PART 2.1
def convert_ultrasonic_to_robot_coords(x_us):
  #TODO: Using US sensor reading and servo angle, return value in robot-centric coordinates
  x_r, y_r = 0., 0.
  x_r = x_us * math.cos(1.39)
  y_r = x_us * math.sin(1.39)
  return x_r, y_r

#PART 2.2
def convert_robot_coords_to_world(x_r, y_r):
  #TODO: Using odometry, convert robot-centric coordinates into world coordinates
  x_w, y_w = 0., 0.
  x_w = (x_r * math.cos(pose2d_sparki_odometry.theta)) - (y_r * math.sin(pose2d_sparki_odometry.theta)) + (pose2d_sparki_odometry.x * 100)
  y_w = (x_r * math.sin(pose2d_sparki_odometry.theta)) + (y_r * math.cos(pose2d_sparki_odometry.theta)) + (pose2d_sparki_odometry.y*100)
  return x_w, y_w

def coords_to_map(x,y):
  i = math.floor(y/4)
  j = math.floor(x/4)
  #print(i,j)
  return int(i),int(j)

def map_to_coords(i,j):
  y = i*4
  x = j*4
  return x,y

#PART 3.4
def populate_map_from_ping(x_ping, y_ping):
  #TODO: Given world coordinates of an object detected via ping, fill in the corresponding part of the map
  global world_map
  i,j = coords_to_map(x_ping, y_ping)
  world_map[i][j] = 1
  

#PART 4.1
def display_map():
  #TODO: Display the map
  global world_map, pose2d_sparki_odometry
  sparki_posei, sparki_posej = coords_to_map(pose2d_sparki_odometry.x*100, pose2d_sparki_odometry.y*100)
  for i in range(35):
    for j in range(len(world_map[i])):
      if(sparki_posei == i and sparki_posej==j):
        print "<O",
      else:
        print world_map[i][j],
    print()

#PART 4.2a
def ij_to_cell_index(i,j):
  #TODO: Convert from i,j coordinates to a single integer that identifies a grid cell
  return i*200 + j

#PART 4.2b
def cell_index_to_ij(cell_index):
  #TODO: Convert from cell_index to (i,j) coordinates
  i = int(math.floor(cell_index))
  j = int(cell_index % 200)
  return i, j

#PART 4.2c
def cost(cell_index_from, cell_index_to):
  #TODO: Return cost of traversing from one cell to another
  i_to, j_to = cell_index_to_ij(cell_index_to)
  i_from, j_from = cell_index_to_ij(cell_index_from)
  check = abs(i_to-i_from)+abs(j_to-j_from)
  return 1 if check == 1 else 99

if __name__ == "__main__":
  main()

      