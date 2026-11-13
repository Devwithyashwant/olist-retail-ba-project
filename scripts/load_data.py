"""
Loads all Olist e-commerce CSV files into SQL Server (OlistRetail database).
Run this once after the CSVs are in data/raw/ and the OlistRetail database exists.
"""

import pandas as pd
from sqlalchemy import create_engine

# --- Connection settings ---
SERVER = "localhost"
PORT = 1434
DATABASE = "OlistRetail"
USERNAME = "sa"
PASSWORD = "Yashwant11pass"

connection_string = (
    f"mssql+pymssql://{USERNAME}:{PASSWORD}@{SERVER}:{PORT}/{DATABASE}"
)

engine = create_engine(connection_string)

# --- Map each CSV file to the table name it should become ---
files_to_tables = {
    "data/raw/olist_customers_dataset.csv": "customers",
    "data/raw/olist_geolocation_dataset.csv": "geolocation",
    "data/raw/olist_order_items_dataset.csv": "order_items",
    "data/raw/olist_order_payments_dataset.csv": "order_payments",
    "data/raw/olist_order_reviews_dataset.csv": "order_reviews",
    "data/raw/olist_orders_dataset.csv": "orders",
    "data/raw/olist_products_dataset.csv": "products",
    "data/raw/olist_sellers_dataset.csv": "sellers",
    "data/raw/product_category_name_translation.csv": "product_category_translation",
}

for file_path, table_name in files_to_tables.items():
    print(f"Loading {file_path} -> {table_name} ...")
    df = pd.read_csv(file_path)
    df.to_sql(
        table_name,
        con=engine,
        if_exists="replace",   # drops and recreates the table each run
        index=False,
        chunksize=5000,        # avoids memory issues on the larger files
    )
    print(f"  done: {len(df)} rows loaded into '{table_name}'")

print("\nAll tables loaded successfully.")