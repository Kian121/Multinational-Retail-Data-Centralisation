from data_extraction import DataExtractor
from data_cleaning import DataCleaning
from database_utils import DatabaseConnector

def main():
    db_connector = DatabaseConnector()
    db_connector.init_db_engine('/Users/kiansemnani/Documents/GitHub/multinational-retail-data-centralisation65/db_creds.yaml')  # Provide the path to your YAML file here
    tables = db_connector.list_db_tables()
    print("Database Tables:", tables)

if __name__ == "__main__":
    main()