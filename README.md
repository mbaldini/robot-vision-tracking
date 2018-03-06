# 6-Axis-Desktop-Robotic-Arm-Raspberry-Pi
This 6-Axis desktop robotic arm is paired with a CMUCam5 Pixy to do basic object tracking using color-based filtering based on the [6-Axis-Desktop-Robotic-Arm-Raspberry-Pi](https://github.com/custom-build-robots/6-Axis-Desktop-Robotic-Arm-Raspberry-Pi) project by [custom-build-robots](https://github.com/custom-build-robots).

![SainSmart 6 axis robotic arm](https://custom-build-robots.com/wp-content/uploads/2017/11/SainSmart_6_axis_desktop_robotic_arm-300x200.jpg)

## Step by Step guide
First follow the setup guide in [custom-build-robots](https://github.com/custom-build-robots)'s blog at: https://custom-build-robots.com/raspberry-pi-robot-cars/sainsmart-6-axis-desktop-robotic-arm-raspberry-pi/9497?lang=en

Next follow the [Hooking up Pixy to Raspberry Pi](http://www.cmucam.org/projects/cmucam5/wiki/Hooking_up_Pixy_to_a_Raspberry_Pi) guide over at the CMUCam5 Pixy blog.

Now you can clone this repository using
```
git clone https://github.com/mbaldini/robot-vision-tracking.git
```

You can now run the application by navigating into the robot-vision-tracking project folder and executing the command:
```
sudo python vision-control-robot.py
```

I have also updated the original web interface from custom-build-robots to allow for easy gamepad control using the HTML5 Gamepad API. You can try this one out by running:
```
sudo python control-robot.py
```

The gamepad controls are setup for an xbox controller, using the two joypads and the trigger/bumper buttons to control movement.

Be sure to follow the CMUCam5's guidelines on how to train the Pixy. I used Pixymon on windows to train the original image.
