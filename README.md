# Assignment2
## Group Members
1. Aakanksha Pharande
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

## Implementation Details

### Generartion of data from simulated IoT Sensors Generate and how it is sent to Azure IoT Hub
The IoT sensors generate data using Python scripts that incorporate randomization. We have three different scripts, each representing a different sensor located at a specific location on the canal. When the scripts are executed, data is generated every 10 seconds for each location. The generated data will be sent to Azure IoT Hub and stored in Blob Storage.

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

The Python script for the sensors is located in the `sensor-simulation` directory within this repository.

### Azure IoT Hub Configuration
To send data to Azure IoT Hub, we first created an IoT Hub named **iot-cst8916** with the pricing tier set to **Free**. After the IoT Hub was created, we added devices by navigating to the **IoT Hub blade** > **Device Management** > **Devices** > **Add Device**. We registered three sensors, each corresponding to a different location on the canal. Each sensor is assigned a unique primary connection string, which is used in the respective Python scripts to send data to the IoT Hub.

For the endpoint configuration, we selected the default **Device-to-cloud endpoint**, which allows devices to send messages to the IoT Hub. The IoT Hub automatically listens for data sent to this endpoint from the registered devices.

### Azure Blob Storage
Azure Blob Storage will be used to store the sensor data for monitoring purposes. To set up Blob Storage, we first created a storage account named **iotstorage8916**, dedicated to blob storage. Then, we added a container within this storage account and named it **iotoutput**.

### Azure Stream Analytics Job
Stream Analytics will be used to process and store the data in Blob Storage. We created a Stream Analytics job resource in Azure named **processiot**. To configure the job, including the input and output settings, we navigated to the **Job Topology**.

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

