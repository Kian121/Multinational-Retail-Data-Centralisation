import logging
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from database_utils import DatabaseConnector
from config import DB_CREDS_PATH_LOCAL, TABLES_PRIMARY_KEYS
from logger_setup import setup_logging


def add_primary_keys():
    # Create an instance of DatabaseConnector
    db_connector = DatabaseConnector(DB_CREDS_PATH_LOCAL)

    # Initialise the database engine
    engine = db_connector.init_db_engine(source=True)

    try:
        with engine.connect() as connection:

            for table, pk_column in TABLES_PRIMARY_KEYS.items():
                # SQL to add primary key
                sql = f"ALTER TABLE {table} ADD PRIMARY KEY ({pk_column});"
                connection.execute(text(sql))
                logging.info(f"Primary key added to {table} on column {pk_column}.")

            # Commit the changes
            connection.commit()

        logging.info("Primary keys added to dimension tables successfully.")

    except SQLAlchemyError as e:
        logging.error("An error occurred: %s", e)


if __name__ == "__main__":
    setup_logging()
    add_primary_keys()
