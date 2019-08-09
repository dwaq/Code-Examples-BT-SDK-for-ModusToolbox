import serial

ser = serial.Serial('COM17', 921600)

data_packet=[]

i=0
while(i<25):
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
            print("Motion Detected:", end =" ")
            print(data_packet[5][-2:])
        elif(data_packet[3][-2:] == "4f"):
            print("Temperature Read:", end =" ")
            # convert from string to int
            temp = int(data_packet[5][-2:], 16)
            print(temp)
        else:
            print("Unknown Data")

    i=i+1

ser.close()