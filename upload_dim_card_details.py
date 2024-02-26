from data_extraction import DataExtractor
from data_cleaning import DataCleaning
from database_utils import DatabaseConnector
from config import DB_CREDS_PATH_LOCAL, DB_CREDS_PATH_AWS
import pandas as pd
from logger_setup import setup_logging
import logging


def process_pdf_data():
    logging.info("Starting the PDF data extraction process")

    # Initialize data extraction, cleaning, and database connectors
    data_cleaner = DataCleaning()
    db_connector = DatabaseConnector(DB_CREDS_PATH_AWS, DB_CREDS_PATH_LOCAL)
    data_extractor = DataExtractor(db_connector)

    # Extract data from PDF file
    pdf_url = "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
    logging.info(f"Extracting data from PDF located at: {pdf_url}")
    extracted_data = data_extractor.retrieve_pdf_data(pdf_url)

    # Check if the data is extracted in the form of a DataFrame
    if isinstance(extracted_data, pd.DataFrame):
        logging.info("Data extracted successfully. Now cleaning the data")

        # Clean the extracted data
        cleaned_data = data_cleaner.clean_card_data(extracted_data)
        logging.info("Data cleaned successfully. Now uploading to the database")

        # Upload cleaned data to the 'dim_card_details' table in your database
        db_connector.upload_to_db(cleaned_data, "dim_card_details")
        logging.info("Data uploaded successfully to table.")
    else:
        logging.error(
            "No data extracted from the PDF. Please check the PDF URL and the extraction method."
        )


if __name__ == "__main__":
    setup_logging()
    process_pdf_data()
