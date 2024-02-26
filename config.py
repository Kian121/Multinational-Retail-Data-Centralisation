# config.py

DB_CREDS_PATH_LOCAL = "/Users/kiansemnani/Documents/GitHub/multinational-retail-data-centralisation65/pgdb_creds.yaml"
DB_CREDS_PATH_AWS = "/Users/kiansemnani/Documents/GitHub/multinational-retail-data-centralisation65/db_creds.yaml"
API_CREDENTIAL_PATH = "/Users/kiansemnani/Documents/GitHub/multinational-retail-data-centralisation65/api_creds.yaml"

TABLES_PRIMARY_KEYS = {
    "dim_users": "user_uuid",
    "dim_products": "product_code",
    "dim_date_times": "date_uuid",
    "dim_card_details": "card_number",
    "dim_store_details": "store_code",
    
}