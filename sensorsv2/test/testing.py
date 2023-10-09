import serial
import time
import datetime
import os


start_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"log_{start_time}.txt"
sensing_data = ""

arduino = serial.Serial(port='/dev/cu.usbmodem12201', baudrate=9600, timeout=2)
#timeout=None : wait forever / until requested number of bytes are received

while True:
    arduino.write(b'start')
    data = arduino.readline().decode().rstrip()
    if data == "EOF":
        print("sensing ended")
        break
    if data != "":
        print(data)
        sensing_data += data +"\n"

# Define the folder path
folder_path = "raw_data"

# Create the folder if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Build the full file path
file_path = os.path.join(folder_path, filename)


try:
    with open(file_path, "w") as file:
        file.write(sensing_data)
        print("Data saved to file:", file_path)
except Exception as e:
    print("Error:", e)


