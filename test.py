import rospy
import intera_interface
from sawyer_pykdl import sawyer_kinematics

#possible imports to get gripper to work
import argparse
import intera_external_devices
#so far: failed to get gripper working


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

#xyz_pos needs to be a 3D array
pos = [0.1, 0.1, 0.1]
joint = kinematics.inverse_kinematics(pos)

dest = (zip(limb._joint_names, joint))
#move arm to object
limb.move_to_joint_positions(dict(dest))

#grasp object
gripper.close()

#bring object to specific predetermined location
end_pos = [0, 0, 0]
end_dest = dict(zip(limb._joint_names, kinematics.inverse_kinematics(end_pos)))

#move arm to final destination
limb.move_to_joint_positions(dict(end_dest))

#send confirmation (who am I sending to?)

