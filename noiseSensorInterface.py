"""
This file facilitates data transfer from WS1381 or HY1361 Noise Level Meters
	(Noise Sensor) to Raspberry Pis
Code was built off of https://github.com/mepster/wensn/blob/master/README.md
	and https://www.ebswift.com/reverse-engineering-spl-usb.html

Must install pyusb library, and set permissions for usb device
To do this follow directions below:

   1- Open terminal window
   2- Enter "pip install pyusb"
   3- To set permissions for usb device create a file by entering: "sudo touch /etc/udev/rules.d/50-usb-perms.rules" in terminal
   4- Open this file by entering: "sudo nano /etc/udev/rules.d/50-usb-perms.rules" in terminal
   5- Add this line to the file (do not include <>): <SUBSYSTEM=="usb", ATTRS{idVendor}=="16c0", ATTRS{idProduct}=="05dc", GROUP="plugdev", MODE="0660">
   6- Save file and exit
   7- In terminal enter "sudo udevadm control --reload"
   8- Also enter "sudo udevadm trigger"

If having error message: could not find module usb.core, pyusb may not be fully installed. Try running "pip install pyusb" and/or "pip3 install pyusb".
If having error message: Authentication error, usb permissions may not have been set correctly. Try veryfying steps 3 through 6, try running with "sudo" (temporary fix but permissions should be updated)
If having error message: AssertionError, make sure sensor has been plugged in

If having issues running this file, see:
	https://github.com/mepster/wensn/blob/master/README.md

"""

import usb.core
import datetime
import time
import os

#This lists all settings available to input to the noise sensor. Adjust them by specifying parameter when calling connectToNoiseSensor function
#Shows what ranges would be listened for. 30-130 recomended
ranges = ["30-80", "40-90", "50-100", "60-110"]

#Fast shows instantaneous DB value, Slow shows average DB over 1 second (slow recomended for most IOT applications)
speeds = ["fast", "slow"]

#Sets frequency wheighting. A is for normal frequency (recomended) C is for low frequency
weights = ["A", "C"]

# Max would hold the highest value (Instant is recomended for most IOT aplications
maxModes = ["instant", "max"]


def connectToNoiseSensor(range="60-110", speed="slow", weight="A", maxMode="instant"):
    # connect to WS1381 over USB
    dev = usb.core.find(idVendor=0x16c0, idProduct=0x5dc)
    assert dev is not None

    # set default modes: "A" weighting, "slow"
    rangeN = ranges[0:4].index(range)
    # For rangeN, setting over USB supports only 2 bits of range,
    #   although 7 values (0 to 6) can be set with buttons on unit.
    speedN = speeds.index(speed)
    weightN = weights.index(weight)
    maxModeN = maxModes.index(maxMode)
    print("setMode: " + range + " weight:" + weight + " speed:" + speed + " maxMode:" + maxMode)
    #wvalue = rangeN | weightN<<3 | speedN<<4 | maxModeN<<5
    wvalue = (rangeN&3) | (weightN&1)<<3 | (speedN&1)<<4 | (maxModeN&1)<<5
    # Function of bits 6 and 7 is unknown (nothing?)
    dev.ctrl_transfer(0xC0, 3, wvalue, 0, 200)

    log = "bo"
    return(dev)


def getNoiseLevel(connection):
    dev = connection

    now = datetime.datetime.now()
    # roll over to a new log whenever the filename changes - in this case, every hour.

    ret = dev.ctrl_transfer(0xC0, 4, 0, 10, 200) # wvalue (3rd arg) is ignored
    #print(ret)
    #print(format(ret[1], '#010b'))

    rangeN = (ret[1]&28)>>2 # bits 2,3,4 in ret[1] return rangeN from 0 to 6
    weightN = (ret[1]&32)>>5 # bit 5 in ret[1] return weightN
    speedN = (ret[1]&64)>>6 # bit 6 in ret[1] return speedN
    # bit 7 seems to alternate every 1 second?
    dB = (ret[0] + ((ret[1] & 3) * 256)) * 0.1 + 30
    #print("%.2f,%s,%s,%s"% (dB, weight, speed, now.strftime('%Y,%m,%d,%H,%M,%S')),file = log.fp)
    return(dB)

# Gives back the average noise in dB over a period of 5 minutes
# Takes one data point every 10 seconds for a total of 30 points
def average(connection):
    i = 0
    val = 0
    average = 0
    while i<30:
        val += getNoiseLevel(connection)
        time.sleep(10)
        i += 1
    average = val/i
    return(average)

if __name__ == "__main__":
    connection = connectToNoiseSensor("60-110", "fast", "A", "instant")
    i = 0
    while i<50:
        print(getNoiseLevel(connection))
        time.sleep(1)
        i += 1



