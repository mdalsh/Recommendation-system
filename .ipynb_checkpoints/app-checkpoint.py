import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df_products = pd.read_csv('products_with_clusters.csv')
df_rules = pd.read_csv('association_rules_output.csv')

st.title("واجهة مشروع تحليل البيانات")

st.header("قوائم الترابط")
st.dataframe(df_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

st.header("نتائج التجميع")
st.dataframe(df_products[['ProductName', 'Cluster']])

st.header("مخطط التشتت لنتائج التجميع")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df_products, x='Price', y='Rating', hue='Cluster', palette='viridis', s=100, ax=ax)
ax.set_title('Clustering of Products (Price vs Rating)')
ax.set_xlabel('Price')
ax.set_ylabel('Rating')
st.pyplot(fig)