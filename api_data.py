import yaml
from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning

# Load API key from the YAML file
with open('/Users/kiansemnani/Documents/GitHub/multinational-retail-data-centralisation65/api_creds.yaml', 'r') as file:
    creds = yaml.safe_load(file)
api_key = creds['api_key']

# API details
headers = {'x-api-key': api_key}
number_stores_url = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
store_details_url = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{}'

# Initialize classes
data_extractor = DataExtractor()
data_cleaner = DataCleaning()
db_connector = DatabaseConnector('/Users/kiansemnani/Documents/GitHub/multinational-retail-data-centralisation65/pgdb_creds.yaml')

# Get the number of stores
number_of_stores = data_extractor.list_number_of_stores(number_stores_url, headers)

if number_of_stores:
    # Retrieve and store all store data
    stores_df = data_extractor.retrieve_stores_data(store_details_url, headers, number_of_stores)

    # Clean the data
    cleaned_stores_df = data_cleaner.clean_store_data(stores_df)

    # Upload the data to the database
    db_connector.upload_to_db(cleaned_stores_df, 'dim_store_details')
    print("Store data uploaded successfully to 'dim_store_details'.")
else:
    print("Failed to retrieve the number of stores.")

