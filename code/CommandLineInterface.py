from DataPipeline import DataPipeline
import questionary as q



class CommandLineInterface:

    def __init__(self):
        self.pipeline = DataPipeline()

    def start_menu(self):
        choice_handler = {
            "Analyze and clean data": self.analyze_data,
            "Connect to database": self.connect_database,
            "Clear database": self.clear_database,
            "Insert sensor data": self.insert_data,
            "Update existing records": self.update_records,
            "Alternative update strategy": self.alternative_update,
            "Database information": self.database_information,
            "Retrieve records": self.retrieve_records,
            "View logs": self.view_logs,
            "Quit": self.quit_program
        }

        question = q.select(
            "What do you want to do?",
            choices=[
                "Analyze and clean data",
                "Connect to database",
                "Clear database",
                "Insert sensor data",
                "Update existing records",
                "Alternative update strategy",
                "Database information",
                "Retrieve records",
                "View logs",
                "Quit"
            ]
        ).ask()
        choice_handler[question]()


    def analyze_data(self):
        strategy = q.select(
            "Select missing values handling strategy:",
            choices=[
                "drop",
                "fill"
            ]
        ).ask()
        self.pipeline.analyze_and_clean_data(strategy = strategy)
        print("Data was analyzed, cleaned and duplicates were removed.")

    def connect_database(self):
        try:
            self.pipeline.connect_to_database()
            print("MongoDB connection established.")
        except ConnectionError as error:
            print(error)

    def clear_database(self):
        choice_handler = {
            "Yes": self.pipeline.clear_database,
            "No": self.back_to_menu
        }

        question = q.select(
            "Are you sure you want to clear database?",
            choices=[
                "Yes",
                "No"
            ]
        ).ask()

        choice_handler[question]()
        if question == "Yes":
            print("Database successfully cleared.")



    def insert_data(self):
        self.pipeline.insert_data_in_batches()

    def update_records(self):
        self.pipeline.update_existing_records()

    def alternative_update(self):
        self.pipeline.alternative_update_strategy()

    def database_information(self):
        info_handler = {
            "Count documents": self.show_document_count,
            "Return back": self.back_to_menu
        }

        question = q.select(
            "Select information:",
            choices=[
                "Count documents",
                "Return back"
            ]
        ).ask()

        info_handler[question]()



    def show_document_count(self):
        count = self.pipeline.database.count_documents()
        print(
            f"Total documents in collection: {count}"
        )

    def view_logs(self):
        log_file = "./logs/database.log"
        try:
            with open(log_file, "r") as file:
                logs = file.readlines()
            if not logs:
                print("Log file is empty.")
                return
            print("\n===== DATABASE LOGS =====")
            for line in logs[-20:]:
                print(line.strip())
        except FileNotFoundError:
            print("No log file found.")

    def retrieve_records(self):
        fields = ['ts', 'device', 'temp', 'humidity']
        key = q.select(
            "Select field:",
            choices=fields
        ).ask()
        self.pipeline.retrieve_by_unique_value(key)

    def back_to_menu(self):
        pass

    def quit_program(self):
        choice_handler = {
            "Yes": exit,
            "No": self.back_to_menu
        }
        question = q.select(
            "Are you sure you want to quit?",
            choices=[
                "Yes",
                "No"
            ]
        ).ask()
        choice_handler[question]()