import time
import sys
from hx711 import HX711
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

referenceUnit = -454
hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()
print("Tare done, place case on scale")
time.sleep(10)

def getWeight():
    boxWeight = max(0, float(hx.get_weight(5)))
    hx.power_down()
    hx.power_up()
    cutWeight = Truncate(boxWeight,1)
    return cutWeight

def get_Number_Of_Pills():
    caseWeight = float(getWeight())
    if (16.4 <= caseWeight <= 18):  
        numPills = 14  # EXPECTED 17.g
        expectedWeight = 17.0
    elif (15.1 <= caseWeight <= 16.3):
        numPills = 13  # EXPECTED 15.8g
        expectedWeight = 15.8
    elif (13.9 <= caseWeight <= 15.0):
        numPills = 12  # EXPECTED 14.6g
        expectedWeight = 14.6
    elif (12.8 <= caseWeight <= 13.8):
        numPills = 11  # EXPECTED 13.4g
        expectedWeight = 13.4
    elif (11.6 <= caseWeight <= 12.7):
        numPills = 10  # EXPECTED 12.0g
        expectedWeight = 12.0
    elif (10.4 <= caseWeight <= 11.5):
        numPills = 9  # EXPECTED 10.8g
        expectedWeight = 10.8
    elif (9.1 <= caseWeight <= 10.3):
        numPills = 8  # EXPECTED 9.6g
        expectedWeight = 9.6
    elif (7.8 <= caseWeight <= 9.0):
        numPills = 7  # EXPECTED 8.4g
        expectedWeight = 8.4
    elif (6.6 <= caseWeight <= 7.7):
        numPills = 6  # EXPECTED 7.2g
        expectedWeight = 7.2
    elif (5.4 <= caseWeight <= 6.5):
        numPills = 5  # EXPECTED 6.0g
        expectedWeight = 6.0
    elif (4.2 <= caseWeight <= 5.3):
        numPills = 4  # EXPECTED 4.8g
        expectedWeight = 4.8
    elif (2.9 <= caseWeight <= 4.1):
        numPills = 3  # EXPECTED 3.6g
        expectedWeight = 3.6
    elif (2.0 <= caseWeight <= 2.8):
        numPills = 2  # EXPECTED 2.4g
        expectedWeight = 2.4
    elif (1.0 <= caseWeight <= 1.9):
        numPills = 1  # EXPECTED 1.2g
        expectedWeight = 1.2
    elif (0 <= caseWeight <= 0.9):
        numPills = 0  # EXPECTED 0g
        expectedWeight = 0
    else:
        numPills = 0
    return numPills, caseWeight

def Truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '%.12f' % f
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

