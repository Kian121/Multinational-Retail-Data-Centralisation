
# Update the last table for the card details.

# +------------------------+-------------------+--------------------+
# |    dim_card_details    | current data type | required data type |
# +------------------------+-------------------+--------------------+
# | card_number            | TEXT              | VARCHAR(?)         |
# | expiry_date            | TEXT              | VARCHAR(?)         |
# | date_payment_confirmed | TEXT              | DATE               |
# +------------------------+-------------------+--------------------+

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
        # Update date_payment_confirmed to NULL for non-date values
        connection.execute(text("""
            UPDATE dim_card_details
            SET date_payment_confirmed = CASE
                WHEN date_payment_confirmed ~ '^\d{4}-\d{2}-\d{2}$' THEN date_payment_confirmed
                ELSE NULL
            END
        """))
        print("Invalid date formats in date_payment_confirmed handled.")

        # Alter the data types of columns in dim_card_details
        connection.execute(text("""
            ALTER TABLE dim_card_details
            ALTER COLUMN card_number TYPE VARCHAR(22),
            ALTER COLUMN expiry_date TYPE VARCHAR(5),
            ALTER COLUMN date_payment_confirmed TYPE DATE USING CAST(date_payment_confirmed AS DATE)
        """))
        print("Data types of columns in dim_card_details table changed successfully.")

        # Commit the changes
        connection.commit()

    print("dim_card_details table updates completed successfully.")

except SQLAlchemyError as e:
    print("An error occurred:", e)

