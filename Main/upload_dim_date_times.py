import pandas as pd
import requests
from database_utils import DatabaseConnector
from data_cleaning import DataCleaning
from config import DB_CREDS_PATH_LOCAL, DB_CREDS_PATH_AWS
from logger_setup import setup_logging
import logging


def extract_dim_date():
    # Initialise the database connector
    db_connector = DatabaseConnector(DB_CREDS_PATH_AWS, DB_CREDS_PATH_LOCAL)
    # Download JSON data
    json_url = (
        "https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json"
    )
    response = requests.get(json_url)
    data = response.json()

    # Load into DataFrame
    sales_data_df = pd.DataFrame(data)

    # Clean the data
    data_cleaner = DataCleaning()
    cleaned_sales_data_df = data_cleaner.clean_data_general(sales_data_df)

    # Upload to the database
    db_connector.upload_to_db(cleaned_sales_data_df, "dim_date_times")
    logging.info("Sales data uploaded successfully to 'dim_date_times' table.")


if __name__ == "__main__":
    setup_logging()
    extract_dim_date()


    