"""
Modified by Caleb Rabbon 2/25/2021
"""
import moisture
import time
import sheets

#open connection to google sheets
sheet = sheets.gSheetsConnect("moistureSensor")

# Connect to temp and current sensor
connection = moisture.connectToSensor('/dev/ttyACM0', 9600)

i = 0

# 24 hours of continuous running with i going to 8640
while i<8640:
    data = moisture.getData(connection)

    sheets.append(sheet,data)
    print(str(data), " appended to google sheets")
    time.sleep(1)

    i += 1
