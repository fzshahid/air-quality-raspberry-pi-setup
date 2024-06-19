
import serial
import requests
import json
import time

# Configure your serial port
# SERIAL_PORT = '/dev/tty.usbserial-AB0LJ9OT'  # Replace with your actual serial port
SERIAL_PORT = '/dev/ttyUSB0'  # Replace with your actual serial port
BAUD_RATE = 115200  # Replace with your baud rate

# plink -serial /dev/tty.usbserial-AB0LJ9OT -sercfg 115200,8,1,N,N

# Configure your web server endpoint
SERVER_URL = 'https://airquality.faizan.me/api/store-ccs811-readings'  # Replace with your server URL

# Open serial port
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

try:
    while True:
        # Read data from serial port
        # if 1 > 0:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').rstrip()
            print(f'Received data: {data}')
            
            # Example: Prepare data to send to server
            payload = {
                'temperature': 1,
                'humidity': 1,
                'eco2': 450,
                'tvoc': 1,
                'data': data,
                'timestamp': int(time.time())
            }
            
            # Send data to server via POST request
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            response = requests.post(SERVER_URL, data=json.dumps(payload), headers=headers)
            
            # Check response status
            if response.status_code == 200:
                print('Data sent successfully')
            else:
                print(f'Failed to send data. Status code: {response.status_code}')
        
        # Optional: Adjust delay based on your application needs
        time.sleep(10)
        
except KeyboardInterrupt:
    print('Interrupted. Closing serial port.')
    ser.close()
except Exception as e:
    print(f'Error: {str(e)}')
    ser.close()