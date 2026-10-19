import pandas as pd
from sqlalchemy import create_engine
import os

# Database Connection
DB_USER = 'postgres'
DB_PASSWORD = 'RitaBabu1300' # <--- Make sure this is your correct password
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'olist_db'

engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
folder_path = r'Brazilian E-Commerce dataset(Olist)'

# Load the missing payments table
file = 'olist_order_payments_dataset.csv'
df = pd.read_csv(os.path.join(folder_path, file))
df.drop_duplicates(inplace=True)

print("Loading olist_order_payments...")
df.to_sql('olist_order_payments', engine, if_exists='append', index=False)
print("Successfully loaded olist_order_payments!")