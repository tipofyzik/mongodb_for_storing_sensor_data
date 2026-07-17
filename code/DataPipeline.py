from DataAnalyzer import DataAnalyzer
from SensorMongoDB import SensorMongoDB

import pandas as pd

#TODO As a data analyst, I want to retrieve historical sensor measurements efficiently 
# so that I can analyze environmental trends.

class DataPipeline:
    """
    A class to handle the data pipeline for IoT telemetry data.
    """
    def __init__(self):
        """
        Initialize the DataPipeline with a pandas DataFrame.
        
        Params: 
            data (pd.DataFrame): A pandas DataFrame containing the IoT telemetry data.
        """
        self.iot_data = pd.read_csv("./data/iot_telemetry_data.csv")
        self.batch_size = 1000
        self.base_columns = ['ts', 'device', 'temp', 'humidity']
        self.extra_columns = ['ts', 'device','co', 'lpg', 'smoke', 'motion', 'light']

        self.n_records = 5
        self.update_rows = self.iot_data[:self.batch_size]
        self.test_rows = self.update_rows.sample(n=self.n_records)

    def analyze_and_clean_data(self, strategy: str = "drop"):
        """
        Analyze and clean the IoT telemetry data.
        """
        data_analyzer = DataAnalyzer(self.iot_data)
        data_analyzer.analyze()
        data_analyzer.handle_missing_values(strategy=strategy)
        self.iot_data = data_analyzer.remove_duplicates()

    def connect_to_database(self):
        """
        Connect to the MongoDB database and check the connection.
        """
        self.database = SensorMongoDB()
        if not self.database.check_connection():
            raise ConnectionError("Failed to connect to MongoDB.")

    def clear_database(self):
        """
        Clear the MongoDB database.
        It should be cleaned as MongoDB stores 
        """
        self.database.clear()

    def check_latest_records(self):
        """
        Check the latest records in MongoDB based on the test rows.
        """
        print(f"\n{self.n_records} random records before adding extra columns")
        for i, last_record in enumerate(self.database.get_by_keys(keys=list(zip(self.test_rows["ts"], self.test_rows["device"])))):
            print(f"Record {i+1}: {last_record}")

    def insert_data_in_batches(self):
        """
        Insert the base columns of the IoT telemetry data into MongoDB in batches.
        """
        self.database.insert_batch(data_list=self.iot_data[self.base_columns].to_dict("records"), 
                                   batch_size=self.batch_size)
        print("Inserted all data into MongoDB in batches of {}.".format(self.batch_size))
        print("\nTotal rows in the dataset: {}".format(len(self.iot_data)))
        print(f"Total documents in collection: {self.database.count_documents()}\n")
        self.check_latest_records()

    def update_existing_records(self):
        """
        Update existing records in MongoDB with extra columns.
        """
        self.database.update_batch(data_list=self.update_rows[self.extra_columns].to_dict("records"),
                                   batch_size=self.batch_size)
        self.check_latest_records()

    def alternative_update_strategy(self):
        """
        An alternative strategy to update existing records in MongoDB by adding new documents.
        This preserves timestamps and device identifiers, which helps in matching new data with old data.
        """
        self.database.insert_batch(data_list=self.update_rows[self.extra_columns].to_dict("records"), 
                                   batch_size=self.batch_size)
        self.database.check_connection()
        self.check_latest_records()

    def retrieve_by_unique_value(self, key: str):
        values = self.database.get_unique_values(key)
        print(f"\nUnique values for {key}:")
        for i, value in enumerate(values):
            print(f"{i+1}. {value}")
        selected = int(input("Select value number: ")) - 1
        selected_value = values[selected]
        records = self.database.get_by_field(
            key,
            selected_value
        )
        print(f"\nFound {len(records)} records")
        for record in records[:5]:
            print(record)