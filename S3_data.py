from data_extraction import DataExtractor
from data_cleaning import DataCleaning
from database_utils import DatabaseConnector

def main():
    data_extractor = DataExtractor()
    data_cleaner = DataCleaning()
    db_connector = DatabaseConnector('/Users/kiansemnani/Documents/GitHub/multinational-retail-data-centralisation65/pgdb_creds.yaml')

    # Extracts data from S3
    s3_file_path = 's3://data-handling-public/products.csv'
    products_df = data_extractor.extract_from_s3(s3_file_path)

    if products_df is not None:
        # Converts product weights
        products_df = data_cleaner.convert_product_weights(products_df)

        # Cleans products data
        cleaned_products_df = data_cleaner.clean_products_data(products_df)

        # Uploads cleaned data to database
        db_connector.upload_to_db(cleaned_products_df, 'dim_products')

        print("Data extraction, cleaning, and upload completed successfully.")

if __name__ == "__main__":
    main()