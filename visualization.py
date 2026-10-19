import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# 1. Database Connection
DB_USER = 'postgres'
DB_PASSWORD = 'RitaBabu1300' # <--- MAKE SURE THIS IS YOUR PASSWORD
engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@localhost:5432/olist_db')

# 2. Query: Top 5 highest-spending customers
query = """
SELECT o.customer_id, SUM(p.payment_value) AS total_spent
FROM olist_orders o
JOIN olist_order_payments p ON o.order_id = p.order_id
GROUP BY o.customer_id
ORDER BY total_spent DESC
LIMIT 5;
"""
df = pd.read_sql(query, engine)

# 3. Create a Pie Chart
plt.figure(figsize=(8, 8))
plt.pie(df['total_spent'], labels=df['customer_id'], autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0'])
plt.title('Top 5 Highest-Spending Customers (Total Revenue Share)')

# 4. Save the chart as an image
plt.savefig('Top_Customers_Chart.png')
print("Chart successfully saved as Top_Customers_Chart.png!")