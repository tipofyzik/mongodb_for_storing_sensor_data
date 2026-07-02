import pandas as pd

from DataAnalyzer import DataAnalyzer
from SensorMongoDB import SensorMongoDB



iot_data = pd.read_csv("./data/iot_telemetry_data.csv")
analyze_dataset = True 
if analyze_dataset:
    data_analyzer = DataAnalyzer(iot_data)
    # data_analyzer.analyze()
    iot_data = data_analyzer.remove_duplicates()

    # column_names = data_analyzer.get_column_names()
    # print("\nColumn names:")
    # print(column_names)

# ['ts', 'device', 'co', 'humidity', 'light', 'lpg', 'motion', 'smoke', 'temp'] -- column_names

# Connecting to MongoDB (inside Docker-network or locally)
database = SensorMongoDB()
database.clear()
batch_size = 1000
base_columns = ['ts', 'device', 'temp', 'humidity']
extra_columns = ['ts', 'device','co', 'lpg', 'smoke', 'motion', 'light']

n_records = 5
update_rows = iot_data[:batch_size]
test_rows = update_rows.sample(n=n_records)



# Inserting the base columns into MongoDB in batches
for i in range(0, len(iot_data), batch_size):
    chunk = iot_data[base_columns].iloc[i:i+batch_size]
    database.insert_batch(chunk.to_dict("records"), batch_size=batch_size)
print("Inserted all data into MongoDB in batches of {}.".format(batch_size))

# Checking the latest records in MongoDB
print (f"Random {n_records} records before adding extra columns")
for i, last_record in enumerate(database.get_by_keys(keys = list(zip(test_rows["ts"], test_rows["device"])))):
    print(f"Record {i+1}: {last_record}")



# Adding extra columns to the existing records in MongoDB
for i in range(0, len(update_rows), batch_size):
    chunk = update_rows[extra_columns].iloc[i:i+batch_size]
    database.update_batch(chunk.to_dict("records"))

# Checking the latest records in MongoDB
print (f"\nRandom {n_records} records after adding extra columns")
for i, last_record in enumerate(database.get_by_keys(keys = list(zip(test_rows["ts"], test_rows["device"])))):
    print(f"Record {i+1}: {last_record}")
