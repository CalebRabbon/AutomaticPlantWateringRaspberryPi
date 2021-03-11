"""
Instructions from here (http://lechacal.com/wiki/index.php?title=Howto_setup_Raspbian_for_serial_read)

Step 1: Enter "sudo raspi-config" in terminal
Step 2: Navigate to Interface Options, then P6 Serial, select no then yes
Step 3: Update RPI with "sudo apt-get update"
Step 4: Reboot RPI with "sudo reboot & exit"
step 5: Run file
"""

import serial
from serial import Serial
import time


def connectToSensor(port,baud):
    serialConnection = serial.Serial(port, baud)
    return(serialConnection)

def getData(serialConnection):
    # Read one line from the serial buffer

    # Create the data list to return
    datalist = []

    # readline from the serial connection and remove the excess \n characters
    # with rstrip
    data = serialConnection.readline().decode('utf-8').rstrip()
    datalist.append(data)

    return datalist

if __name__ == "__main__":
    ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            #line = ser.readline()
            print(line)

#    i = 0
#    while(i < 10):
#       connection = connectToSensor('/dev/ttyACM1', 9600)
#       connection.flush()
#
#       while True:
#           if connection.in_waiting > 0:
#               line = connection.readline().decode('utf-8').rstrip()
#               print(line)
#       #getData(connection)
#       i += 1
#    while i<50:
#        print(getData(connection))
#        i += 1
