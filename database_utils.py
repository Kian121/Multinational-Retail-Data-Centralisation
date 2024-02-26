from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    Text,
    inspect,
    text,
)

import yaml


class DatabaseConnector:
    def __init__(self, creds_file, creds_file_destination=None):
        """
        Initialises the DatabaseConnector with paths to the source and (optional) destination credentials files.

        :param creds_file: Path to the YAML file containing the source database credentials.
        :param creds_file_destination: Optional path to the YAML file containing the destination database credentials.
        """
        self.creds_file = creds_file
        self.creds_file_destination = creds_file_destination
        self.readDB = (
            self.creds_file_destination is None
        )  # Set to True if creds_file_destination is None
        self.engine = self.init_db_engine(source=self.readDB)

    def init_db_engine(self, source=True):
        """
        Initialises and returns the database engine using the credentials provided.

        :param source: Boolean flag to determine whether to use the source or destination credentials.
        :return: A SQLAlchemy Engine instance connected to the database.
        """
        creds_file = self.creds_file if source else self.creds_file_destination
        creds = self.read_db_creds(creds_file)
        if source:
            engine = create_engine(
                f"postgresql://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}"
            )
        else:
            engine = create_engine(
                f"postgresql://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}",
                isolation_level="AUTOCOMMIT",
            )
        return engine

    @staticmethod
    def read_db_creds(creds_file):
        """
        Reads the database credentials from a YAML file.

        :param creds_file: Path to the YAML file containing the database credentials.
        :return: A dictionary containing the database credentials.
        """
        with open(creds_file, "r") as file:
            return yaml.safe_load(file)

    def list_db_tables(self):
        """
        Lists all the table names in the database.

        :return: A list of table names.
        """
        inspector = inspect(self.engine)
        return inspector.get_table_names()

    def read_db_table(self, table_name):
        """
        Read a table name in the database.

        :return: A table.
        """
        inspector = inspect(self.engine)
        if inspector.has_table(table_name):
            return inspector.get_columns(table_name)
        else:
            return ""

    def execute_query(self, query):
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query))
                return result
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            return None

    def create_table(self, table_name):

        # Add other columns as needed

        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ();"

        with self.engine.connect() as connection:
            connection.execute(text(create_table_sql))

    def upload_to_db(self, df, table_name):
        """
        Uploads a DataFrame to a specified table in the database, replacing the table if it already exists.

        :param df: A pandas DataFrame containing the data to upload.
        :param table_name: The name of the target table in the database.
        """
        self.create_table(table_name)
        df.to_sql(table_name, self.engine, if_exists="replace", index=False)
