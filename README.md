```bash
ping raspberrypi.local
```

Copy ip address and ssh into it

```bash
sss pi@ipaddress
```


```bash
sudo su

raspi-config
```

## Configure Uart to Web Server
```py
import serial
import requests
import json
import time

# Configure your serial port
SERIAL_PORT = '/dev/ttyS0'  # Replace with your actual serial port
BAUD_RATE = 9600  # Replace with your baud rate

# Configure your web server endpoint
SERVER_URL = 'https://airquality.faizan.me/api/store-ccs811-readings'  # Replace with your server URL

# Open serial port
# ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

try:
    while True:
        # Read data from serial port
        if 1 > 0:
        # if ser.in_waiting > 0:
            # data = ser.readline().decode('utf-8').strip()
            # print(f'Received data: {data}')
            
            # Example: Prepare data to send to server
            payload = {
                'temperature': 1,
                'humidity': 1,
                'eco2': 1,
                'tvoc': 1,
                'timestamp': int(time.time())
            }
            
            # Send data to server via POST request
            headers = {'Content-Type': 'application/json'}
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
    # ser.close()
except Exception as e:
    print(f'Error: {str(e)}')
    # ser.close()
```


To run the Python script `uart_to_webserver.py` in the background and ensure it starts automatically after the Raspberry Pi reboots, you can use several methods. Here, I'll show you how to use the `systemd` service, which is a robust and reliable method for managing background processes on Linux systems.

### Step 1: Create the Python Script

Ensure your script is saved in a known location. For example, save it in `/home/pi/uart_to_webserver.py`.

```bash
nano /home/pi/uart_to_webserver.py
```

Copy and paste your Python code into this file and save it.

### Step 2: Create a Systemd Service File

Create a systemd service file to manage your Python script. This file will define how and when your script runs.

```bash
sudo nano /etc/systemd/system/uart_to_webserver.service
```

Add the following content to the service file:

```ini
[Unit]
Description=UART to Webserver Service
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/uart_to_webserver.py
WorkingDirectory=/home/pi
StandardOutput=append:/home/pi/uart_to_webserver.log
StandardError=append:/home/pi/uart_to_webserver.log
Restart=on-failure
RestartSec=10
User=pi

[Install]
WantedBy=multi-user.target

```

### Explanation:

- **Description**: A brief description of your service.
- **After**: Specifies that this service should start after the network is up.
- **ExecStart**: The command to start your Python script. Ensure the path to Python (`/usr/bin/python3`) is correct and the script path is correct.
- **WorkingDirectory**: The working directory for your script.
- **StandardOutput** and **StandardError**: Directs output and error messages to the journal.
- **Restart**: Ensures the service restarts if it fails.
- **User**: The user under which the service will run (`pi` in this case).
- **WantedBy**: Specifies when the service should be started (in this case, when the system reaches `multi-user.target`, a common system state).

### Step 3: Enable and Start the Service

Reload the systemd manager configuration to ensure it recognizes the new service:

```bash
sudo systemctl daemon-reload
```

Enable the service to start on boot:

```bash
sudo systemctl enable uart_to_webserver.service
```

Start the service immediately:

```bash
sudo systemctl start uart_to_webserver.service
```

### Step 4: Verify the Service

Check the status of your service to ensure it is running correctly:

```bash
sudo systemctl status uart_to_webserver.service
```

You should see output indicating that the service is active and running. If there are any errors, they will be displayed here.

### Additional Notes:

- **Logs**: You can check the logs of your service using `journalctl`:

  ```bash
  sudo journalctl -u uart_to_webserver.service
  ```

- **Editing the Script**: If you make changes to your Python script, you can restart the service to apply the changes:

  ```bash
  sudo systemctl restart uart_to_webserver.service
  ```

- **Disabling the Service**: If you need to disable the service from starting at boot:

  ```bash
  sudo systemctl disable uart_to_webserver.service
  ```


## Connect to WIFI

### 1. Check Wi-Fi Interface

First, let's make sure that your Wi-Fi interface is up:

```bash
sudo ifconfig wlan0 up
```

### 2. Scan for Available Networks

Scan for available Wi-Fi networks to make sure your iPhone hotspot is visible:

```bash
sudo iwlist wlan0 scan
```

Look for the SSID `data.sh` in the scan results.

### 3. Check `wpa_supplicant.conf`

Ensure your `wpa_supplicant.conf` file is correctly configured:

```bash
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

The file should look like this:

```plaintext
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=DE

network={
    ssid="data.sh"
    psk="pass"
}

network={
    ssid="UPC9F82B1A"
    psk="password"
}
```

### 4. Restart `wpa_supplicant` Service

Restart the `wpa_supplicant` service to apply the changes:

```bash
sudo systemctl restart wpa_supplicant
```

### 5. Restart Networking Service

Restart the networking service:

```bash
sudo systemctl restart networking
```

### 6. Check the Status

Check the status of the `wpa_supplicant` service to ensure it is running correctly:

```bash
sudo systemctl status wpa_supplicant
```

### 8. Reconfigure Network Interfaces

Reconfigure the network interfaces:

```bash
sudo ifdown wlan0
sudo ifup wlan0
```

### 9. Reboot the Raspberry Pi

Reboot your Raspberry Pi:

```bash
sudo reboot
```

### 10. Check Connection After Reboot

After rebooting, check the network connection status:

```bash
ifconfig wlan0
```

Ensure that `wlan0` has an IP address assigned.

### 11. Logs and Debugging

If it still doesn't connect, check the logs for any errors:

```bash
sudo journalctl -u wpa_supplicant
```
