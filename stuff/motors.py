import RPi.GPIO as GPIO
from helpers import setServo, setServoPCA9685, setMotor, getSumOfInputs

class Motor(object):
    
    def __init__(self, pinEN, pin1, pin2, inputs):
        self.pinEN = pinEN
        self.pin1 = pin1
        self.pin2 = pin2
        self.inputs = inputs
        
        if self.pinEN >= 0:
            GPIO.setup(self.pinEN, GPIO.OUT)
        GPIO.setup(self.pin1, GPIO.OUT)
        GPIO.setup(self.pin2, GPIO.OUT)
        GPIO.output(self.pin1, GPIO.LOW)
        GPIO.output(self.pin2, GPIO.LOW)
        if self.pinEN >= 0:
            self.pwm = GPIO.PWM(self.pinEN, 1000)
            self.pwm.start(0)
        else:
            self.pwm = None
        
    def update(self, updateInterval):
        setMotor(self.pwm, self.pin1, self.pin2, getSumOfInputs(self.inputs))


class Servo_1(object):
    
    def __init__(self, pin, restingDutyCycle, minDutyCycle, maxDutyCycle, inputs):
        self.pin = pin
        self.restingDutyCycle = restingDutyCycle
        self.minDutyCycle = minDutyCycle
        self.maxDutyCycle = maxDutyCycle
        self.inputs = inputs
        
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(self.restingDutyCycle)

    def update(self, updateInterval):
        setServo(self.pwm, self.restingDutyCycle + getSumOfInputs(self.inputs), self.minDutyCycle, self.maxDutyCycle)


class Servo_2(object):
    
    def __init__(self, pin, startingDutyCycle, minDutyCycle, maxDutyCycle, inputs):
        self.pin = pin
        self.startingDutyCycle = startingDutyCycle
        self.minDutyCycle = minDutyCycle
        self.maxDutyCycle = maxDutyCycle
        self.inputs = inputs
        
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(self.startingDutyCycle)
        self.currentDutyCycle = self.startingDutyCycle

    def update(self, updateInterval):
        self.currentDutyCycle = max(self.minDutyCycle, min(self.maxDutyCycle, self.currentDutyCycle + getSumOfInputs(self.inputs) * updateInterval))
        setServo(self.pwm, self.currentDutyCycle, self.minDutyCycle, self.maxDutyCycle)


class PCA9685_1(object):
    
    def __init__(self, pca9685, channel, restingDutyCycle, minDutyCycle, maxDutyCycle, inputs):
        self.pca9685 = pca9685
        self.channel = channel
        self.restingDutyCycle = restingDutyCycle
        self.minDutyCycle = minDutyCycle
        self.maxDutyCycle = maxDutyCycle
        self.inputs = inputs
        
        setServoPCA9685(pca9685, self.channel, self.restingDutyCycle, self.minDutyCycle, self.maxDutyCycle)

    def update(self, updateInterval):
        setServoPCA9685(self.pca9685, self.channel, self.restingDutyCycle + getSumOfInputs(self.inputs), self.minDutyCycle, self.maxDutyCycle)


class PCA9685_2(object):
    
    def __init__(self, pca9685, channel, startingDutyCycle, minDutyCycle, maxDutyCycle, inputs):
        self.pca9685 = pca9685
        self.channel = channel
        self.startingDutyCycle = startingDutyCycle
        self.minDutyCycle = minDutyCycle
        self.maxDutyCycle = maxDutyCycle
        self.inputs = inputs
        
        self.currentDutyCycle = self.startingDutyCycle
        setServoPCA9685(pca9685, self.channel, self.startingDutyCycle, self.minDutyCycle, self.maxDutyCycle)

    def update(self, updateInterval):
        self.currentDutyCycle = max(self.minDutyCycle, min(self.maxDutyCycle, self.currentDutyCycle + getSumOfInputs(self.inputs) * updateInterval))
        setServoPCA9685(self.pca9685, self.channel, self.currentDutyCycle, self.minDutyCycle, self.maxDutyCycle)