import RPi.GPIO as GPIO
from input_manager import Input

class L298N(object):
    
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
            self.pinENPWM = GPIO.PWM(self.pinEN, 1000)
            self.pinENPWM.start(0)
        else:
            self.pwm = None
        
    def update(self, updateInterval):
        _setMotorL298N(self.pinENPWM, self.pin1, self.pin2, Input.getSumOfInputs(self.inputs))


class DRV8833(object):
    
    def __init__(self, pin1, pin2, inputs):
        self.pin1 = pin1
        self.pin2 = pin2
        self.inputs = inputs
        
        GPIO.setup(self.pin1, GPIO.OUT)
        GPIO.setup(self.pin2, GPIO.OUT)
        
        self.pin1PWM = GPIO.PWM(self.pin1, 1000)
        self.pin1PWM.start(0)
        
        self.pin2PWM = GPIO.PWM(self.pin2, 1000)
        self.pin2PWM.start(0)
        
    def update(self, updateInterval):
        _setMotorDRV8833(self.pin1PWM, self.pin2PWM, Input.getSumOfInputs(self.inputs))
    

class Servo_1(object):
    
    def __init__(self, pin, restingDutyCycle, minDutyCycle, maxDutyCycle, inputs):
        self.pin = pin
        self.restingDutyCycle = restingDutyCycle
        self.minDutyCycle = minDutyCycle
        self.maxDutyCycle = maxDutyCycle
        self.inputs = inputs
        
        GPIO.setup(self.pin, GPIO.OUT)
        self.pinPWM = GPIO.PWM(self.pin, 50)
        self.pinPWM.start(self.restingDutyCycle)

    def update(self, updateInterval):
        _setServo(self.pinPWM, self.restingDutyCycle + Input.getSumOfInputs(self.inputs), self.minDutyCycle, self.maxDutyCycle)


class Servo_2(object):
    
    def __init__(self, pin, startingDutyCycle, minDutyCycle, maxDutyCycle, inputs):
        self.pin = pin
        self.startingDutyCycle = startingDutyCycle
        self.minDutyCycle = minDutyCycle
        self.maxDutyCycle = maxDutyCycle
        self.inputs = inputs
        
        GPIO.setup(self.pin, GPIO.OUT)
        self.pinPWM = GPIO.PWM(self.pin, 50)
        self.pinPWM.start(self.startingDutyCycle)
        self.currentDutyCycle = self.startingDutyCycle

    def update(self, updateInterval):
        self.currentDutyCycle = max(self.minDutyCycle, min(self.maxDutyCycle, self.currentDutyCycle + Input.getSumOfInputs(self.inputs) * updateInterval))
        _setServo(self.pinPWM, self.currentDutyCycle, self.minDutyCycle, self.maxDutyCycle)


class PCA9685_1(object):
    
    def __init__(self, pca9685, channel, restingDutyCycle, minDutyCycle, maxDutyCycle, inputs):
        self.pca9685 = pca9685
        self.channel = channel
        self.restingDutyCycle = restingDutyCycle
        self.minDutyCycle = minDutyCycle
        self.maxDutyCycle = maxDutyCycle
        self.inputs = inputs
        
        _setServoPCA9685(pca9685, self.channel, self.restingDutyCycle, self.minDutyCycle, self.maxDutyCycle)

    def update(self, updateInterval):
        _setServoPCA9685(self.pca9685, self.channel, self.restingDutyCycle + Input.getSumOfInputs(self.inputs), self.minDutyCycle, self.maxDutyCycle)


class PCA9685_2(object):
    
    def __init__(self, pca9685, channel, startingDutyCycle, minDutyCycle, maxDutyCycle, inputs):
        self.pca9685 = pca9685
        self.channel = channel
        self.startingDutyCycle = startingDutyCycle
        self.minDutyCycle = minDutyCycle
        self.maxDutyCycle = maxDutyCycle
        self.inputs = inputs
        
        self.currentDutyCycle = self.startingDutyCycle
        _setServoPCA9685(pca9685, self.channel, self.startingDutyCycle, self.minDutyCycle, self.maxDutyCycle)

    def update(self, updateInterval):
        self.currentDutyCycle = max(self.minDutyCycle, min(self.maxDutyCycle, self.currentDutyCycle + Input.getSumOfInputs(self.inputs) * updateInterval))
        _setServoPCA9685(self.pca9685, self.channel, self.currentDutyCycle, self.minDutyCycle, self.maxDutyCycle)



def _setMotorL298N(pwm, pin1, pin2, percentInput):
    spin = max(-1, min(1, percentInput))
    if spin > 0:
        GPIO.output(pin1, GPIO.HIGH)
        GPIO.output(pin2, GPIO.LOW)
    elif spin < 0:
        GPIO.output(pin1, GPIO.LOW)
        GPIO.output(pin2, GPIO.HIGH)
    else:
        GPIO.output(pin1, GPIO.LOW)
        GPIO.output(pin2, GPIO.LOW)
    if pwm != None:
        pwm.ChangeDutyCycle(abs(spin) * 100)
        
def _setMotorDRV8833(pin1, pin2, percentInput):
    spin = max(-1, min(1, percentInput))
    print(spin)
    if spin > 0:
        pin1.ChangeDutyCycle(abs(spin) * 100)
        pin2.ChangeDutyCycle(0)
    elif spin < 0:
        pin1.ChangeDutyCycle(0)
        pin2.ChangeDutyCycle(abs(spin) * 100)
    else:
        pin1.ChangeDutyCycle(0)
        pin2.ChangeDutyCycle(0)

def _setServo(pwm, dutyCycle, minDutyCycle, maxDutyCycle):
    dutyCycle = max(minDutyCycle, min(maxDutyCycle, dutyCycle))
    pwm.ChangeDutyCycle(dutyCycle)

def _setServoPCA9685(pca9685, channel, dutyCycle, minDutyCycle, maxDutyCycle):
    dutyCycle = max(minDutyCycle, min(maxDutyCycle, dutyCycle))
    pca9685.channels[channel].duty_cycle = round(dutyCycle / 100 * 65535)#percent of 65535