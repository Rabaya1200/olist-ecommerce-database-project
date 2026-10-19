import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# 1. Page Configuration (MUST BE THE FIRST STREAMLIT COMMAND)
st.set_page_config(page_title="Olist E-Commerce Dashboard", layout="wide", page_icon="🛍️")

# Custom CSS to make it look cleaner
st.markdown("""
    <style>
    .big-font { font-size:30px !important; font-weight: bold; color: #4CAF50; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛍️ Brazilian E-Commerce Dashboard")
st.markdown("Welcome to the Olist business intelligence dashboard. Data is pulled directly from PostgreSQL.")
st.sidebar.title("👨‍💻 Developer Info")
st.divider()

# 2. Database Connection
DB_USER = 'postgres'
DB_PASSWORD = 'RitaBabu1300' # <--- MAKE SURE THIS IS YOUR PASSWORD
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'olist_db'

@st.cache_resource
def get_engine():
    return create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

engine = get_engine()

# 3. Load KPI Data
@st.cache_data
def load_kpis():
    rev = pd.read_sql("SELECT SUM(payment_value) as total FROM olist_order_payments", engine).iloc[0]['total']
    orders = pd.read_sql("SELECT COUNT(order_id) as total FROM olist_orders", engine).iloc[0]['total']
    custs = pd.read_sql("SELECT COUNT(customer_id) as total FROM olist_customers", engine).iloc[0]['total']
    return rev, orders, custs

total_revenue, total_orders, total_customers = load_kpis()

# 4. Display KPI Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Revenue (BRL)", value=f"R$ {total_revenue:,.2f}")
with col2:
    st.metric(label="Total Orders", value=f"{total_orders:,}")
with col3:
    st.metric(label="Total Customers", value=f"{total_customers:,}")

st.divider()

# 5. Charts
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("🏆 Top 10 Best-Selling Categories")
    query_cat = """
    SELECT p.product_category_name AS Category, COUNT(*) AS "Times Sold"
    FROM olist_order_items i
    JOIN olist_products p ON i.product_id = p.product_id
    GROUP BY p.product_category_name
    ORDER BY "Times Sold" DESC
    LIMIT 10;
    """
    df_cat = pd.read_sql(query_cat, engine)
    fig_bar = px.bar(df_cat, x='Times Sold', y='category', orientation='h',
                     color='Times Sold', color_continuous_scale='Blues')
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_bar, use_container_width=True)

with col_chart2:
    st.subheader("💳 Payment Methods Used")
    query_pay = """
    SELECT payment_type AS "Payment Type", COUNT(*) AS "Count"
    FROM olist_order_payments
    GROUP BY payment_type;
    """
    df_pay = pd.read_sql(query_pay, engine)
    fig_pie = px.pie(df_pay, values='Count', names='Payment Type', hole=0.4,
                     color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()
st.caption("Dashboard created by Rabaya Jahan for Principles of Database System.")