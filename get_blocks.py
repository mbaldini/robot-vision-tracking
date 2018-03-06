from pixy import *
from ctypes import *
from flask import Flask
from flask import request

import time

# Import the Adafruit PCA9685 library
import Adafruit_PCA9685

# Initialise the PCA9685 using the default address (0x40).
PCA9685_pwm = Adafruit_PCA9685.PCA9685()

# Set frequency to 60hz, good for l298n h-bridge.
PCA9685_pwm.set_pwm_freq(60)

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

app = Flask(__name__)

@app.route("/")
def web_interface():
  html = open("index.html")
  response = html.read().replace('\n', '')
  html.close()
  return response

@app.route("/set_servo1")  
def set_servo1():  
  speed = request.args.get("speed")
  print "Received " + str(speed)
  PCA9685_pwm.set_pwm(0, 0, int(speed))
  return "Received " + str(speed)   
  
@app.route("/set_servo2")  
def set_servo2():  
  speed = request.args.get("speed")
  print "Received " + str(speed)
  PCA9685_pwm.set_pwm(1, 0, int(speed))  
  return "Received " + str(speed)  

@app.route("/set_servo3")  
def set_servo3():  
  speed = request.args.get("speed")
  print "Received " + str(speed)
  PCA9685_pwm.set_pwm(2, 0, int(speed))  
  return "Received " + str(speed) 

@app.route("/set_servo4")  
def set_servo4():  
  speed = request.args.get("speed")
  print "Received " + str(speed)
  PCA9685_pwm.set_pwm(3, 0, int(speed))  
  return "Received " + str(speed) 
 
@app.route("/set_servo5")  
def set_servo5():  
  speed = request.args.get("speed")
  print "Received " + str(speed)
  PCA9685_pwm.set_pwm(4, 0, int(speed))  
  return "Received " + str(speed) 

@app.route("/set_servo6")  
def set_servo6():  
  speed = request.args.get("speed")
  print "Received " + str(speed)
  PCA9685_pwm.set_pwm(5, 0, int(speed))  
  return "Received " + str(speed)   

def callback(ch, method, properties, body):
  body = json.loads(body)
  axis = None
  position = None
  
  if 'axis' in body['data']: axis = body['position']

  if 'position' in body['data']: position = body['position']

  if not axis: return
  if not position: return

  print('got axis %s, position %s' % (axis, position))

  PCA9685_pwm.set_pwm(axis, 0, position)

def get_center_offset(x, y, w, h):
  # 320 x 240 resolution
  # get center of screen
  cx_frame = 320 / 2
  cy_frame = 180 / 2

  # get the center of the block
  cx_block = (w / 2) + x
  cy_block = (h / 2) + y

  offset_x = (cx_frame - cx_block) / 10
  offset_y = (cy_frame - cy_block) / 10

  # if cx_frame > cx_block:
  #   offset_x = 1
  # elif cx_frame < cx_block:
  #   offset_x = -1
  
  # if cy_frame > cy_block:
  #   offset_y = 1
  # elif cy_frame < cy_block:
  #   offset_y = -1

  return [offset_x, offset_y]

class Blocks (Structure):
  _fields_ = [ ("type", c_uint),
               ("signature", c_uint),
               ("x", c_uint),
               ("y", c_uint),
               ("width", c_uint),
               ("height", c_uint),
               ("angle", c_uint) ]

if __name__ == "__main__":
  # app.run(host='0.0.0.0', port=8181, debug=True)
  
  # Initialize Pixy Interpreter thread #
  pixy_init()

blocks = BlockArray(10)
frame  = 0

axis_1_pos = 360
axis_6_pos = 390

# move to center position
PCA9685_pwm.set_pwm(0, 0, axis_1_pos)
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
      print 'offset x=%d y=%d' % (offset[0], offset[1])
      axis_1_pos += offset[0]
      axis_6_pos += offset[1]
      PCA9685_pwm.set_pwm(0, 0, axis_1_pos)
      PCA9685_pwm.set_pwm(5, 0, axis_6_pos)

    time.sleep(0.02)