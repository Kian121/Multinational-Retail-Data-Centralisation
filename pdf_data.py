from data_extraction import DataExtractor
from data_cleaning import DataCleaning
from database_utils import DatabaseConnector
import pandas as pd

def process_pdf_data():
    print("Starting the PDF data extraction process...")
    data_extractor = DataExtractor()
    data_cleaner = DataCleaning()
    db_connector = DatabaseConnector('/Users/kiansemnani/Documents/GitHub/multinational-retail-data-centralisation65/pgdb_creds.yaml') 

    # Extracts data from PDF file
    pdf_url = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf'
    print(f"Extracting data from PDF located at: {pdf_url}")
    extracted_data = data_extractor.retrieve_pdf_data(pdf_url)

    # Checks if the data is extracted in the form of a DataFrame
    if isinstance(extracted_data, pd.DataFrame):
        print("Data extracted successfully. Now cleaning the data...")
        
        # Cleans the extracted data
        cleaned_data = data_cleaner.clean_card_data(extracted_data)  # Use the appropriate cleaning method
        print("Data cleaned successfully. Now uploading to the database...")

        # Uploads cleaned data to the 'dim_users' table in your database
        db_connector.upload_to_db(cleaned_data, 'dim_card_details')
        print("Data uploaded successfully to table.")
    else:
        print("No data extracted from the PDF. Please check the PDF URL and the extraction method.")

if __name__ == "__main__":
    process_pdf_data()
