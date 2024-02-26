import logging
from data_extraction import DataExtractor
from data_cleaning import DataCleaning
from database_utils import DatabaseConnector
from config import DB_CREDS_PATH_LOCAL, DB_CREDS_PATH_AWS
from logger_setup import setup_logging


def process_data():
    logging.info("Initialising database connectors")
    rds_connector = DatabaseConnector(DB_CREDS_PATH_AWS)
    local_connector = DatabaseConnector(DB_CREDS_PATH_AWS, DB_CREDS_PATH_LOCAL)

    logging.info("Initialising data extraction and cleaning modules")
    data_extractor = DataExtractor(rds_connector)
    data_cleaner = DataCleaning()

    logging.info("Extracting data from the source database")
    raw_data = data_extractor.read_rds_table("legacy_users")
    logging.info("Cleaning data...")
    clean_data = data_cleaner.clean_user_data(raw_data)
    logging.info("Uploading cleaned data to the destination database")
    local_connector.upload_to_db(clean_data, "dim_users")
    logging.info("Data upload complete.")


if __name__ == "__main__":
    setup_logging()
    process_data()
