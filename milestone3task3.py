from sqlalchemy import text
from database_utils import DatabaseConnector

# Path to YAML file containing database credentials
creds_file_path = '/Users/kiansemnani/Documents/GitHub/multinational-retail-data-centralisation65/pgdb_creds.yaml'

# Create an instance of DatabaseConnector
db_connector = DatabaseConnector(creds_file_path)

# Initialize the database engine
engine = db_connector.init_db_engine(source=True)

try:
    with engine.connect() as connection:
        with connection.begin():
            # Cleans the data in staff_numbers column
            connection.execute(text("""
                UPDATE dim_store_details
                SET staff_numbers = NULLIF(regexp_replace(staff_numbers, '\D', '', 'g'), '')
            """))

            # Update the data types as per the requirement
            connection.execute(text("""
                ALTER TABLE dim_store_details
                ALTER COLUMN longitude TYPE FLOAT USING longitude::FLOAT,
                ALTER COLUMN locality TYPE VARCHAR(255),
                ALTER COLUMN store_code TYPE VARCHAR(11),  
                ALTER COLUMN staff_numbers TYPE SMALLINT USING CASE WHEN staff_numbers IS NULL THEN NULL ELSE staff_numbers::SMALLINT END,
                ALTER COLUMN opening_date TYPE DATE USING opening_date::DATE,
                ALTER COLUMN store_type TYPE VARCHAR(255),
                ALTER COLUMN latitude TYPE FLOAT USING latitude::FLOAT,
                ALTER COLUMN country_code TYPE VARCHAR(3),  
                ALTER COLUMN continent TYPE VARCHAR(255)
            """))

    print("Database updates completed successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
