import yaml
from logger_setup import setup_logging
import logging
from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning
from config import DB_CREDS_PATH_LOCAL, DB_CREDS_PATH_AWS, API_CREDENTIAL_PATH

# Constants for URLs

NUMBER_STORES_URL = (
    "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores"
)
STORE_DETAILS_URL = (
    "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{}"
)


def load_credentials(file_path: str) -> dict:
    """Load API credentials from a YAML file."""
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def process_api_data():
    """Process API data, extract, clean, and upload to the database."""

    # Loads API key from the YAML file
    creds = load_credentials(API_CREDENTIAL_PATH)
    api_key = creds["api_key"]

    # API details
    headers = {"x-api-key": api_key}

    # Initialises classes
    data_cleaner = DataCleaning()
    db_connector = DatabaseConnector(DB_CREDS_PATH_AWS, DB_CREDS_PATH_LOCAL)
    data_extractor = DataExtractor(db_connector)

    # Gets the number of stores
    number_of_stores = data_extractor.list_number_of_stores(NUMBER_STORES_URL, headers)

    if number_of_stores:
        # Retrieves and stores all store data
        stores_df = data_extractor.retrieve_stores_data(
            STORE_DETAILS_URL, headers, number_of_stores
        )

        # Cleans the data
        cleaned_stores_df = data_cleaner.clean_store_data(stores_df)

        # Uploads the data to the database
        db_connector.upload_to_db(cleaned_stores_df, "dim_store_details")
        logging.info("Store data uploaded successfully to 'dim_store_details'.")
    else:
        logging.error("Failed to retrieve the number of stores.")


if __name__ == "__main__":
    # Call the setup_logging function
    setup_logging()
    process_api_data()
