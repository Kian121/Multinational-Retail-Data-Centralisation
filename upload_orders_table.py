from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning
from config import DB_CREDS_PATH_LOCAL, DB_CREDS_PATH_AWS
from logger_setup import setup_logging
import logging


def extra_and_clean_orders():
    rds_connector = DatabaseConnector(DB_CREDS_PATH_AWS)
    local_connector = DatabaseConnector(DB_CREDS_PATH_AWS, DB_CREDS_PATH_LOCAL)
    # Initialises classes

    # The DataExtractor class is now initialized with rds_connector
    data_extractor = DataExtractor(rds_connector)

    data_cleaner = DataCleaning()

    # Lists all tables in the database
    tables = rds_connector.list_db_tables()
    logging.info("Available tables in the database: %s", tables)

    order_table_name = "orders_table"

    # Extracts the orders data
    orders_df = data_extractor.read_rds_table(order_table_name)

    # Cleans the orders data
    cleaned_orders_df = data_cleaner.clean_orders_data(orders_df)

    # Uploads the cleaned data to the database
    local_connector.upload_to_db(cleaned_orders_df, "orders_table")
    logging.info("Orders data uploaded successfully to 'orders_table'.")


if __name__ == "__main__":
    setup_logging()
    extra_and_clean_orders()

