from pymongo import MongoClient, InsertOne, UpdateOne



class SensorMongoDB:
    """
    Simple wrapper class for MongoDB sensor data storage.
    Designed for IoT batch ingestion.
    """

    def __init__(self, uri="mongodb://root:example@mongodb:27017/", db_name="sensordb"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db["sensor_readings"]

    # -----------------------------
    # Single insert (for testing)
    # -----------------------------
    def insert_reading(self, data: dict):
        """
        Insert single sensor reading.
        Automatically adds timestamp if missing.

        Params:
            data (dict): A dictionary containing sensor reading data.        
        """
        return self.collection.insert_one(data)

    # -----------------------------
    # Batch insert (main requirement)
    # -----------------------------
    def insert_batch(self, data_list: list[dict], batch_size: int = 1000):
        """
        Insert sensor data in batches (required by task).
        Much faster than insert_one in loop.

        Params:
            data_list (list[dict]): A list of dictionaries containing sensor reading data.
            batch_size (int): Number of records to insert in each batch. Default is 1000.
        """
        operations = []

        for _, item in enumerate(data_list):
            operations.append(InsertOne(item))

            # flush batch
            if len(operations) >= batch_size:
                self.collection.bulk_write(operations)
                operations = []

        # remainder
        if operations:
            self.collection.bulk_write(operations)

    def update_batch(self, data_list: list[dict], batch_size: int = 1000):
        operations = []

        for item in data_list:
            filter_query = {
                "ts": item["ts"],
                "device": item["device"]
            }

            update_fields = {
                k: v for k, v in item.items()
                if k not in ["ts", "device"]
            }

            operations.append(
                UpdateOne(
                    filter_query,
                    {"$set": update_fields},
                    upsert=False
                )
            )
            

            if len(operations) >= batch_size:
                results = self.collection.bulk_write(operations, ordered=False)
                print("matched:", results.matched_count)
                print("modified:", results.modified_count)
                operations = []

        if operations:
            self.collection.bulk_write(operations, ordered=False)
        print(f"Updated {len(data_list)} records in batches of {batch_size}.")

    # -----------------------------
    # Query readyings by filter (for testing)
    # -----------------------------
    def get_by_keys(self, keys: list[tuple]):
        """
        keys: [(ts, device), ...]
        """
        return list(
            self.collection.find({
                "$or": [
                    {"ts": ts, "device": device}
                    for ts, device in keys
                ]
            })
        )

    def clear(self):
        """
        Delete all data. For testing purposes.
        """
        self.collection.delete_many({})
