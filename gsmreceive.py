import RPi.GPIO as GPIO
import serial
import time, sys

GPIO.setmode(GPIO.BOARD)

def sendsms():
    ser= serial.Serial("/dev/serial0", baudrate=115200, timeout=1)
    ser.write('AT+CMGS="+91*********"'+'\r\n')
    rcv = ser.read(10)
    print (rcv)
    time.sleep(1)
    ser.write('Data matched'+'\r\n')  # Message
    rcv = ser.read(10)
    print (rcv)
    ser.write("\x1A") # Enable to send SMS
    for i in range(10):
        rcv = ser.read(10)
        print (rcv)
    
def initrec():
    ser= serial.Serial("/dev/serial0", baudrate=115200, timeout=1)
    ser.write("AT+CMGF=1\r") # set to text mode
    rcv = ser.readall()
    print(rcv)
    time.sleep(1)
    ser.write('AT+CMGDA="DEL ALL"\r') # delete all SMS
    rcv = ser.readall()
    print(rcv)
    time.sleep(1)
    reply = ser.read(ser.inWaiting()) 
    print("Listening for incomming SMS...")
    while True:
        reply = ser.read(ser.inWaiting())
        if reply != "":
            ser.write("AT+CMGR=1\r") 
            time.sleep(3)
            reply = ser.read(ser.inWaiting())
            print("SMS received. Content:")
            print(reply)
            if "help" in reply:
                print("String matched")
                sendsms()
                ser.write('AT+CMGDA="DEL ALL"\r')
                time.sleep(3)
                ser.read(ser.inWaiting())
            else:
                print("String unmatched")
                ser.write('AT+CMGDA="DEL ALL"\r')
                rcv = ser.readall()
                print(rcv)
                time.sleep(3)
                print("reset")
                
            
        

if __name__=='__main__':
    initrec()
    
