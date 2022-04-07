# import libraries 
import RPi.GPIO as gpio
import time
from picamera import PiCamera


# set pin mapping to BOARD
gpio.setmode(gpio.BOARD)
# turn off channel warnings messages
gpio.setwarnings(False)
# Set GPIO pins as output
gpio.setup(7,gpio.OUT)
gpio.setup(10,gpio.OUT)
GPIO_TRIGGER = 36
GPIO_ECHO = 37

# set GPIO pins as inputs
leftSensor = 15
rightSensor = 16
gpio.setup(leftSensor,gpio.IN)
gpio.setup(rightSensor,gpio.IN)
gpio.setup(GPIO_TRIGGER, gpio.OUT)
gpio.setup(GPIO_ECHO, gpio.IN)

def startAll():
    gpio.output(7,1)
    gpio.output(10,1)

# turn on left motor
def leftOn():
    gpio.output(7,1)
    
# turn off left motor
def leftOff():
    gpio.output(7,0)
  
# turn on right motor
def rightOn():
    gpio.output(10,1)

#turn off right motor
def rightOff():
    gpio.output(10,0)

# turn off all motors
def stopAll():
    gpio.output(10,0)
    gpio.output(7,0)

def distance():
    # set Trigger to HIGH
    gpio.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    gpio.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while gpio.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while gpio.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

camera = PiCamera()
time.sleep(2)
camera.resolution = (640, 480)
camera.vflip = False
camera.contrast = 10
file_name = "/home/pi/Videos/video_" + str(time.time()) + ".h264"

# main program loop

stopAll()   # make sure all pin are set to off

x = input()


#if __name__ == '__main__':
if x == 'm':
    try:
        camera.start_recording(file_name)
        while True:
            camera.wait_recording()
            dist = distance()
            # if left and right sensors are off stop both motors
            if gpio.input(leftSensor)== 1 and gpio.input(rightSensor) == 1:  
                stopAll()
                
            # if both sensors are on then turn both motors on
            if gpio.input(leftSensor)== 0 and gpio.input(rightSensor)==0:
                startAll()
                
            # if left sensor is on turn right motor off (pivot left)
            if gpio.input(leftSensor)==0 and gpio.input(rightSensor)==1:
                leftOn()
                rightOff()
                
            # if right sensor is on turn left motor off (pivot right)
            if gpio.input(leftSensor)==1 and gpio.input(rightSensor)==0:
                leftOff()
                rightOn()
                
            if dist < 15:
                stopAll()

                
            
    except KeyboardInterrupt:
        print("Stop")                
        gpio.cleanup()
        
    finally:
        print("End")
        gpio.cleanup()
        camera.stop_recording()