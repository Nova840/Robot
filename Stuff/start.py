import RPi.GPIO as GPIO
from time import sleep
import os
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
import sys
from input_manager import Input
from motors import L298N, DRV8833, Servo_1, Servo_2, PCA9685_1, PCA9685_2
from validate_input import validateInput

def main():
    file = open(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/inputs.txt", "r")
    lines = file.readlines()
    file.close()
    for i in range(len(lines)):
        lines[i] = "".join(lines[i].split())#remove all white space
        lines[i] = lines[i].upper()#capitalize everything
    lines = [line for line in lines if not line == ""]#removes empty lines
    lines = [line for line in lines if not line[0] == "#"]#removes commented lines

    try:
        validateInput(lines)
    except Exception as e:
        print(e)
        print("Press enter to exit.")
        Input.stopInputListeners()
        input()
        sys.exit()

    try:
        i2c_bus = busio.I2C(SCL, SDA)
        pca9685 = PCA9685(i2c_bus)
        pca9685.frequency = 60
    except:
        pca9685 = None
    GPIO.setmode(GPIO.BCM)
    motors = []
    shutdown_inputs = {}

    for l in lines:
        l = l.split(",")
        if l[0] == "L298N":
            motors.append(L298N(int(l[1]), int(l[2]), int(l[3]), Input.getInputsDictionary(l[4:])))
        elif l[0] == "DRV8833":
            motors.append(DRV8833(int(l[1]), int(l[2]), Input.getInputsDictionary(l[3:])))
        elif l[0] == "SERVO_1":
            motors.append(Servo_1(int(l[1]), float(l[2]), float(l[3]), float(l[4]), Input.getInputsDictionary(l[5:])))
        elif l[0] == "SERVO_2":
            motors.append(Servo_2(int(l[1]), float(l[2]), float(l[3]), float(l[4]), Input.getInputsDictionary(l[5:])))
        elif pca9685 != None and l[0] == "PCA9685_1":
            motors.append(PCA9685_1(pca9685, int(l[1]), float(l[2]), float(l[3]), float(l[4]), Input.getInputsDictionary(l[5:])))
        elif pca9685 != None and l[0] == "PCA9685_2":
            motors.append(PCA9685_2(pca9685, int(l[1]), float(l[2]), float(l[3]), float(l[4]), Input.getInputsDictionary(l[5:])))
        elif l[0] == "SHUTDOWN":
            shutdown_inputs.update(Input.getInputsDictionary(l[1:]))

    print("Script Started")

    updateInterval = 1 / 30 #update 30 times per second
    running = True
    while True:
        for i in shutdown_inputs:
            if Input.getInput(i, shutdown_inputs[i]) >= 1:
                shutdown()
                running = False
                break        
        if not running:
            break
        if Input.getInput("KEY_KEY.ESC", 1) >= 1:
            break
            
        for motor in motors:
            motor.update(updateInterval)
        
        sleep(updateInterval)

    GPIO.setwarnings(False)#in case there are no GPIO pins set up
    GPIO.cleanup()

    print("Script Finished")

def shutdown():
    command = "/usr/bin/sudo /sbin/shutdown -P now"
    import subprocess
    subprocess.Popen(command.split())

if __name__ == '__main__':
    main()