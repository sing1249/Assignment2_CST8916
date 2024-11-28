# Assignment 2: Real-time Monitoring System for Rideau Canal Skateway

## Group Members
1. Aakanksha Pharande (041075173)
2. Vrinda Dua
3. Talwinder Singh (040952048)

## Scenario Description:
The Rideau Canal Skateway is one of the world's largest natural ice skating venues, attracting thousands of visitors each winter. To ensure the safety of skaters, continuous monitoring of ice and weather conditions is crucial. Dynamic factors like ice thickness, surface temperature, and snow accumulation can rapidly change, making it essential to assess these metrics in real time to determine if the Skateway is safe for public use.
### How it solves the problem:
This project deploys simulated IoT sensors at three key locations along the Rideau Canal: Dow's Lake, Fifth Avenue, and the NAC. These sensors provide live updates on critical parameters, including:

Ice Thickness: Ensures the ice meets safety standards for skating. <br>
Surface Temperature: Detects early signs of ice melting risks. <br>
Snow Accumulation: Assesses the impact of snow on ice stability. <br>
External Temperature: Provides context for overall weather conditions. <br>
<br>
The collected data is processed in real time using Azure Stream Analytics and stored in Azure Blob Storage. This real-time processing enables the National Capital Commission (NCC) to identify hazards quickly, take immediate action, and maintain a safe environment for skaters. Additionally, the stored data offers valuable insights for historical analysis, helping to improve long-term safety and maintenance protocols.

By leveraging continuous monitoring and data-driven decision-making, this solution enhances the safety and reliability of the Rideau Canal Skateway for everyone.

## System Architecture
![System Architecture Diagram](/system_architecture_diagram.png)

## Implementation Details

### IoT Sensor Simulation
The IoT sensors generate data using Python scripts that incorporate randomization. To simulate IoT sensors for the Rideau Canal Skateway, we created three different scripts, each representing a different sensor located at a specific location on the canal. When the scripts are executed, data is generated every 10 seconds for each location. The generated data will be sent to Azure IoT Hub and stored in Blob Storage.

The JSON payload example sent includes the randomization of sensor data as follows:

