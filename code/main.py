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
# Data should be cleaned as MongoDB stores as a 
database.clear()
batch_size = 1000
base_columns = ['ts', 'device', 'temp', 'humidity']
extra_columns = ['ts', 'device','co', 'lpg', 'smoke', 'motion', 'light']

n_records = 5
update_rows = iot_data[:batch_size]
test_rows = update_rows.sample(n=n_records)

insert = True
if insert:
    # Inserting the base columns into MongoDB in batches
    database.insert_batch(data_list=iot_data[base_columns].to_dict("records"), batch_size=batch_size)
    print("Inserted all data into MongoDB in batches of {}.".format(batch_size))
    print("\nTotal rows in the dataset: {}".format(len(iot_data)))
    print(f"Total documents in collection: {database.count_documents()}\n")

    # Checking the latest records in MongoDB
    print (f"{n_records} random  records before adding extra columns")
    for i, last_record in enumerate(database.get_by_keys(keys = list(zip(test_rows["ts"], test_rows["device"])))):
        print(f"Record {i+1}: {last_record}")

update = True
if update:
    # Adding extra columns to the existing records in MongoDB
    database.update_batch(update_rows[extra_columns].to_dict("records"))

    # Checking the latest records in MongoDB
    print (f"\n{n_records} random records after adding extra columns")
    for i, last_record in enumerate(database.get_by_keys(keys = list(zip(test_rows["ts"], test_rows["device"])))):
        print(f"Record {i+1}: {last_record}")

# Alternatively, instead of updating existing documents, we can simply add new ones, 
# preserving timestamps and device identifiers, which will help in matching new data with the old one.
alternative = False
if alternative:
    database.insert_batch(data_list=update_rows[extra_columns].to_dict("records"), batch_size=batch_size)

    # Checking the latest records in MongoDB
    print (f"\n{n_records} random records after adding extra columns")
    for i, last_record in enumerate(database.get_by_keys(keys = list(zip(test_rows["ts"], test_rows["device"])))):
        print(f"Record {i+1}: {last_record}")
