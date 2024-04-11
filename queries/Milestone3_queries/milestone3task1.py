
from sqlalchemy import text
from database_utils import DatabaseConnector

# Path to YAML file containing database credentials
creds_file_path = '/Users/kiansemnani/Documents/GitHub/multinational-retail-data-centralisation65/pgdb_creds.yaml'

# Create an instance of DatabaseConnector
db_connector = DatabaseConnector(creds_file_path)

# Initialise the database engine
engine = db_connector.init_db_engine(source=True)

# First connection: To find the maximum length for VARCHAR columns
max_lengths = {}
with engine.connect() as connection:
    for column in ['card_number', 'store_code', 'product_code']:
        # Determine data type of the column
        data_type_result = connection.execute(text(f"SELECT data_type FROM information_schema.columns WHERE table_name = 'orders_table' AND column_name = '{column}'"))
        data_type = data_type_result.scalar()

        # Handle column based on its data type
        if data_type == 'bigint':
            # If the data type is BIGINT, cast it to TEXT to calculate length
            length_result = connection.execute(text(f"SELECT MAX(LENGTH(CAST({column} AS TEXT))) FROM orders_table"))
        else:
            # If the data type is TEXT, use LENGTH directly
            length_result = connection.execute(text(f"SELECT MAX(LENGTH({column})) FROM orders_table"))

        max_length = length_result.scalar()
        max_lengths[column] = max_length

# Second connection: To change data types
with engine.connect() as connection:
    with connection.begin():
        # Update TEXT to UUID for date_uuid and user_uuid
        connection.execute(text("ALTER TABLE orders_table ALTER COLUMN date_uuid TYPE UUID USING (date_uuid::uuid)"))
        connection.execute(text("ALTER TABLE orders_table ALTER COLUMN user_uuid TYPE UUID USING (user_uuid::uuid)"))

        # Update TEXT to VARCHAR for card_number, store_code, product_code
        for column, length in max_lengths.items():
            connection.execute(text(f"ALTER TABLE orders_table ALTER COLUMN {column} TYPE VARCHAR({length})"))

        # Update BIGINT to SMALLINT for product_quantity
        connection.execute(text("ALTER TABLE orders_table ALTER COLUMN product_quantity TYPE SMALLINT"))

print("Data types changed successfully.")
