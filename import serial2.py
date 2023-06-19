import serial
import csv
import time
import os
import pandas as pd
import numpy as np

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

#get number of data points
cmd_points = "DSPN?0\n"
ser.write(cmd_points.encode())
time.sleep(1)
points = int(float(ser.read(ser.in_waiting).decode()))
print("N: ", points)

#get start frequency
cmd_start_freq = "SSTR?0\n" # replace with actual command
ser.write(cmd_start_freq.encode())
time.sleep(1)
start_freq = float(ser.read(ser.in_waiting).decode())
print("Start Frequency: ",start_freq)

#get stop frequency
cmd_stop_freq = "SSTP?0\n" # replace with actual command
ser.write(cmd_stop_freq.encode())
time.sleep(1)
stop_freq = float(ser.read(ser.in_waiting).decode())
print("Stop Frequency: ",stop_freq)

#calculate x values
x_values = np.logspace(np.log10(start_freq), np.log10(stop_freq), num=points)


#get y values
cmd = "DSPY?0\n"
ser.write(cmd.encode())
y_values = []
while True:
    time.sleep(3)
    rx = ser.read(ser.in_waiting).decode()
    if not rx:
        break
    for val in rx.split(","):
        try:
            y_values.append(float(val))
        except ValueError:
            print(f"Skipping invalid value: {val}")

ser.close()

#################################
lower_limit = float(input("Enter the lower limit for Y values: "))
upper_limit = float(input("Enter the upper limit for Y values: "))

# Filter Y values based on user-defined limits
y_values = [y if lower_limit <= y <= upper_limit else None for y in y_values]
#################################

#combine x and y values
data = list(zip(x_values, y_values))
filename = input("Enter filename for the CSV file (without .csv extension): ")
directory = input("Enter the directory to save the CSV file (e.g. C:/Users/username/Documents): ")
y_label = input("Enter the label for the Y data: ")

filename_with_path = os.path.join(directory, f'{filename}.csv')

if os.path.exists(filename_with_path):
    # if file exists, read it, add new column, and write back
    df = pd.read_csv(filename_with_path)
    df_new = pd.DataFrame(data, columns=['Frequency (Hz)', y_label])
    df = pd.concat([df, df_new[y_label]], axis=1)
else:
    # if file does not exist, create it
    df = pd.DataFrame(data, columns=['Frequency (Hz)', y_label])

df.to_csv(filename_with_path, index=False)

