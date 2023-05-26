import xbox
from pynput import keyboard, mouse
import RPi.GPIO as GPIO

class Input:
    _joy = None
    try:
        _joy = xbox.Joystick()
        print("Joystick Found")
    except:
        print("Joystick Not Found")

    _keyboardInputs = []

    def _on_press(key):
        keyStr = str(key).upper()
        if keyStr not in Input._keyboardInputs:
            Input._keyboardInputs.append(keyStr)

    def _on_release(key):
        keyStr = str(key).upper()
        if keyStr in Input._keyboardInputs:
            Input._keyboardInputs.remove(keyStr)

    def _on_click(x, y, button, pressed):
        buttonStr = str(button).upper()
        if pressed:
            if buttonStr not in Input._keyboardInputs:
                Input._keyboardInputs.append(buttonStr)
        else:
            if buttonStr in Input._keyboardInputs:
                Input._keyboardInputs.remove(buttonStr)

    _k_listener = keyboard.Listener(on_press = _on_press, on_release = _on_release, suppress = True)
    _k_listener.start()

    _m_listener = mouse.Listener(on_click = _on_click, suppress = True)
    _m_listener.start()

    @staticmethod
    def getInput(inputText, multiplier):
        device = inputText[0:3]
        button = inputText[4:]
        result = 0
        if device == "KEY":
            result = 1 if button in Input._keyboardInputs else 0
        elif device == "JOY" and Input._joy != None and Input._joy.connected():
            if button == "A":
                result = Input._joy.A()
            elif button == "B":
                result = Input._joy.B()
            elif button == "X":
                result = Input._joy.X()
            elif button == "Y":
                result = Input._joy.Y()
            elif button == "START":
                result = Input._joy.Start()
            elif button == "BACK":
                result = Input._joy.Back()
            elif button == "GUIDE":
                result = Input._joy.Guide()
            elif button == "LEFTX":
                result = Input._joy.leftX()
            elif button == "LEFTY":
                result = Input._joy.leftY()
            elif button == "RIGHTX":
                result = Input._joy.rightX()
            elif button == "RIGHTY":
                result = Input._joy.rightY()
            elif button == "DPADUP":
                result = Input._joy.dpadUp()
            elif button == "DPADDOWN":
                result = Input._joy.dpadDown()
            elif button == "DPADLEFT":
                result = Input._joy.dpadLeft()
            elif button == "DPADRIGHT":
                result = Input._joy.dpadRight()
            elif button == "LEFTTHUMBSTICK":
                result = Input._joy.leftThumbstick()
            elif button == "RIGHTTHUMBSTICK":
                result = Input._joy.rightThumbstick()
            elif button == "LEFTBUMPER":
                result = Input._joy.leftBumper()
            elif button == "RIGHTBUMPER":
                result = Input._joy.rightBumper()
            elif button == "LEFTTRIGGER":
                result = Input._joy.leftTrigger()
            elif button == "RIGHTTRIGGER":
                result = Input._joy.rightTrigger()
        elif device == "SWT":
            result = not GPIO.input(int(button))
        result *= multiplier
        return result
    
    @staticmethod
    def getSumOfInputs(inputs):
        sumInputs = 0
        for i in inputs:
            sumInputs += Input.getInput(i, inputs[i])
        return sumInputs

    @staticmethod
    def getInputsDictionary(inputs):#inputs is an array that alternates between string and float
        inputsDict = {}
        for i in range(int(len(inputs) / 2)):
            inputsDict.update({inputs[i * 2]: float(inputs[i * 2 + 1])})#input string: input multiplier
        for i in inputsDict:
            if i[0:3] == "SWT":
                GPIO.setup(int(i[4:]), GPIO.IN, pull_up_down = GPIO.PUD_UP)
        return inputsDict

    @staticmethod
    def stopInputListeners():
        Input._k_listener.stop()
        Input._m_listener.stop()
        if Input._joy != None:
            Input._joy.close()