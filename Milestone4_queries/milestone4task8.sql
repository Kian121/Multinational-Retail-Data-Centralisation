from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from database_utils import DatabaseConnector

# Path to your YAML file containing database credentials
creds_file_path = '/Users/kiansemnani/Documents/GitHub/multinational-retail-data-centralisation65/pgdb_creds.yaml'

# Create an instance of DatabaseConnector
db_connector = DatabaseConnector(creds_file_path)

# Initialize the database engine
engine = db_connector.init_db_engine(source=True)

try:
    with engine.connect() as connection:
        result = connection.execute(text("""
            SELECT SUM(sales_amount) AS total_sales, store_type, country_code
            FROM dim_store_details
            WHERE country_code = 'DE'
            GROUP BY store_type, country_code
            ORDER BY total_sales DESC
        """))

        # Prepare a list to hold the results
        sales_data_list = []

        # Append each row to the list
        for row in result:
            sales_data_list.append((row[0], row[1], row[2]))

        # Print the list
        for item in sales_data_list:
            print(f"Total Sales: {item[0]}, Store Type: {item[1]}, Country Code: {item[2]}")

except SQLAlchemyError as e:
    print("An error occurred:", e)
