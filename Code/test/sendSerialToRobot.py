import serial 
from serialCom import SerialCommunicator
import time

# arduino = serial.Serial(port='COM8', baudrate=1000000, timeout=1) 

SC = SerialCommunicator("COM8", 1000000, 1)
SC.start()

time.sleep(1)

TRAVEL = 10
SLEEP = 0

# def write_read(x): 
    # arduino.write((x + '\n').encode())
    # response = arduino.read_until(b'\n').decode().strip()
    # return response


while 1:
    for i in range(TRAVEL):
        SC.write(str(90-i) + "|" + str(i) + "|")
        # write_read(str(90-i) + "|" + str(i) + "|")
        time.sleep(SLEEP)

    for i in range(TRAVEL):
        i = TRAVEL - i 
        SC.write(str(90 - i) + "|" + str(i) + "|")
        # write_read(str(90 - i) + "|" + str(i) + "|")
        time.sleep(SLEEP)



    newString = str(round(math.degrees(math.pi-link1.get_angle()))) + "|" + str(round(angle2 * 57.2957795)) + "|"
    if (preString != newString):
        print(newString)
        SC.write(newString)
        preString = newString
