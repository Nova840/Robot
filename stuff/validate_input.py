def validateInput(lines):
    lines = lines.copy()
    for i in range(len(lines)):
        lines[i] = lines[i].split(",")
    for line in lines:
        if not firstElementIsValidType(line):
            raise RuntimeError("The first element on one or more lines is not valid.")
        if not correctNumberOfElements(line):
            raise RuntimeError("There are an incorrect number of elements on one or more lines.")
        if not correctTypes(line):
            raise RuntimeError("Some elements are not numbers where they should be.")
        if not servoValuesWithinRange(line):
            raise RuntimeError("Some servo values are out of range.")
    if not uniquePins(lines):
        raise RuntimeError("Some pins are either used more than once or invalid.")

def firstElementIsValidType(splitLine):
    first = splitLine[0]
    return first == "MOTOR" or first == "SERVO_1" or first == "SERVO_2" or first == "PCA9685_1" or first == "PCA9685_2" or first == "SHUTDOWN"

def correctNumberOfElements(splitLine):
    #number of elements must be even, because inputs come in pairs
    #skip over the first 4 elements for motors, first 5 for servos
    if splitLine[0] == "MOTOR":
        return len(splitLine) >= 4 and len(splitLine[4:]) % 2 == 0
    elif splitLine[0] == "SHUTDOWN":
        return len(splitLine) >= 1 and len(splitLine[1:]) % 2 == 0
    else:
        return len(splitLine) >= 5 and len(splitLine[5:]) % 2 == 0

def correctTypes(splitLine):
    try:
        if splitLine[0] == "MOTOR":
            int(splitLine[1])
            int(splitLine[2])
            int(splitLine[3])
            for i in range(len(splitLine[4:])):
                if i % 2 == 0:
                    continue
                float(splitLine[i + 4])
        elif splitLine[0] == "SHUTDOWN":
            for i in range(len(splitLine[1:])):
                if i % 2 == 0:
                    continue
                float(splitLine[i + 1])
        else:
            int(splitLine[1])
            float(splitLine[2])
            float(splitLine[3])
            float(splitLine[4])
            for i in range(len(splitLine[5:])):
                if i % 2 == 0:
                    continue
                float(splitLine[i + 5])
        
        if splitLine[0] == "MOTOR":
            for i in range(len(splitLine[4:])):
                if i % 2 == 1:
                    continue
                if splitLine[i + 4][0:3] == "BTN":
                    int(splitLine[i + 4][4:])
        elif splitLine[0] == "SHUTDOWN":
            for i in range(len(splitLine[1:])):
                if i % 2 == 1:
                    continue
                if splitLine[i + 1][0:3] == "BTN":
                    int(splitLine[i + 1][4:])
        else:
            for i in range(len(splitLine[5:])):
                if i % 2 == 1:
                    continue
                if splitLine[i + 5][0:3] == "BTN":
                    int(splitLine[i + 5][4:])
        return True
    except:
        return False

def servoValuesWithinRange(splitLine):
    if splitLine[0] == "MOTOR" or splitLine[0] == "SHUTDOWN":
        return True

    servoStart = float(splitLine[2])
    servoMin = float(splitLine[3])
    servoMax = float(splitLine[4])

    if servoMin < 0:
        return False
    if servoMax > 100:
        return False
    if servoMin > servoMax:
        return False
    if servoStart < servoMin:
        return False
    if servoStart > servoMax:
        return False
    
    return True

def uniquePins(splitLines):
    channels = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    pins = [4,17,27,22,10,9,11,5,6,13,19,26,14,15,18,23,24,25,8,7,12,16,20,21]
    for splitLine in splitLines:
        first = splitLine[0]
        
        if first == "MOTOR":
            if not validPin(int(splitLine[1]), pins, True) or not validPin(int(splitLine[2]), pins, False) or not validPin(int(splitLine[3]), pins, False):
                return False
        elif first == "SERVO_1" or first == "SERVO_2":
            if not validPin(int(splitLine[1]), pins, False):
                return False
        elif first == "PCA9685_1" or first == "PCA9685_2":
            if not validPin(int(splitLine[1]), channels, False):
                return False
            
        if first == "MOTOR":
            for i in range(len(splitLine[4:])):
                if i % 2 == 1:
                    continue
                if splitLine[i + 4][0:3] == "BTN" and not validPin(int(splitLine[i + 4][4:]), pins, False):
                    return False
        elif first == "SHUTDOWN":
            for i in range(len(splitLine[1:])):
                if i % 2 == 1:
                    continue
                if splitLine[i + 1][0:3] == "BTN" and not validPin(int(splitLine[i + 1][4:]), pins, False):
                    return False
        else:
            for i in range(len(splitLine[5:])):
                if i % 2 == 1:
                    continue
                if splitLine[i + 5][0:3] == "BTN" and not validPin(int(splitLine[i + 5][4:]), pins, False):
                    return False
                
    return True

def validPin(pin, pins, isMotorEN):
    if isMotorEN and pin < 0:
        return True
    valid = pin in pins
    if valid:
        pins.remove(pin)
    return valid