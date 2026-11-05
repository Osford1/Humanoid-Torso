# Humanoid torso — single-motor MX-64T base plate

**One Dynamixel MX-64T turns the torso's base plate through a 5:1 gear pair; you type a plate angle and
it goes there.** This is the bench script I used to characterise the base joint: gear ratio, the
angle→tick conversion, and the multi-turn logic that stops the plate unwinding the long way round.

Lab script, not a library — no trajectory planner, no ROS node, no test suite.

## The interesting part: choosing the short way round

A plate angle repeats every 360°. The motor does not: it keeps counting past one revolution, so
"plate at 0°" is a different motor position every turn. The script reads the motor's present position,
converts it to degrees, then picks the integer `k` that puts the target nearest the current angle:

```python
motor_angle_desired_deg = plate_angle_deg * GEAR_RATIO
k = round((motor_angle_current_deg - motor_angle_desired_deg) / MOTOR_PERIOD_DEG)
motor_angle_target = motor_angle_desired_deg + k * MOTOR_PERIOD_DEG
```

`MOTOR_PERIOD_DEG` is one full plate revolution in motor degrees: 360° × 5 = 1800°. Without the `k`
term the plate takes the long way round and can run through the cable. With it, commanding 0° from 10°
moves 10° back, not 350° forward. That logic is `extended_position_control()` in `initialize.py`.

## Hardware

| Item | What I used |
| --- | --- |
| Motor | 1 × Dynamixel MX-64T, Protocol 2.0 |
| ID | 1 |
| Interface | U2D2 |
| Gears | 18-tooth pinion into a 90-tooth gear on the base plate (ratio 5.0) |
| Encoder | 4096 counts per motor revolution |
| Baud | 57600 |
| Port | `COM4` on my machine — change it |
| Gains | P 850, I 0, D 100, written to the motor at startup |

## Wiring

1. Bolt the MX-64T into the base plate mount (the mount has one index hole for the pinion).
2. Motor → U2D2, U2D2 → laptop.
3. Power the motor from its own supply.

## Run it

```bash
pip install dynamixel-sdk          # or install from ROBOTIS-GIT/DynamixelSDK/python
python basic_torso_control.py
```

Then:

1. it opens the port, enables torque and prints the current operating mode,
2. it **asks for an operating mode** — enter `4` (Extended Position Control), which is the mode
   multi-turn absolute positioning needs,
3. it prompts `Enter angle (0 - 360, -9999999 to exit)`; enter a plate angle in degrees,
4. it reads the present position, computes the nearest equivalent motor target, writes it, and polls
   the position every loop until the motor is within 10 counts of the target,
5. enter `-9999999` to exit; torque is disabled and the port closed.

```text
Enter angle (0 - 360, -9999999 to exit): 90
Enter angle (0 - 360, -9999999 to exit): 0
Enter angle (0 - 360, -9999999 to exit): -9999999
```

## Knobs

| Constant | File | Default | What it does |
| --- | --- | --- | --- |
| `DXL_ID` | `basic_torso_control.py` | 1 | motor ID |
| `BAUDRATE` | `basic_torso_control.py` | 57600 | bus speed |
| `DEVICENAME` | `basic_torso_control.py` | `"COM4"` | serial port (`/dev/ttyUSB0` on Linux) |
| `TEETH_SMALL`, `TEETH_LARGE` | `basic_torso_control.py` | 18, 90 | gear teeth; sets `GEAR_RATIO = 5.0` |
| `PLATE_PERIOD_DEG` | `basic_torso_control.py` | 360.0 | one plate revolution |
| `MOTOR_PERIOD_DEG` | `basic_torso_control.py` | 1800.0 | the same revolution in motor degrees |
| `COUNTS_PER_TURN` | `basic_torso_control.py` | 4096.0 | counts per motor revolution |
| `POSITION_P_GAIN` / `_I_` / `_D_` | `basic_torso_control.py` | 850 / 0 / 100 | written to the motor at startup through `init.setPosition_*_gain()` |
| `PROFILE_ACCELERATION` | `basic_torso_control.py` | 20 | ramp-up |
| `PROFILE_VELOCITY` | `basic_torso_control.py` | 200 | cruise speed |

Changing `TEETH_SMALL`/`TEETH_LARGE` is the one edit needed to retarget this at a different gear pair:
the ratio feeds both the angle conversion and the multi-turn period.

## Troubleshooting (errors I actually hit)

| Symptom | Cause | Fix |
| --- | --- | --- |
| `failed to open the port` | wrong COM number | check Device Manager / `ls /dev/ttyUSB*` |
| Motor holds but does not move | wrong operating mode | enter `4`; position mode (3) is single-turn |
| Plate takes the long way round | `MOTOR_PERIOD_DEG` does not match the real ratio | count the teeth and fix `TEETH_SMALL`/`TEETH_LARGE` |
| Motor buzzes or oscillates at the target | gains too stiff for the load | lower `POSITION_P_GAIN`; it is written to the motor at startup, so editing the constant is enough |
| Script never exits the wait loop | position stalled more than 10 counts away | the 10-count threshold is the tolerance in `extended_position_control()` |

## Status

Ran on the bench with the real mechanism. The script's loop is polling-based, so it prints a position
line per iteration; it was written to watch the joint settle, not to drive the robot. Next step was
feeding this from the robot's control layer instead of the terminal, which never happened in this file.

<!-- TODO(owner): no photo of the base plate and gear pair in the repo. Add one to docs/screenshots/ and
reference it here. -->

## Files

| File | Purpose |
| --- | --- |
| `basic_torso_control.py` | main script: setup, mode prompt, angle prompt, multi-turn target, motion wait |
| `initialize.py` | shared helpers: torque, operating mode, profiles, gains, position read, motion loop |

## Credits

Built for the University of Melbourne MSP humanoid's torso mechanism — the mechanism and gearing are
the team's, the control code here is mine. Servo API from
[ROBOTIS DynamixelSDK](https://github.com/ROBOTIS-GIT/DynamixelSDK) (Apache-2.0); control-table
addresses and the MX-64T page are from the [Robotis e-manual](https://emanual.robotis.com/docs/en/dxl/mx/mx-64-2/).

MIT — see `LICENSE`.
