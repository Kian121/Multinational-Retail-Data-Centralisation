from data_extraction import DataExtractor
from data_cleaning import DataCleaning
from database_utils import DatabaseConnector
from config import DB_CREDS_PATH_LOCAL, DB_CREDS_PATH_AWS
from logger_setup import setup_logging
import logging


def main():

    data_cleaner = DataCleaning()
    db_connector = DatabaseConnector(DB_CREDS_PATH_AWS, DB_CREDS_PATH_LOCAL)
    data_extractor = DataExtractor(db_connector)
    # Extracts data from S3
    s3_file_path = "s3://data-handling-public/products.csv"
    products_df = data_extractor.extract_from_s3(s3_file_path)

    if products_df is not None:
        # Converts product weights
        products_df = data_cleaner.convert_product_weights(products_df)

        # Cleans products data
        cleaned_products_df = data_cleaner.clean_products_data(products_df)

        # Uploads cleaned data to database
        db_connector.upload_to_db(cleaned_products_df, "dim_products")

        logging.info("Data extraction, cleaning, and upload completed successfully.")


if __name__ == "__main__":
    setup_logging()
    main()
