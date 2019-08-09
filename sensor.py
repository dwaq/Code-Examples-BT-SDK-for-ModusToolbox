import serial
import os
import time

start_time = time.time()
last_time = 0

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
        

        # check the property_id
        if(data_packet[3][-2:] == "4d"):
            elapsed_time = time.time() - start_time
            print('{:4.2f}'.format(elapsed_time), end=" ")

            time_diff = elapsed_time - last_time
            print('{:4.2f}'.format(time_diff), end=" ")

            last_time = elapsed_time

            print("Motion Detected:", end =" ")
            raw_value=data_packet[5][-2:]
            print(raw_value)

            # turn lights on when motion detected
            if(raw_value=="01"):
                os.system('python control-insteon.py 100')
            # turn lights off when motion no longer detected
            elif(raw_value=="00"):
                os.system('python control-insteon.py 0')
            
        elif(data_packet[3][-2:] == "4f"):
            #print("Temperature Read:", end =" ")
            # convert from string to int
            temp = int(data_packet[5][-2:], 16)
            #print(temp)
        else:
            print("Unknown Data")

ser.close()