# Mongo database for storing IoT sensor data

To run this project, follow the instruction below:
1. Download the repository "code", download [Environmental Sensor Telemetry Data](https://www.kaggle.com/datasets/garystafford/environmental-sensor-data-132k) from kaggle and put it into "data" folder inside "code" directory.  
2. Download Docker Desktop and run it.  
3. Open CLI or IDE (integrated development environment) in the project directory. Then run "_**docker compose up -d --build**_" in the console to create docker images and run containers in the background. To stop containers run "_**docker compose down**_".
4. In order to start the program itself and interact with the database via CLI, run "_**docker exec -it sensor_loader python main.py**_" in the console. You will get the menu where you can choose among different options. In order to run commands connected to the database (between "Clear database" and "Retrieve records"), connect to the database first:  
<img width="408" height="258" alt="image" src="https://github.com/user-attachments/assets/6aabc325-4693-4681-bc5b-a3e8e6036404" />

Regarding functions:  
When you insert the data, the program loads the initial dataset with only four primary columns (ts, device, temp, humidity) into MongoDB. To add the remained columns into database you can both update existing documents (only the first 1,000 rows for testing purposes) and add them as separate documents. To demonstrate that the process works correctly, the program displays five randomly selected records from the updated subset both before and after the update.

## Usage scenario
**Environmental Monitoring System for a Municipality**  
The goal of the system is to collect and store data from environmental sensors installed across a city. The collected measurements are used to monitor air quality, detect unusual environmental conditions, and support future analysis. The system receives sensor measurements from multiple devices. Initially, sensors provide basic measurements such as temperature and humidity. Over time, additional sensors may be installed to measure parameters such as carbon monoxide, smoke, LPG, motion, and light levels.  

**User stories:**  
_City operator:_  
As a city operator, I want sensor measurements to be stored automatically so that I can access historical environmental data.  
As a city operator, I want new sensor types to be added without changing the whole database structure so that the system can be expanded in the future.  
As a city operator, I want incorrect or missing sensor data to be detected so that unreliable measurements do not affect further analysis.

Solution:  
**Store sensor measurements automatically**
The `DataPipeline` class provides ingestion of IoT telemetry data. The dataset is loaded, processed, and inserted into MongoDB using batch insertion. The `insert_batch()` method in the `SensorMongoDB` class stores measurements in batches of 1,000 records, which improves performance when handling larger datasets.

**Add new sensor types without changing the database structure**
MongoDB was selected because of its flexible document-based structure. Initially, only the core attributes (`ts`, `device`, `temp`, and `humidity`) are stored. Additional sensor attributes (`co`, `lpg`, `smoke`, `motion`, and `light`) are added later using the `update_batch()` method. This demonstrates that new sensor measurements can be introduced without redesigning the database schema.

**Detect incorrect or missing sensor data**
The `DataAnalyzer` class is responsible for data quality checks before ingestion. It analyzes the dataset, detects missing values, removes incomplete records or fills missing values depending on the selected strategy, and removes duplicate measurements before storing the data.
<table>
  <tr>
    <td>
      
    </td>
    <td>
      
    </td>
    <td>
      
    </td>
    <td>
      
    </td>
  </tr>
</table>
---

_Maintenance engineer:_  
As a maintenance engineer, I want the data ingestion service to report errors when the database is unavailable so that problems can be resolved.

Solution:  
The `SensorMongoDB` class implements connection monitoring using the `check_connection()` method. Database operations are wrapped with exception handling, and failures are recorded using Python logging. The system creates log entries containing timestamps, severity levels, and error descriptions, allowing maintenance engineers to investigate problems. Additionally, analysis history and update history logs can be observed, which is important for reviewing of what was already done.
<table>
  <tr>
    <td>
      <img width="395" height="189" alt="image" src="https://github.com/user-attachments/assets/ec668dcf-43cc-48bf-b8b4-80fe952d8520" />
    </td>
    <td>
      <img width="333" height="184" alt="image" src="https://github.com/user-attachments/assets/c9d28cc6-e3cb-442d-a938-488e5d943ca6" />
    </td>
    <td>
      <img width="994" height="484" alt="image" src="https://github.com/user-attachments/assets/4a745a76-e1eb-44fb-b314-b7c2cabd9519" />
    </td>
  </tr>
</table>
---

_Data analyst_  
As a data analyst, I want to retrieve historical sensor measurements efficiently so that I can analyze environmental trends.  

Solution:  
The system provides query methods for retrieving stored measurements from MongoDB. Analysts can retrieve records using specific key combinations (`ts` and `device`) or search by selected sensor attributes. The `get_unique_values()` functionality allows users to retrieve available unique values for a field and then request all historical measurements related to the selected value.  

Example usage:  
An analyst wants to investigate how the temperature changed during a specific period. Using the CLI interface, the analyst selects the temperature sensor, chooses a starting date and hour, and defines the analysis duration (for example, 6 hours or 3 days). The system retrieves the corresponding measurements from MongoDB and provides statistical results that help identify minimym, maximum and average temperature during chose period.

<table>
  <tr>
    <td>
      <img width="396" height="187" alt="image" src="https://github.com/user-attachments/assets/22f152b3-dd65-46f0-ab8c-b64c2a8af0b0" />
    </td>
    <td>
      <img width="389" height="116" alt="image" src="https://github.com/user-attachments/assets/1188e056-4bdf-4023-9f07-22042ec5a094" />
    </td>
    <td>
      <img width="308" height="167" alt="image" src="https://github.com/user-attachments/assets/54a9bbdd-674e-40e3-bbe8-c0f097c6c8e6" />
    </td>
    <td>
      <img width="292" height="231" alt="image" src="https://github.com/user-attachments/assets/8258710f-1e6e-4fdb-a7a2-4189f9900f63" />
    </td>
    <td>
      <img width="296" height="558" alt="image" src="https://github.com/user-attachments/assets/ab4b16fe-a45f-4ac6-ac32-c466433efec7" />
    </td>
    <td>
      <img width="395" height="194" alt="image" src="https://github.com/user-attachments/assets/115cd09c-9875-4ab0-9375-c939c9c583bb" />
    </td>
  </tr>
</table>

