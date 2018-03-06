from flask import Flask
from flask import request

import time
import pika

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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8181, debug=True)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.0.0.198'))
    
    channel = connection.channel()
    channel.exchange_declare(exchange='robot', exchange_type='fanout')
    
    queue = channel.queue_declare('commands').method.queue
    channel.queue_bind(exchange='robot', queue=queue, routing_key='*')
