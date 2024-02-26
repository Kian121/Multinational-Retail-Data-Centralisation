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
            SELECT COUNT(*) AS numbers_of_sales, SUM(product_quantity) AS product_quantity_count, store_code AS location
            FROM orders_table
            GROUP BY store_code
        """))

        # Prepare a list to hold the results
        sales_data_list = []

        # Append each row to the list
        for row in result:
            sales_data_list.append((row[0], row[1], row[2]))

        # Print the list
        print("+------------------+-------------------------+----------+")
        print("| numbers_of_sales | product_quantity_count  | location |")
        print("+------------------+-------------------------+----------+")
        for item in sales_data_list:
            print(f"| {item[0]:>16} | {item[1]:>23} | {item[2]:<8} |")
        print("+------------------+-------------------------+----------+")

except SQLAlchemyError as e:
    print("An error occurred:", e)
