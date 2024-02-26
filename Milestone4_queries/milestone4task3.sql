import logging
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from database_utils import DatabaseConnector

# Enable basic logging
logging.basicConfig(level=logging.INFO)

# Path to your YAML file containing database credentials
creds_file_path = '/Users/kiansemnani/Documents/GitHub/multinational-retail-data-centralisation65/pgdb_creds.yaml'

# Create an instance of DatabaseConnector
db_connector = DatabaseConnector(creds_file_path)

# Initialize the database engine
engine = db_connector.init_db_engine(source=True)

try:
    with engine.connect() as connection:
        logging.info("Connected to the database.")
        
        result = connection.execute(text("""
            SELECT SUM(product_quantity) AS total_sales, date_uuid
            FROM orders_table
            GROUP BY date_uuid
            ORDER BY total_sales DESC
        """))

        if result.rowcount == 0:
            logging.warning("No data found.")
        else:
            logging.info("Data retrieved successfully.")

            # Print the results as a simple list
            for row in result:
                # Accessing row elements by index
                print(f"Month: {row[1]}, Total Sales: {row[0]}")

except SQLAlchemyError as e:
    logging.error("An error occurred: %s", e)
