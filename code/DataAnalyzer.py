import pandas as pd



class DataAnalyzer:
    """
    A class to analyze IoT telemetry data.
    """
    def __init__(self, data: pd.DataFrame):
        """
        Initialize the DataAnalyzer with a pandas DataFrame.
        
        Params: 
        data (pd.DataFrame): A pandas DataFrame containing the IoT telemetry data.
        """
        self.data = data

    def check_missing_values(self):
        """
        Check for missing values in the dataset and print the count of missing values for each column.
        """
        missing_values = self.data.isnull().sum()
        print("Missing values in each column:")
        print(missing_values)

    def check_data_types(self):
        """
        Check the data types of each column in the dataset and print them.
        """
        data_types = self.data.dtypes
        print("\nData types of each column:")
        print(data_types)

    def analyze(self):
        """
        Perform analysis on the dataset by checking for missing values and data types.
        """
        self.check_missing_values()
        self.check_data_types()
        print(self.data.head(10))
    
    def remove_duplicates(self):
        """
        Remove duplicate rows from the dataset.
        """
        self.data = self.data.drop_duplicates()
        return self.data

    def get_column_names(self) -> list[str]:
        """
        Return the names of all columns in the dataset.
        """
        return self.data.columns.tolist()
