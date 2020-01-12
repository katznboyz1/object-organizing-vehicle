#imports
import pigpio, time

#function provided by https://github.com/TFmini/TFmini-RaspberryPi
def getTFminiData():
    
    #set up gpio stuff
    RX = 15
    pi = pigpio.pi()
    pi.set_mode(RX, pigpio.INPUT)
    pi.bb_serial_read_open(RX, 115200) 

    #main try statement
    try:
        time.sleep(0.05)
        (count, recv) = pi.bb_serial_read(RX)
        if count > 8:
            for i in range(0, count-9):
                if recv[i] == 89 and recv[i+1] == 89: # 0x59 is 89
                    checksum = 0
                for j in range(0, 8):
                    checksum = checksum + recv[i+j]
                checksum = checksum % 256
                if checksum == recv[i+8]:
                    distance = recv[i+2] + recv[i+3] * 256
                    strength = recv[i+4] + recv[i+5] * 256
                    return [True, distance, strength] #status on whether or not the request was completed, distance, strength
    
    #if there is an error then return the false completion status
    except:
        return [False, 0, 0]
    
    #close the connection
    finally:
        pi.bb_serial_read_close(RX)
        pi.stop()

#print the data (distance is in CM)
data = getTFminiData()
print('''
DATA RECIEVED FROM TFMINI:
Distance: {}cm
Strength: {}
Success: {}
'''.format(data[1], data[2], 'Yes' if data[0] else 'No'))