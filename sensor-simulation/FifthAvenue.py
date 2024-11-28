import time
import random
from azure.iot.device import IoTHubDeviceClient, Message

# Replace this with the connection string for the specific sensor
CONNECTION_STRING = "HostName=iot-cst8916.azure-devices.net;DeviceId=FifthAvenue;SharedAccessKey=UCwL5U8spSf1o2rT5tf0nqwxxEpDt6YnuFBm7BoE8XI="

# Replace this with the location name for the specific sensor
LOCATION = "Fifth Avenue"

# Simulate data for the location
def simulate_data(location):
    return {
        "location": location,
        "iceThickness": round(random.uniform(15.0, 35.0), 2),
        "surfaceTemperature": round(random.uniform(-5.0, 5.0), 2),
        "snowAccumulation": round(random.uniform(0, 10), 2),
        "externalTemperature": round(random.uniform(-10.0, 5.0), 2),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

# Send data to Azure IoT Hub
def send_data(client, location):
    while True:
        data = simulate_data(location)
        message = Message(str(data))
        client.send_message(message)
        print(f"Sent data from {location}: {data}")
        time.sleep(10)

# Main function to connect to IoT Hub and send data
def main():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    try:
        print(f"Starting simulation for {LOCATION}")
        send_data(client, LOCATION)
    except KeyboardInterrupt:
        print("Simulation stopped.")
    finally:
        client.disconnect()

# Run the script
if __name__ == "__main__":
    main()
