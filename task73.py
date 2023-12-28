from database_utils import DatabaseConnector

# Initialize the DatabaseConnector
db_connector = DatabaseConnector('/Users/kiansemnani/Documents/GitHub/multinational-retail-data-centralisation65/db_creds.yaml')
# Step 1: List all tables in the database
tables = db_connector.list_db_tables()
print("Available tables in the database:", tables)


#this is to find the table name