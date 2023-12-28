import pandas as pd
import requests
from database_utils import DatabaseConnector
from data_cleaning import DataCleaning

# Initialize the database connector
db_connector = DatabaseConnector('/Users/kiansemnani/Documents/GitHub/multinational-retail-data-centralisation65/pgdb_creds.yaml')

# Download JSON data
json_url = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json'
response = requests.get(json_url)
data = response.json()

# Load into DataFrame
sales_data_df = pd.DataFrame(data)

# Clean the data
data_cleaner = DataCleaning()
cleaned_sales_data_df = data_cleaner.clean_data_general(sales_data_df)  # Assumes you have a method for cleaning sales data

# Upload to the database
db_connector.upload_to_db(cleaned_sales_data_df, 'dim_date_times')
print("Sales data uploaded successfully to 'dim_date_times' table.")