import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pyodbc

st.set_page_config(page_title="Banggood Dashboard", layout="wide")
st.title("📊 Banggood Products Dashboard")

# -----------------------------
# SQL Connection to fetch data
# -----------------------------
conn_str_db = f"DRIVER={SQL_CONFIG['driver']};SERVER={SQL_CONFIG['server']};DATABASE={SQL_CONFIG['database']};Trusted_Connection=yes;"
conn = pyodbc.connect(conn_str_db)
df_sql = pd.read_sql("SELECT * FROM banggood_products", conn)
conn.close()

# -----------------------------
# Dashboard Layout
# -----------------------------
st.subheader("Top 10 Products by Reviews")
top_reviews = df_sql.sort_values('reviews', ascending=False).head(10)
st.dataframe(top_reviews[['product_name','reviews','category']])

st.subheader("Category Distribution")
category_counts = df_sql['category'].value_counts()
fig1, ax1 = plt.subplots(figsize=(6,6))
category_counts.plot.pie(autopct='%1.1f%%', startangle=140, ax=ax1, cmap='Set3')
ax1.set_ylabel('')
st.pyplot(fig1)

st.subheader("Top 10 Products Bar Chart")
fig2, ax2 = plt.subplots(figsize=(12,6))
sns.barplot(x='reviews', y='product_name', data=top_reviews, palette='viridis', ax=ax2)
ax2.set_xlabel("Reviews")
ax2.set_ylabel("Product Name")
st.pyplot(fig2)

st.subheader("Price Drop Distribution by Category")
fig3, ax3 = plt.subplots(figsize=(10,6))
sns.boxplot(x='category', y='price_drop', data=df_sql, ax=ax3)
ax3.set_title("Price Drop Distribution")
st.pyplot(fig3)

st.subheader("Value Score Distribution by Category")
fig4, ax4 = plt.subplots(figsize=(10,6))
sns.boxplot(x='category', y='value_score', data=df_sql, ax=ax4)
ax4.set_title("Value Score Distribution")
st.pyplot(fig4)
