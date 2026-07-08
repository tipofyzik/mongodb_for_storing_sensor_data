# Mongo database for storing IoT sensor data

To run this project, follow the instruction below:
1. Download the repository "code", download [Environmental Sensor Telemetry Data](https://www.kaggle.com/datasets/garystafford/environmental-sensor-data-132k) from kaggle and put it into "data" folder inside "code" directory.  
2. Download Docker Desktop and run it.  
3. Open CLI or IDE (integrated development environment) in the project directory. Then run "_**docker compose up --build**_" in the console to create docker images and run containers. To stop containers run "_**docker compose down**_".

The program automatically loads the initial dataset with four primary columns (ts, device, temp, humidity) into MongoDB. For testing purposes, it then updates only the first 1,000 rows by adding the remaining columns (co, lpg, smoke, motion, light). Finally, to demonstrate that the process works correctly, the program displays five randomly selected records from the updated subset both before and after the update.

## Usage scenario
**Environmental Monitoring System for a Municipality**  
The goal of the system is to collect and store data from environmental sensors installed across a city. The collected measurements are used to monitor air quality, detect unusual environmental conditions, and support future analysis. The system receives sensor measurements from multiple devices. Initially, sensors provide basic measurements such as temperature and humidity. Over time, additional sensors may be installed to measure parameters such as carbon monoxide, smoke, LPG, motion, and light levels.  

**User stories:**  
_City operator:_  
As a city operator, I want sensor measurements to be stored automatically so that I can access historical environmental data.  
As a city operator, I want new sensor types to be added without changing the whole database structure so that the system can be expanded in the future.  
As a city operator, I want incorrect or missing sensor data to be detected so that unreliable measurements do not affect further analysis.

_Maintenance engineer:_  
As a maintenance engineer, I want to verify that sensors are sending data regularly so that malfunctioning devices can be identified quickly.  
As a maintenance engineer, I want the data ingestion service to report errors when the database is unavailable so that problems can be resolved.

_Data analyst_  
As a data analyst, I want to retrieve historical sensor measurements efficiently so that I can analyze environmental trends.  
