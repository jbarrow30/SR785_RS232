import serial
import csv
import time

ser = serial.Serial(
    port='COM4',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    bytesize=serial.EIGHTBITS,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

if ser.is_open == 1:
    print("Successfully Connected")
else:
    print("Failed to connect")

# enter whatever command reads
cmd = "DSPY?0,0\n"
ser.write(cmd.encode())
data = []
while True:
    time.sleep(1)
    rx = ser.read(ser.in_waiting).decode()
    if not rx:
        break
    data.append(rx.split())


ser.close()

with open('data.csv','w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)


#print(len(data))
#print(data)
