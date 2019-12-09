import rospy
import intera_interface
from sawyer_pykdl import sawyer_kinematics

#initialize node and variables for the sawyer arm and kinematics solver
rospy.init_node("ik")
limb = intera_interface.Limb('right')
kinematics = sawyer_kinematics('right')

#ensure gripper is open 
gripper = intera_interface.Gripper()
gripper.open()

#Get command to grab object (will I pinged from Liam?)
#Determine location
    #Plan B: use preset locations and navigate to option 1, 2, 3
    #to get positions: there is an object in a predetermined location, physically move arm to specific location, save joint angles

#go to object
obj_pos = [0.0, 0.0, 0.0]
obj_joint = kinematics.inverse_kinematics(obj_pos)
obj_dest = (zip(limb._joint_names, obj_joint))

#move arm to object
limb.move_to_joint_positions(dict(obj_dest))

#grasp object
gripper.close()

#move object along one axis
axis_pos = [0.0, 0.0, 0.5]
axis_joint = kinematics.inverse_kinematics(axis_pos)
axis_dest = (zip(limb._joint_names, axis_joint))

#move arm along one axis
limb.move_to_joint_positions(dict(axis_dest))

#open gripper to release object
gripper.open()
