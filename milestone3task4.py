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
    # Single connection block
    with engine.connect() as connection:
        # Remove the £ character from the product_price column
        connection.execute(text("""
            UPDATE dim_products
            SET product_price = REPLACE(product_price, '£', '')
        """))
        print("£ character removed from product_price.")

        # Add the new weight_class column
        connection.execute(text("""
            ALTER TABLE dim_products
            ADD COLUMN weight_class VARCHAR(15)
        """))
        print("weight_class column added.")

        # Update the weight_class based on weight
        connection.execute(text("""
            UPDATE dim_products
            SET weight_class = CASE
                WHEN CAST(REGEXP_REPLACE(weight, '[^0-9.]', '', 'g') AS NUMERIC) < 2 THEN 'Light'
                WHEN CAST(REGEXP_REPLACE(weight, '[^0-9.]', '', 'g') AS NUMERIC) >= 2 AND CAST(REGEXP_REPLACE(weight, '[^0-9.]', '', 'g') AS NUMERIC) < 40 THEN 'Mid_Sized'
                WHEN CAST(REGEXP_REPLACE(weight, '[^0-9.]', '', 'g') AS NUMERIC) >= 40 AND CAST(REGEXP_REPLACE(weight, '[^0-9.]', '', 'g') AS NUMERIC) < 140 THEN 'Heavy'
                WHEN CAST(REGEXP_REPLACE(weight, '[^0-9.]', '', 'g') AS NUMERIC) >= 140 THEN 'Truck_Required'
                ELSE 'Unknown'
            END
        """))
        print("weight_class column updated.")

        # Commit the transaction
        connection.commit()

    print("dim_products table updates completed successfully.")

except SQLAlchemyError as e:
    print("An error occurred:", e)

