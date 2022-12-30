import RPi.GPIO as GPIO
import xbox
from pynput import keyboard, mouse

joy = None
try:
    joy = xbox.Joystick()
    print("Joystick Found")
except:
    print("Joystick Not Found")

keyboardInputs = []

def getInput(inputText, multiplier):
    device = inputText[0:3]
    button = inputText[4:]
    result = 0
    if device == "KEY":
        result = 1 if button in keyboardInputs else 0
    elif device == "JOY" and joy != None and joy.connected():
        if button == "A":
            result = joy.A()
        elif button == "B":
            result = joy.B()
        elif button == "X":
            result = joy.X()
        elif button == "Y":
            result = joy.Y()
        elif button == "START":
            result = joy.Start()
        elif button == "Back":
            result = joy.Back()
        elif button == "GUIDE":
            result = joy.Guide()
        elif button == "LEFTX":
            result = joy.leftX()
        elif button == "LEFTY":
            result = joy.leftY()
        elif button == "RIGHTX":
            result = joy.rightX()
        elif button == "RIGHTY":
            result = joy.rightY()
        elif button == "DPADUP":
            result = joy.dpadUp()
        elif button == "DPADDOWN":
            result = joy.dpadDown()
        elif button == "DPADLEFT":
            result = joy.dpadLeft()
        elif button == "DPADRIGHT":
            result = joy.dpadRight()
        elif button == "LEFTTHUMBSTICK":
            result = joy.leftThumbstick()
        elif button == "RIGHTTHUMBSTICK":
            result = joy.rightThumbstick()
        elif button == "LEFTBUMPER":
            result = joy.leftBumper()
        elif button == "RIGHTBUMPER":
            result = joy.rightBumper()
        elif button == "LEFTTRIGGER":
            result = joy.leftTrigger()
        elif button == "RIGHTTRIGGER":
            result = joy.rightTrigger()
    elif device == "BTN":
        result = not GPIO.input(int(button))
    result *= multiplier
    return result

def getSumOfInputs(inputs):
    sumInputs = 0
    for i in inputs:
        sumInputs += getInput(i, inputs[i])
    return sumInputs

def setMotor(pwm, pin1, pin2, percentInput):
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

def setServo(pwm, dutyCycle, minDutyCycle, maxDutyCycle):
    dutyCycle = max(minDutyCycle, min(maxDutyCycle, dutyCycle))
    pwm.ChangeDutyCycle(dutyCycle)

def setServoPCA9685(pca9685, channel, dutyCycle, minDutyCycle, maxDutyCycle):
    dutyCycle = max(minDutyCycle, min(maxDutyCycle, dutyCycle))
    pca9685.channels[channel].duty_cycle = round(dutyCycle / 100 * 65535)#percent of 65535

def getInputsDictionary(inputs):#inputs is an array that alternates between string and float
    inputsDict = {}
    for i in range(int(len(inputs) / 2)):
        inputsDict.update({inputs[i * 2]: float(inputs[i * 2 + 1])})#input string: input multiplier
    for i in inputsDict:
        if i[0:3] == "BTN":
            GPIO.setup(int(i[4:]), GPIO.IN, pull_up_down = GPIO.PUD_UP)
    return inputsDict

def on_press(key):
    keyStr = str(key).upper()
    if keyStr not in keyboardInputs:
        keyboardInputs.append(keyStr)

def on_release(key):
    keyStr = str(key).upper()
    if keyStr in keyboardInputs:
        keyboardInputs.remove(keyStr)
        
def on_click(x, y, button, pressed):
    buttonStr = str(button).upper()
    if pressed:
        if buttonStr not in keyboardInputs:
            keyboardInputs.append(buttonStr)
    else:
        if buttonStr in keyboardInputs:
            keyboardInputs.remove(buttonStr)

k_listener = keyboard.Listener(on_press = on_press, on_release = on_release, suppress = True)
k_listener.start()

m_listener = mouse.Listener(on_click = on_click, suppress = True)
m_listener.start()

def shutdown():
    command = "/usr/bin/sudo /sbin/shutdown -P now"
    import subprocess
    subprocess.Popen(command.split())
    
def stopInputListeners():
    k_listener.stop()
    m_listener.stop()
    if joy != None:
        joy.close()