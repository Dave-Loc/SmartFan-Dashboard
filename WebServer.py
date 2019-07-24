from flask import Flask, render_template, request
from sense_hat import SenseHat
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import RPi.GPIO as GPIO
import json
import time

#New flask object named app
app = Flask(__name__)

#New motorkit object called kit
kit = MotorKit()

#New sensehat object called sense
sense = SenseHat()
sense.clear()

#utlogo
blue = (0, 0 ,104)
gold = (255, 215, 0)

sense.set_pixel(0, 0, blue)
sense.set_pixel(1, 0, blue)
sense.set_pixel(2, 0, blue)
sense.set_pixel(3, 0, blue)
sense.set_pixel(4, 0, blue)
sense.set_pixel(5, 0, blue)
sense.set_pixel(6, 0, blue)
sense.set_pixel(7, 0, blue)
sense.set_pixel(1, 1, blue)
sense.set_pixel(1, 2, blue)
sense.set_pixel(1, 3, blue)
sense.set_pixel(1, 4, blue)
sense.set_pixel(1, 5, blue)
sense.set_pixel(1, 6, blue)
sense.set_pixel(1, 7, blue)
sense.set_pixel(2, 1, blue)
sense.set_pixel(2, 6, blue)
sense.set_pixel(2, 7, blue)
sense.set_pixel(3, 1, blue)
sense.set_pixel(4, 1, blue)
sense.set_pixel(3, 3, blue)
sense.set_pixel(3, 4, blue)
sense.set_pixel(3, 5, blue)
sense.set_pixel(3, 6, blue)
sense.set_pixel(3, 7, blue)
sense.set_pixel(4, 3, blue)
sense.set_pixel(4, 4, blue)
sense.set_pixel(4, 5, blue)
sense.set_pixel(4, 6, blue)
sense.set_pixel(4, 7, blue)
sense.set_pixel(5, 1, blue)
sense.set_pixel(5, 3, blue)
sense.set_pixel(5, 4, blue)
sense.set_pixel(5, 6, blue)
sense.set_pixel(5, 7, blue)
sense.set_pixel(6, 0, blue)
sense.set_pixel(6, 1, blue)
sense.set_pixel(6, 2, blue)
sense.set_pixel(6, 3, blue)
sense.set_pixel(6, 4, blue)
sense.set_pixel(6, 5, blue)
sense.set_pixel(6, 6, blue)
sense.set_pixel(6, 7, blue)
sense.set_pixel(7, 0, blue)
sense.set_pixel(7, 1, blue)
sense.set_pixel(7, 2, blue)
sense.set_pixel(7, 3, blue)
sense.set_pixel(7, 4, blue)
sense.set_pixel(7, 5, blue)
sense.set_pixel(7, 6, blue)
sense.set_pixel(7, 7, blue)

sense.set_pixel(0, 1, gold)
sense.set_pixel(0, 2, gold)
sense.set_pixel(0, 3, gold)
sense.set_pixel(0, 4, gold)
sense.set_pixel(0, 5, gold)
sense.set_pixel(0, 6, blue)
sense.set_pixel(0, 7, blue)
sense.set_pixel(1, 5, gold)
sense.set_pixel(2, 1, gold)
sense.set_pixel(2, 2, gold)
sense.set_pixel(2, 3, gold)
sense.set_pixel(2, 4, gold)
sense.set_pixel(2, 5, gold)
sense.set_pixel(3, 2, gold)
sense.set_pixel(4, 2, gold)
sense.set_pixel(5, 2, gold)
sense.set_pixel(6, 2, gold)
sense.set_pixel(7, 2, gold)
sense.set_pixel(5, 3, gold)
sense.set_pixel(5, 4, gold)
sense.set_pixel(5, 5, gold)
sense.set_pixel(5, 6, gold)

#Defining GPIO number system to Broadcom
GPIO.setmode(GPIO.BCM)

#Setting up GPIO pin 18 (Not Board Number), pin 18 is hardware PWM
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.HIGH)

#declaring pwm global variable, 25000 is 25Khz frequency
pwm = GPIO.PWM(18, 25000)

#Defining function for converting temperature to fahrenheit
def to_fahrenheit(celcius):
    return ((celcius/5)*9)+32

#Oscillation Power
global oscillation
oscillation = False

#Function for modifyind duty cycle/fan speed
def ChangeFanSpeed(FanDutyCycle):
    pwm.ChangeDutyCycle(FanDutyCycle)
    return str(FanDutyCycle)
    
def ChangeFanRotation(startstep, endstep):
    print(oscillation)
    while True:
        for i in range(16 * startstep, 16 * endstep):
            kit.stepper1.onestep(style=stepper.MICROSTEP, direction=stepper.FORWARD)
            #time.sleep(0.05)
        for i in range(16 * startstep, 16 * endstep):
            kit.stepper1.onestep(style=stepper.MICROSTEP, direction=stepper.BACKWARD)
            #time.sleep(0.05)
            
#Routing for web root directory
@app.route('/')
def index():
        #Retrieving sense hat temperature data
        temp = sense.get_temperature()
        #Converting temperature data to fahrenheit
        temp = to_fahrenheit(temp)
        #Rounding temperature data to 1 decimal place
        temp = round(temp, 1)
        #Retrieving sense hat humidity data
        humid = sense.get_humidity()
        #Rounding sense hat humidity data to 1 decimal place
        humid = round(humid, 1)
        #Retrieving sense hat pressure data
        press = sense.get_pressure()
        #Rounding sense hat pressure data to 1 decimal place
        press = round(press, 1)
        #Read temperature data into web template
        sensorData = {
        'temp' : temp,
        'humid' : humid,
        'press' : press
        }
        return render_template(('index.html'), **sensorData)

@app.route('/GetWebFanDutyCycle', methods=['GET','POST'])
def GetWebFanDutyCycle():
    FanDutyCycle = int(request.form['FanDutyCycle'])
    return ChangeFanSpeed(FanDutyCycle)
    
@app.route('/GetWebFanRotation', methods=['GET','POST'])
def GetWebFanRotation():
    FanRotation = str(request.form['FanRotation'])
    startstep, endstep = FanRotation.split(";")
    ChangeFanRotation(int(startstep), int(endstep))
    return FanRotation
    
@app.route('/FanSpeedOn', methods=['GET','POST'])
#Function for turning PWM fan speed control on
def FanSpeedOn():
    #Duty cycle is variable square wave that can be set from 0 to 100
    #0 duty cycle is 0% and 100 duty cycle is 100%, or full strength
    pwm.start(100)
    return "Fan Turned On"

@app.route('/FanSpeedOff', methods=['GET','POST'])
def FanSpeedOff():
    pwm.start(0)
    return "Fan Turned Off"
    
@app.route('/FanRotationOn', methods=['GET','POST'])
def FanRotationOn():
    oscillation = True
    print(oscillation)
    return "Fan Oscillation On"
    
@app.route('/FanRotationOff', methods=['GET','POST'])
def FanRotationOff():
    oscillation = False
    print(oscillation)
    kit.stepper1.release()
    return "Fan Oscillation Off"
    
    
if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
