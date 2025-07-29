import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


@st.cache_data
def load_data():
    df_products = pd.read_csv('products_with_clusters.csv')
    df_rules = pd.read_csv('association_rules_output.csv')
    return df_products, df_rules

df_products, df_rules = load_data()


st.set_page_config(layout="wide")
st.sidebar.title("قائمة التنقل")


page = st.sidebar.radio(
    "اختر الصفحة:",
    ["الرئيسية", "قواعد الترابط", "نتائج التجميع", "مخطط التشتت"]
)


if page == "الرئيسية":
    st.title("واجهة مشروع تحليل البيانات")
    st.write("""
    ### مرحباً بك في واجهة مشروع تحليل البيانات
    
    استخدم القائمة الجانبية للتنقل بين الصفحات المختلفة:
    
    - **قواعد الترابط**: عرض قواعد الارتباط المكتشفة
    - **نتائج التجميع**: عرض نتائج تجميع المنتجات  
    - **مخطط التشتت**: عرض المخطط البياني لنتائج التجميع
    """)
    
    st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)


elif page == "قواعد الترابط":
    st.title("قواعد الترابط")
    st.write("### قواعد الارتباط المكتشفة")
    
    # إضافة فلاتر
    min_confidence = st.slider("الحد الأدنى للثقة", 0.0, 1.0, 0.5)
    min_lift = st.slider("الحد الأدنى للرفع", 1.0, 5.0, 1.0)
    

    filtered_rules = df_rules[
        (df_rules['confidence'] >= min_confidence) & 
        (df_rules['lift'] >= min_lift)
    ]
    
    st.dataframe(
        filtered_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].style.format({
            'support': '{:.4f}',
            'confidence': '{:.4f}',
            'lift': '{:.4f}'
        })
    )
    
    st.write(f"عدد القواعد المعروضة: {len(filtered_rules)} من أصل {len(df_rules)}")


elif page == "نتائج التجميع":
    st.title("نتائج التجميع")
    st.write("### تجميع المنتجات بناءً على السعر والتقييم")
    
 
    cluster_stats = df_products['Cluster'].value_counts().sort_index()
    st.write("#### توزيع المنتجات حسب المجموعات:")
    st.bar_chart(cluster_stats)
    

    st.dataframe(df_products[['ProductName', 'Price', 'Rating', 'Cluster']].sort_values('Cluster'))
    
   
    st.write("#### إحصائيات كل مجموعة:")
    cluster_summary = df_products.groupby('Cluster').agg({
        'Price': ['mean', 'min', 'max'],
        'Rating': ['mean', 'min', 'max']
    }).round(2)
    st.dataframe(cluster_summary)


elif page == "مخطط التشتت":
    st.title("مخطط التشتت لنتائج التجميع")
    
    col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox("اختر المحور الأفقي:", ['Price', 'Rating'], index=0)
    with col2:
        y_axis = st.selectbox("اختر المحور العمودي:", ['Price', 'Rating'], index=1)
    
    color_palette = st.selectbox(
        "اختر لوحة الألوان:",
        ['viridis', 'plasma', 'inferno', 'magma', 'coolwarm']
    )
    
   
    fig, ax = plt.subplots(figsize=(12, 8))
    scatter = sns.scatterplot(
        data=df_products, 
        x=x_axis, 
        y=y_axis, 
        hue='Cluster', 
        palette=color_palette, 
        s=100, 
        ax=ax
    )
    
    ax.set_title(f'Clustering of Products ({x_axis} vs {y_axis})')
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    

    plt.legend(title='المجموعات')
    
    st.pyplot(fig)
    

    st.write("#### معلومات عن المجموعات:")
    for cluster_num in sorted(df_products['Cluster'].unique()):
        cluster_data = df_products[df_products['Cluster'] == cluster_num]
        st.write(f"**المجموعة {cluster_num}:** {len(cluster_data)} منتج")

st.sidebar.divider()
st.sidebar.write("### معلومات المشروع")
st.sidebar.write("- تحليل سلة المشتريات")
st.sidebar.write("- تجميع المنتجات")
st.sidebar.write("- تحليل الارتباط")

if st.sidebar.button("إعادة تحميل البيانات"):
    st.cache_data.clear()
    st.success("تم إعادة تحميل البيانات!")