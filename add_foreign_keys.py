import logging
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from database_utils import DatabaseConnector
from config import DB_CREDS_PATH_LOCAL, TABLES_PRIMARY_KEYS
from logger_setup import setup_logging


def add_foreign_keys():
    # Create an instance of DatabaseConnector
    db_connector = DatabaseConnector(DB_CREDS_PATH_LOCAL)

    # Initialise the database engine
    engine = db_connector.init_db_engine(source=True)

    try:
        with engine.connect() as connection:
            # List of foreign keys and their references in the orders_table
            orders_table_foreign_keys = {
                "fk_user": ("orders_table", "user_uuid", "dim_users"),
                "fk_product": ("orders_table", "product_code", "dim_products"),
                "fk_datetime": ("orders_table", "date_uuid", "dim_date_times"),
                "fk_card": ("orders_table", "card_number", "dim_card_details"),
                "fk_store": ("orders_table", "store_code", "dim_store_details"),
                # ... add other foreign keys and their references here ...
            }

            for fk_name, (table, column, ref_table) in orders_table_foreign_keys.items():
                # Handle non-matching foreign key values
                connection.execute(text(f"""
                    DELETE FROM {table}
                    WHERE {column} NOT IN (SELECT {TABLES_PRIMARY_KEYS[ref_table]} FROM {ref_table})
                """))

                # Add foreign keys to orders_table
                sql = f"ALTER TABLE {table} ADD CONSTRAINT {fk_name} FOREIGN KEY ({column}) REFERENCES {ref_table}({TABLES_PRIMARY_KEYS[ref_table]});"
                connection.execute(text(sql))
                logging.info(f"Foreign key {fk_name} added to {table} referencing {ref_table} on column {column}.")

            # Commit the changes
            connection.commit()

        logging.info("Foreign keys added successfully.")

    except SQLAlchemyError as e:
        logging.error("An error occurred: %s", e)


if __name__ == "__main__":
    setup_logging()
    add_foreign_keys()
