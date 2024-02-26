from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from database_utils import DatabaseConnector

# Path to YAML file containing database credentials
creds_file_path = '/Users/kiansemnani/Documents/GitHub/multinational-retail-data-centralisation65/pgdb_creds.yaml'

# Create an instance of DatabaseConnector
db_connector = DatabaseConnector(creds_file_path)

# Initialise the database engine
engine = db_connector.init_db_engine(source=True)

try:
    with engine.connect() as connection:
        # Delete rows where month has more than 2 characters
        connection.execute(text("""
            DELETE FROM dim_date_times
            WHERE LENGTH(month) > 2
        """))
        print("Rows with month length greater than 2 characters deleted.")

        # Alter the data types of columns in dim_date_times
        connection.execute(text("""
            ALTER TABLE dim_date_times
            ALTER COLUMN month TYPE VARCHAR(2),
            ALTER COLUMN year TYPE VARCHAR(4),
            ALTER COLUMN day TYPE VARCHAR(2),
            ALTER COLUMN time_period TYPE VARCHAR(10), -- Adjust the length as needed
            ALTER COLUMN date_uuid TYPE UUID USING (date_uuid::uuid)
        """))
        print("Data types of columns in dim_date_times table changed successfully.")

        # Commit the changes
        connection.commit()

    print("dim_date_times table updates completed successfully.")

except SQLAlchemyError as e:
    print("An error occurred:", e)

