import serial
import os
import time

start_time = time.time()

ser = serial.Serial('COM17', 921600)

data_packet=[]

while(True):
    line = ser.readline()

    # start of data packet
    if(line == b'\n'):
        del data_packet[:]

    # decode the line and store it
    data_packet.append(line.decode("utf-8").strip('\n'))

    #print(data_packet)

    # recieved the whole packet
    if(len(data_packet)==6):
        # print elapsed time
        print('{:4.2f}'.format(time.time() - start_time), end=" ")

        # check the property_id
        if(data_packet[3][-2:] == "4d"):
            print("Motion Detected:", end =" ")
            print(data_packet[5][-2:])

            # turn lights on when motion detected
            os.system('python control-insteon.py 100')
        elif(data_packet[3][-2:] == "4f"):
            #print("Temperature Read:", end =" ")
            # convert from string to int
            temp = int(data_packet[5][-2:], 16)
            #print(temp)
        else:
            print("Unknown Data")

ser.close()