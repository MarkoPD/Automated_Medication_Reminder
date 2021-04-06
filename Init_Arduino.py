import serial
import time

Deactivate = "0"
Activate = "2"
encDeactivate = Deactivate.encode()
encActivate = Activate.encode()
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.flush()

def Activate(flag):
    while (flag == 1):
        ser.write(encActivate)
        line = ser.readline().decode('utf-8').rstrip()
        lenline = len(line)
        if (lenline > 0):
            flag = 0
            break

def Deactivate(flag):
    while (flag == 1):
        ser.write(encDeactivate)
        line = ser.readline().decode('utf-8').rstrip()
        lenline = len(line)
        if (lenline > 0):
            flag = 0
            break

def Activate_Alarm():
    flagA = 1
    Activate(flagA)


def Deactivate_Alarm():
    flagD = 1
    Deactivate(flagD)
