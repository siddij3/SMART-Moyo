import glob
import serial
import sys
import time

""" Lists serial port names

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of the serial ports available on the system
"""
def findPorts():
    # TODO incosistent variable definitions for bluetooth in Windows
    bluetooth = False
    timeout = 1 #second
    print(sys.platform) #Debugging to android
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(16)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
        bluetooth = glob.glob('/dev/rfcomm[A-Za-z0-9]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
        bluetooth = glob.glob('/dev/rfcomm[A-Za-z0-9]*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    print(ports)
    for port in ports:
        try:
            s = serial.Serial(port, timeout=timeout)
            tmp = s.readline().decode('utf-8')
            s.close()

            if (tmp != ''):
                result.append(port)
        except (OSError, serial.SerialException):
            pass

    if result == []:
        print("\n\nThe accelerometer is not on or not connected properly\n\n")
        print("If you have turned it on, give it a few moments and try again shortly\n\n")
        time.sleep(2)
        exit()

    return result[0]


#Checks for idle accelerometer (No compressions being performed)
def idle(accel, err):
    tmp = max(accel) - min(accel)
    if abs(tmp) <= 0.09*err:
        print("Accelerometer is idle\n\n")
        return True

    return False

#Opens up manual serial port
def openSerial(port, baud):
    ser = serial.Serial(port, baud)

    if ser.isOpen():
        print('Port ' + ser.name + ' is open')
    else:
        print("Port is not open")
        ser.close()
        exit()

    return ser

# Reads one line from the serial port
def readSerial(ser):
    # Removes possible incomplete lines
    cleanLine = ser.readline().decode('utf-8')
    data = ser.readline().decode('utf-8')

    return data

# Fixes each line as time becomes large
# Readline Might have made this unnecessary
def fixByteSize(byte, data):
#TODO
    return
