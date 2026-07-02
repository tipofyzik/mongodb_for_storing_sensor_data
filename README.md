# Mongo database for storing IoT sensor data

To run this project, follow the instruction below:
1. Download the repository "code", download [Environmental Sensor Telemetry Data](https://www.kaggle.com/datasets/garystafford/environmental-sensor-data-132k) from kaggle and put it into "data" folder inside "code" directory.  
2. Download Docker Desktop and run it.  
3. Open CLI or IDE (integrated development environment) in the project directory. Then run "docker compose up --build" in the console to create docker images and run containers.

The program automatically loads the initial dataset with four primary columns (ts, device, temp, humidity) into MongoDB. For testing purposes, it then updates only the first 1,000 rows by adding the remaining columns (co, lpg, smoke, motion, light). Finally, to demonstrate that the process works correctly, the program displays five randomly selected records from the updated subset both before and after the update.
