import serial

ser = serial.Serial('COM7', 115200)  # change COM port

while True:
    line = ser.readline().decode().strip()
    print(line)


def parse_data(line):
    try:
        key, value = line.split(":")
        return {key: int(value)}
    except:
        return None