```json
{
    "location": location,
    "iceThickness": round(random.uniform(15.0, 35.0), 2),
    "surfaceTemperature": round(random.uniform(-5.0, 5.0), 2),
    "snowAccumulation": round(random.uniform(0, 10), 2),
    "externalTemperature": round(random.uniform(-10.0, 5.0), 2),
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
}
```
The following Python script was used to simulate the telemetry data and send it to the Azure IoT Hub. The script generates random data for parameters such as ice thickness, surface temperature, snow accumulation, and external temperature every 10 seconds. The `CONNECTION_STRING` in the script was replaced for each specific location (e.g., Dow's Lake, Fifth Avenue, NAC) to ensure that each simulated IoT sensor sends data to its corresponding IoT Hub device.
The three Python scripts for different locations are included in the `sensor-simulation` directory within this repository.

```python
import time
import random
from azure.iot.device import IoTHubDeviceClient, Message

# Replace this with the connection string for the specific sensor
CONNECTION_STRING = "IoT Hub device connection string here"

# Replace this with the location name for the specific sensor
LOCATION = "location-name"

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
        client
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
```
### Azure IoT Hub Configuration
To send data to Azure IoT Hub, we first created an IoT Hub named **iot-cst8916** with the pricing tier set to **Free**. After the IoT Hub was created, we added devices by navigating to the **IoT Hub blade** > **Device Management** > **Devices** > **Add Device**. We registered three sensors, each corresponding to a different location on the canal. Each sensor is assigned a unique primary connection string, which is used in the respective Python scripts to send data to the IoT Hub.

For the endpoint configuration, we selected the default **Device-to-cloud endpoint**, which allows devices to send messages to the IoT Hub. The IoT Hub automatically listens for data sent to this endpoint from the registered devices.

### Azure Blob Storage
Azure Blob Storage will be used to store the sensor data for monitoring purposes. To set up Blob Storage, we first created a storage account named **iotstorage8916**, dedicated to blob storage. Then, we added a container within this storage account and named it **iotoutput**. The data will be stored in this container in json format. 

### Azure Stream Analytics Job
Stream Analytics will be used to process and store the data in Blob Storage. We created a Stream Analytics job resource in Azure named **processiot**. To configure the job, including the input and output settings, we navigated to the **Job Topology** which is described in further steps.

## Usage Instructions

### Running the IoT Sensor Simulation
To run the scripts for each sensor through VS Code, follow these steps:

1. Switch to the directory `sensor-simulation`, which contains the Python code for all 3 sensors and the `requirements.txt` file.
2. Create a virtual environment in VS Code WSL using the following steps:
    - Open Command Palette
    - Select **Python: Create Environment** > **Venv**
    - Choose the Python version
    - Choose the file with dependencies, which is `requirements.txt`. The dependencies in this case include the installation of the `azure.iot.device` module.
    - After the module is installed, a virtual environment will be created.
3. After the virtual environment is set up, open 3 separate terminals and run the following commands:
    - ```python DowsLake.py```
    - ```python FifthAvenue.py```
    - ```python NAC.py```
    
    These commands will run the scripts and simulate the sensors sending data to the IoT Hub.

### Configuring Azure Services

#### Setting up the IoT Hub
To set up the IoT Hub to use the script as sensors, follow these steps:

- Use the primary connection string for each sensor in the Python scripts. The primary connection string is used to connect to the sensors.
- Assign the global variable `CONNECTION_STRING` the value of the primary connection string for each respective sensor script.

```python
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
```
#### Setting up the Strem Analytics Job: 
In order to set up the job, we will go into Job Topology and follow the following steps.
- **Setting up the input**  
  In the Job Topology, we selected **Input > Add Input**, and the system automatically detected the input hub, which in our case is **iot-cst8916**. We named this input **"input"**.

- **Setting up the output**  
  In the Job Topology, we selected **Output > Add Output**, and then chose **Blob Storage/ADLS Gen 2**. This allowed us to link the previously created Blob Storage container as the output destination.

- **Query**  
  The following query runs when the job is executed. It aggregates data for each location over a 5-minute window and calculates the following:
  - Average ice thickness
  - Maximum snow accumulation

```sql
SELECT
    location AS Location,
    AVG(iceThickness) AS AvgIceThickness,
    MAX(snowAccumulation) AS MaxSnowAccumulation,
    System.Timestamp AS EventTime
INTO
    [output]
FROM
    [input]
GROUP BY
    location, TumblingWindow(minute, 5)
```
### Accessing Stored Data

When we hit run in the query in the Stream Analytics job the data does not automatically gets stored into the blob storage. In order for it to be stored in the Blob Storage these are the steps we can follow:

1. We will have to start the job. For that we go into Overview Section of the Azure Analyctics. In this case we will go into processiot > overview.
2. We will then start the job there.
3. To access the data, we can go into the storage account and then into the container in the storage account.
4. After that we can open the container that we configured as output source in the Azure Analytics job.
5. After hitting the refresh data, we can see a file that is in json format that will have the data of the job,
6. We can click on the file, it will be downloaded and we can see the data using any JSON viewer.

### Results
The result of the job that ran in the Azure Analytcis processiot will be stored in blob storage. It will have a file in JSON format. After downloading and opening the file it will give us the following data.
We can see that it gives us data for every 5 minutes for each location and we can see the AvgIceThickness and MaxSnowAccumulation. This will help in maintaing safety of people skating on the canal. 

```json
{"Location":"Dow's Lake","AvgIceThickness":26.311333333333334,"MaxSnowAccumulation":9.27,"EventTime":"2024-11-26T20:00:00.0000000Z"}
{"Location":"NAC","AvgIceThickness":24.802333333333333,"MaxSnowAccumulation":9.27,"EventTime":"2024-11-26T20:00:00.0000000Z"}
{"Location":"Fifth Avenue","AvgIceThickness":24.853448275862064,"MaxSnowAccumulation":9.99,"EventTime":"2024-11-26T20:00:00.0000000Z"}
{"Location":"Dow's Lake","AvgIceThickness":25.33724137931034,"MaxSnowAccumulation":9.83,"EventTime":"2024-11-26T20:05:00.0000000Z"}
{"Location":"NAC","AvgIceThickness":24.541379310344833,"MaxSnowAccumulation":9.8,"EventTime":"2024-11-26T20:05:00.0000000Z"}
{"Location":"Fifth Avenue","AvgIceThickness":24.728333333333335,"MaxSnowAccumulation":9.51,"EventTime":"2024-11-26T20:05:00.0000000Z"}
{"Location":"Dow's Lake","AvgIceThickness":25.786666666666658,"MaxSnowAccumulation":9.82,"EventTime":"2024-11-26T20:10:00.0000000Z"}
{"Location":"NAC","AvgIceThickness":25.391333333333343,"MaxSnowAccumulation":9.78,"EventTime":"2024-11-26T20:10:00.0000000Z"}
{"Location":"Fifth Avenue","AvgIceThickness":26.287999999999993,"MaxSnowAccumulation":9.86,"EventTime":"2024-11-26T20:10:00.0000000Z"}
{"Location":"Dow's Lake","AvgIceThickness":25.585333333333327,"MaxSnowAccumulation":9.93,"EventTime":"2024-11-26T20:15:00.0000000Z"}
{"Location":"NAC","AvgIceThickness":24.387931034482765,"MaxSnowAccumulation":9.94,"EventTime":"2024-11-26T20:15:00.0000000Z"}
{"Location":"Fifth Avenue","AvgIceThickness":24.012068965517248,"MaxSnowAccumulation":9.65,"EventTime":"2024-11-26T20:15:00.0000000Z"}
```
### Reflection
Setting up the IoT Hub and configuring the message routing was pretty straightforward because we had already seen a demo of the process in class. However, one challenge we faced was ensuring the Stream Analytics query aggregated the data correctly over a 5-minute window. While the concept was clear, getting the syntax right and testing the output took some trial and error. With a bit of experimentation and referring to Azure documentation, we were able to resolve the issue and successfully process the data.

