
from sqlalchemy import text
from database_utils import DatabaseConnector

# Path to YAML file containing database credentials
creds_file_path = '/Users/kiansemnani/Documents/GitHub/multinational-retail-data-centralisation65/pgdb_creds.yaml'

# Create an instance of DatabaseConnector
db_connector = DatabaseConnector(creds_file_path)

# Initialise the database engine
engine = db_connector.init_db_engine(source=True)

# Connection: To find the maximum length for VARCHAR columns for country_code
with engine.connect() as connection:
    length_result = connection.execute(text("SELECT MAX(LENGTH(country_code)) FROM dim_users"))
    max_length_country_code = length_result.scalar()

# Connection: To change data types
with engine.connect() as connection:
    with connection.begin():
        # Update TEXT to VARCHAR(255) for first_name and last_name
        connection.execute(text("ALTER TABLE dim_users ALTER COLUMN first_name TYPE VARCHAR(255)"))
        connection.execute(text("ALTER TABLE dim_users ALTER COLUMN last_name TYPE VARCHAR(255)"))

        # Update TEXT to DATE for date_of_birth and join_date
        connection.execute(text("ALTER TABLE dim_users ALTER COLUMN date_of_birth TYPE DATE USING (date_of_birth::DATE)"))
        connection.execute(text("ALTER TABLE dim_users ALTER COLUMN join_date TYPE DATE USING (join_date::DATE)"))

        # Update TEXT to UUID for user_uuid
        connection.execute(text("ALTER TABLE dim_users ALTER COLUMN user_uuid TYPE UUID USING (user_uuid::uuid)"))

        # Update TEXT to VARCHAR for country_code with determined max length
        if max_length_country_code is not None:
            connection.execute(text(f"ALTER TABLE dim_users ALTER COLUMN country_code TYPE VARCHAR({max_length_country_code})"))

print("Data types changed successfully.")