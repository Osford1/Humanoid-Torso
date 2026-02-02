from dynamixel_sdk import *
import initialize as init

# Control table address
TORQUE_ENABLE_ADDRESS               = 64                          # Control table address is different in Dynamixel model
GOAL_POSITION_ADDRESS               = 116
PRESENT_POSITION_ADDRESS            = 132
OPERATING_MODE_ADDRESS              = 11
PROFILE_ACCELERATION_ADDRESS        = 108
PROFILE_VELOCITY_ADDRESS            = 112   

POSITION_P_GAIN_ADDRESS             = 84
POSITION_I_GAIN_ADDRESS             = 82
POSITION_D_GAIN_ADDRESS             = 80

# Protocol version
PROTOCOL_VERSION            = 2.0                             # See which protocol version is used in the Dynamixel

# Data setting
DXL_ID                      = 1                             # Dynamixel ID: 1
BAUDRATE                    = 57600
DEVICENAME                  = "COM4"       # Check which port is being used on your controller

# Other Constants
data                        = 1            # Data you want to write to the specified address
# gear constants
TEETH_SMALL                 = 18
TEETH_LARGE                 = 90

GEAR_RATIO                  = TEETH_LARGE/TEETH_SMALL

# PID Constants
POSITION_P_GAIN             = 850
POSITION_I_GAIN             = 0
POSITION_D_GAIN             = 100

# acceleration / velocity constants
PROFILE_ACCELERATION = 20           # to be changed 
PROFILE_VELOCITY     = 200

# angle constants

CENTER_POS = 0
COUNTS_PER_TURN = 4096.0
COUNTS_PER_DEGREE = COUNTS_PER_TURN/360.0        # the resolution
PLATE_PERIOD_DEG = 360.0
MOTOR_PERIOD_DEG = PLATE_PERIOD_DEG * GEAR_RATIO    # 360 * 5 = 1800


# initialize handler objects
portHandler = PortHandler("COM4")
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port and set Baud rate 
# exception handling, oepnPort and setBaudrate() functions returns a boolean value, it indicates success of failure
if portHandler.openPort():
    print("succeeded to open the port")
else: 
    print("failed to open the port")
    exit()    # exit if failed to open 

if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    exit()      # exit if failed to change the baudrate 


# Write data to enable torque
init.enable_Torque(packetHandler, portHandler, DXL_ID, TORQUE_ENABLE_ADDRESS, data)

# read the operating mode 
init.readOperatingMode(portHandler, DXL_ID, OPERATING_MODE_ADDRESS)

# Disable the torque 
packetHandler.write1ByteTxRx(portHandler, DXL_ID, TORQUE_ENABLE_ADDRESS, 0)
print("Disabling torque to set operating mode")

# set operating mode
init.setOperatingMode(portHandler, DXL_ID, OPERATING_MODE_ADDRESS)

# set acceleration profile
init.setAccelerationProfile(portHandler, DXL_ID, PROFILE_ACCELERATION_ADDRESS, PROFILE_ACCELERATION)

# set velocity profile
init.setVelocityProfile(portHandler, DXL_ID, PROFILE_VELOCITY_ADDRESS, PROFILE_VELOCITY)

print("Setting the motion profile (accel/velocity)")

# setting PID gains:
init.setPosition_P_gain(portHandler, DXL_ID, POSITION_P_GAIN_ADDRESS, POSITION_P_GAIN)
init.setPosition_I_gain(portHandler, DXL_ID, POSITION_I_GAIN_ADDRESS, POSITION_I_GAIN)
init.setPosition_D_gain(portHandler, DXL_ID, POSITION_D_GAIN_ADDRESS, POSITION_D_GAIN)

# Enabling torque
print("Enabling torque")
packetHandler.write1ByteTxRx(portHandler, DXL_ID, TORQUE_ENABLE_ADDRESS, 1)


'''POSITION CONTROL MODE '''
init.extended_position_control(packetHandler, portHandler, DXL_ID, PRESENT_POSITION_ADDRESS, COUNTS_PER_DEGREE, GEAR_RATIO, MOTOR_PERIOD_DEG, GOAL_POSITION_ADDRESS)

data = 0
packetHandler.write1ByteTxRx(portHandler, DXL_ID, TORQUE_ENABLE_ADDRESS, data)
portHandler.closePort()
