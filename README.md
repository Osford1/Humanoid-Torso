# Torso control
The torso is driven by one dynamixel MX-64T motor. It is connected to the base of the torso via 2 gears. Gear ratio 5:1. 

Steps to move torso:
1. Attach dynamixel to base if not already done (there should be hole indicating where its supposed to be)
2. Connect the dynamixel to the U2D2
3. Connect U2D2 to computer/jetson
4. Run code

## Code explanation and what not 
### Setup
1. Ensure python3 is installed 
    https://www.python.org/downloads/
2. Download Dynamixel SDK (source code from github)
```
$ git clone https://github.com/ROBOTIS-GIT/DynamixelSDK.git

```
3. Build and install the SDK 
- Open the {$Dynamixel_SDK}/python folder
- Right click on the folder an select open in terminal
- Build and install Dynamixel_SDK through below command
``` $pip install . ```
- Check whether pip recognizes the SDK by running
``` $pip show dynamixel_sdk ```

### basic_torso_control.py
This is the main code used to control the dynamixel driving the base plate. 

#### how it works when you run it :
```python basic_torso_control.py ```
- It will first print out a bunch of stuff indicating whether connections are successful or what not. 
- Then it will print out the current operating mode of the motor
- Then it will ask you for a number to set the operating mode (I done this incase we want to use other modes in the future), input 4 in the terminal for extended position control 
- If no issues, it will ask for angles in the terminal, input the angle you want the base plate to be at (0-360), the code will convert the plate angle to motor angle to raw goal intepreted by the motor 
- Thats it, this code just manually turns the plate at a desired angle, in the future will connect this to more code to respond to sound/requests

### explanation
At the top we imported the sdk library and also the python file initialize.py (this is just a file that contains all the functions used in basic_torso_control.py)

The meat of the code is essentially just us sending instruction packets to the Motor via the U2D2 and receiving status packets from the motor through to the U2D2.

We mainly do these using functions:
``` write1ByteTxRx(), write2ByteTxRx(), write4ByteTxRx() ```
Where Tx - Transmit, Rx - receive, these are methods within the PacketHandler class. Heres a link to the documentation:
https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/api_reference/python/python_packethandler/#python-packethandler

#### Constants:
We first have the control table addresses, we use these addresses to write and read packets to and from the motor. You can find the addresses for any motor by searching up the motor model, and looking at the control table given. For the motor used in torso: https://emanual.robotis.com/docs/en/dxl/mx/mx-64-2/


Alternatively you can connect the motor to your computer via the dynamixel wizard 2.0 app, and observe through there.

The protocol version and data settings can be found the same way.

Gear constants:
- TEETH_SMALL - the number of teeth on the small gear (attached to the motor)
- TEETH_LARGE - the number of teeth on the large gear (attach to the bottom of the base plate)

Gear ratio:
- The gear ratio between the two gears

PID Constants:
- POSITION_P_GAIN - the P gain value we are using
- POSITION_I_GAIN - the I gain value we are using
- POSITION_D_GAIN - the D gain value we are using

Acceleration and velocity constants:
- Profile acceleration - the acceleration value we set, higher means higher acceleration, max value is 32767
- Profile velocty - the velocity value we set, higher means faster average velocity, max is 2047

Angle constants: constants used to map motor angle to base plate angle
- CENTER_POS - the middle position (0)
- COUNTS_PER_TURN - the max raw data value
- COUNTS_PER_DEGREE - the resolution
- MOTOR_PERIOD_DEG - convert angle from plate to motor angle via gear ratio 

There rest of the code should be pretty easy to understand. We essentially just use a bunch of methods from library after initialising the packet and port handler objects. 
