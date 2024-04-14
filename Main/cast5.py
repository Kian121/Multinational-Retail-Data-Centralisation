
# Make the changes to the columns to cast them to the following data types:

# +-----------------+--------------------+--------------------+
# |  dim_products   | current data type  | required data type |
# +-----------------+--------------------+--------------------+
# | product_price   | TEXT               | FLOAT              |
# | weight          | TEXT               | FLOAT              |
# | EAN             | TEXT               | VARCHAR(?)         |
# | product_code    | TEXT               | VARCHAR(?)         |
# | date_added      | TEXT               | DATE               |
# | uuid            | TEXT               | UUID               |
# | still_available | TEXT               | BOOL               |
# | weight_class    | TEXT               | VARCHAR(?)         |
# +-----------------+--------------------+--------------------+

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
        # Rename 'removed' column to 'still_available'
        connection.execute(text("""
            ALTER TABLE dim_products
            RENAME COLUMN removed TO still_available
        """))
        print("Column 'removed' renamed to 'still_available'.")

        # Clean product_price, weight, date_added, and uuid columns
        connection.execute(text("""
            UPDATE dim_products
            SET product_price = REGEXP_REPLACE(product_price, '[^0-9.]', '', 'g'),
                weight = REGEXP_REPLACE(weight, '[^0-9.]', '', 'g'),
                date_added = CASE
                    WHEN date_added ~ '^\d{4}-\d{2}-\d{2}$' THEN date_added
                    ELSE NULL
                END,
                uuid = CASE
                    WHEN uuid ~ '^[A-Fa-f0-9]{8}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{12}$' THEN uuid
                    ELSE NULL
                END
        """))
        print("Non-numeric characters removed from product_price and weight, and invalid dates and UUIDs handled.")

        # Delete rows with EAN length greater than 13
        connection.execute(text("""
            DELETE FROM dim_products
            WHERE LENGTH("EAN") > 13
        """))
        print("Rows with EAN length greater than 13 deleted.")

        # Commit the changes
        connection.commit()

    with engine.connect() as connection:
        # Now alter the data types
        connection.execute(text("""
            ALTER TABLE dim_products
            ALTER COLUMN product_price TYPE FLOAT USING CAST(product_price AS FLOAT),
            ALTER COLUMN weight TYPE FLOAT USING CAST(weight AS FLOAT),
            ALTER COLUMN "EAN" TYPE VARCHAR(13),
            ALTER COLUMN product_code TYPE VARCHAR(11),
            ALTER COLUMN date_added TYPE DATE USING CAST(date_added AS DATE),
            ALTER COLUMN uuid TYPE UUID USING (uuid::uuid),
            ALTER COLUMN still_available TYPE BOOL USING CASE WHEN Still_available = 'true' THEN TRUE ELSE FALSE END,
            ALTER COLUMN weight_class TYPE VARCHAR(15)
        """))
        print("Data types of columns in dim_products table changed successfully.")

        # Commit the changes
        connection.commit()

    print("dim_products table updates completed successfully.")

except SQLAlchemyError as e:
    print("An error occurred:", e)

    print("An error occurred:", e)

