import pandas as pd
from sqlalchemy import create_engine
import os

# 1. Database Connection
DB_USER = 'postgres'
DB_PASSWORD = 'DB_PASSWORD = YOUR_PASSWORD_HERE'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'olist_db'

engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
folder_path = r'Brazilian E-Commerce dataset(Olist)'

# 2. ETL Process (Ordered to avoid Foreign Key errors)
files_to_load = [
    'olist_customers_dataset.csv',
    'olist_sellers_dataset.csv',
    'olist_products_dataset.csv',
    'olist_orders_dataset.csv',
    'olist_order_items_dataset.csv'
]

for file in files_to_load:
    file_path = os.path.join(folder_path, file)
    if not os.path.exists(file_path):
        continue

    df = pd.read_csv(file_path)

    # --- DATA CLEANING ---
    df.drop_duplicates(inplace=True)

    if file == 'olist_products_dataset.csv':
        df.rename(columns={
            'product_name_lenght': 'product_name_length',
            'product_description_lenght': 'product_description_length'
        }, inplace=True)

        numeric_cols = ['product_name_length', 'product_description_length', 'product_photos_qty', 'product_weight_g',
                        'product_length_cm', 'product_height_cm', 'product_width_cm']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].fillna(0)

    if 'product_category_name' in df.columns:
        df['product_category_name'] = df['product_category_name'].fillna('Unknown')

    if 'price' in df.columns:
        df = df[df['price'] >= 0]

    # --- LOAD INTO DATABASE ---
    table_name = file.replace('_dataset', '').replace('.csv', '')
    print(f"Loading {file} into {table_name}...")
    df.to_sql(table_name, engine, if_exists='append', index=False)
    print(f"Successfully loaded {table_name}!")

print("ETL Process Complete!")