import serial
import os
import time

# start a timer for logging elapsed time
start_time = time.time()
last_time = 0

# open COM port (change if needed)
ser = serial.Serial('COM17', 921600)

data_packet=[]

while(True):
    # read a line
    line = ser.readline()

    # a line that is just a newline is the end of the packet
    # so delete the contents of storage to start over in the next loop
    if(line == b'\n'):
        del data_packet[:]

    # decode the line, strip the newline character, and store it
    data_packet.append(line.decode("utf-8").strip('\n'))

    #print(data_packet)

    # received the whole packet (6 lines long)
    if(len(data_packet)==6):
        # check the property_id (last 2 chars in 3rd message)
        if(data_packet[3][-2:] == "4d"):
            # calculate and print the elapsed time
            elapsed_time = time.time() - start_time
            print('{:4.2f}'.format(elapsed_time), end=" ")

            # calculate and print the time between messages
            time_diff = elapsed_time - last_time
            print('{:4.2f}'.format(time_diff), end=" ")

            # store this message's time for the next loop
            last_time = elapsed_time

            # Motion detection status is last 2 chars in 5th message
            print("Motion Detected:", end =" ")
            raw_value=data_packet[5][-2:]
            print(raw_value)

            # turn lights on when motion detected
            if(raw_value=="01"):
                os.system('python control-insteon.py 100')
            # turn lights off when motion no longer detected
            elif(raw_value=="00"):
                os.system('python control-insteon.py 0')
        
        # temperature monitoring
        '''
        # uncomment to use with sensor_temperature
        elif(data_packet[3][-2:] == "4f"):
            print("Temperature Read:", end =" ")
            # convert from string to int
            temp = int(data_packet[5][-2:], 16)
            print(temp)
        '''
        else:
            print("Unknown Data")

ser.close()