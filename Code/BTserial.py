from time import sleep
import serial

# Establish the connection on a specific port
ser = serial.Serial('COM7', 9600, timeout=15)

while True:
    signal = input("Open (O) / Close (C): ")
    print(signal)
    ser.write(signal.encode())
    sleep(.1)  # Delay for one tenth of a second
