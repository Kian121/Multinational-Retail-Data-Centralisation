from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning

# Initialize classes
data_extractor = DataExtractor()
data_cleaner = DataCleaning()
rds_connector = DatabaseConnector('/Users/kiansemnani/Documents/GitHub/multinational-retail-data-centralisation65/db_creds.yaml')
local_connector = DatabaseConnector('/Users/kiansemnani/Documents/GitHub/multinational-retail-data-centralisation65/pgdb_creds.yaml')

# Lists all tables in the database
tables = rds_connector.list_db_tables()
print("Available tables in the database:", tables)

order_table_name = 'orders_table' 

# Extracts the orders data
orders_df = data_extractor.read_rds_table(rds_connector, order_table_name)

# Cleans the orders data
cleaned_orders_df = data_cleaner.clean_orders_data(orders_df)

# Uploads the cleaned data to the database
local_connector.upload_to_db(cleaned_orders_df, 'orders_table')
print("Orders data uploaded successfully to 'orders_table'.")
