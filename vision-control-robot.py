from pixy import *
from ctypes import *
from threading import Thread

import time
import sys

# Import the Adafruit PCA9685 library
import Adafruit_PCA9685

# Initialise the PCA9685 using the default address (0x40).
PCA9685_pwm = Adafruit_PCA9685.PCA9685()

# Set frequency to 60hz, good for l298n h-bridge.
PCA9685_pwm.set_pwm_freq(60)

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

track = False

def get_center_offset(x, y, w, h):
  # 320 x 180-ish resolution
  # get center of image
  cx_frame = 320 / 2
  cy_frame = 180 / 2

  # get the center of the block
  cx_block = (w / 2) + x
  cy_block = (h / 2) + y

  offset_x = (cx_frame - cx_block) / 10 # divide by 10 to slow it down a bit
  offset_y = (cy_frame - cy_block) / 10

  return [offset_x, offset_y]

class Blocks (Structure):
  _fields_ = [ ("type", c_uint),
               ("signature", c_uint),
               ("x", c_uint),
               ("y", c_uint),
               ("width", c_uint),
               ("height", c_uint),
               ("angle", c_uint) ]

def start_tracking():
  global track 
  track = False

  blocks = BlockArray(10)
  frame  = 0

  axis_1_pos = 360
  axis_6_pos = 390

  # move to center position
  PCA9685_pwm.set_pwm(0, 0, axis_1_pos)
  PCA9685_pwm.set_pwm(1, 0, 160)
  PCA9685_pwm.set_pwm(2, 0, 400)
  PCA9685_pwm.set_pwm(3, 0, 350)
  PCA9685_pwm.set_pwm(4, 0, 360)
  PCA9685_pwm.set_pwm(5, 0, axis_6_pos)

  # Wait for blocks #
  while 1:
    count = pixy_get_blocks(10, blocks)

    if count > 0:
      # Blocks found #
      frame = frame + 1
      largest_block = None
      for index in range (0, count):
        if largest_block is None:
          largest_block = blocks[index]
        elif largest_block.width * largest_block.height < blocks[index].width * blocks[index].height:
          largest_block = blocks[index]

      if largest_block is not None:
        offset = get_center_offset(blocks[index].x, blocks[index].y, blocks[index].width, blocks[index].height)
        axis_1_pos += offset[0]
        axis_6_pos += offset[1]
        PCA9685_pwm.set_pwm(0, 0, axis_1_pos)
        PCA9685_pwm.set_pwm(5, 0, axis_6_pos)

    time.sleep(0.05)

if __name__ == "__main__":

  try:
    pixy_init()
    start_tracking()
  except KeyboardInterrupt, SystemExit:
    PCA9685_pwm.set_pwm(0, 0, 375)
    PCA9685_pwm.set_pwm(1, 0, 160)
    PCA9685_pwm.set_pwm(2, 0, 500)
    sys.exit()