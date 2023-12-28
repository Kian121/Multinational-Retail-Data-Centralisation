from sqlalchemy import create_engine, inspect
import yaml

class DatabaseConnector:
    def __init__(self, creds_file, creds_file_destination=None):
        self.creds_file = creds_file
        self.creds_file_destination = creds_file_destination

    def init_db_engine(self, source=True):
        creds_file = self.creds_file if source else self.creds_file_destination
        creds = self.read_db_creds(creds_file)
        engine = create_engine(f"postgresql://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}")
        return engine

    @staticmethod
    def read_db_creds(creds_file):
        with open(creds_file, 'r') as file:
            return yaml.safe_load(file)

    def list_db_tables(self):
        engine = self.init_db_engine()
        inspector = inspect(engine)
        return inspector.get_table_names()
        
    def upload_to_db(self, df, table_name):
        engine = self.init_db_engine()
        df.to_sql(table_name, engine, if_exists='replace', index=False)