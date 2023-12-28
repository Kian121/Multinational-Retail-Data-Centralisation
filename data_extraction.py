import requests
import pandas as pd
import boto3
from io import StringIO
from sqlalchemy import create_engine
import tabula

class DataExtractor:
    def __init__(self):
        # Initialisation
        pass
    
    def extract_from_csv(self, file_path):
        # Reads a CSV file and return it as a DataFrame
        return pd.read_csv(file_path)
    
    def extract_from_api(self, api_url):
        # Makes a GET request to the API and return the response data
        response = requests.get(api_url)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()
    
    def read_rds_table(self, db_connector, table_name):
        engine = db_connector.init_db_engine()
        return pd.read_sql_table(table_name, engine)

    def retrieve_pdf_data(self, pdf_url):
        """
        Extracts data from a PDF file and returns it as a pandas DataFrame.
        :param pdf_url: URL to the PDF file
        :return: DataFrame containing the extracted data
        """
        tables = tabula.read_pdf(pdf_url, pages='all', multiple_tables=True)
        df = pd.concat(tables, ignore_index=True)
        return df
     
    
    def list_number_of_stores(self, number_stores_url, headers):
        response = requests.get(number_stores_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if 'number_stores' in data:
                return int(data['number_stores'])  # Update key here
            else:
                print("Key 'number_stores' not found in response:", data)
                return None
        else:
            print(f"Error retrieving number of stores: {response.status_code}, {response.text}")
            return None


    def retrieve_stores_data(self, store_details_url, headers, number_of_stores):
        stores_data = []
        for store_number in range(1, number_of_stores + 1):
            try:
                url = store_details_url.format(store_number)
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    stores_data.append(response.json())
                else:
                    print(f"Error retrieving data for store {store_number}: {response.status_code}")
            except Exception as e:
                print(f"Exception occurred for store {store_number}: {e}")
        return pd.DataFrame(stores_data)
    
    def extract_from_s3(self, s3_file_path):
        """
        Extracts a CSV file from an S3 bucket and returns it as a pandas DataFrame.
        :param s3_file_path: Full path to the CSV file in the S3 bucket
        :return: pandas DataFrame containing the extracted data
        """
        # Parse the S3 file path to get the bucket name and object key
        bucket_name = s3_file_path.split('/')[2]
        object_key = '/'.join(s3_file_path.split('/')[3:])

        # Initialise an S3 client
        s3_client = boto3.client('s3')

        try:
            # Get the object from the bucket
            csv_obj = s3_client.get_object(Bucket=bucket_name, Key=object_key)
            body = csv_obj['Body'].read().decode('utf-8')
            return pd.read_csv(StringIO(body))
        except Exception as e:
            print(f"Error in S3 data extraction: {e}")
            return None
    