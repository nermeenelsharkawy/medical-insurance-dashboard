import streamlit as st
import pandas as pd
import plotly.express as px

# إعداد الصفحة لتكون بعرض الشاشة
st.set_page_config(layout="wide")

# قراءة ملف البيانات باستخدام المسار الكامل المباشر
file_path = r"C:\Users\STW\Desktop\data engineering\project\medical-insurance-dataset Train_Data.csv"
df = pd.read_csv(file_path)

# عنوان لوحة التحكم
st.title("لوحة تحكم بيانات التأمين الطبي 📊")

# تقسيم الشاشة إلى 3 أعمدة للمؤشرات الرئيسية
col1, col2, col3 = st.columns(3)
col1.metric("إجمالي المشتركين", f"{len(df):,}")
col2.metric("متوسط التكاليف الكلية", f"${df['charges'].mean():,.2f}")
col3.metric("متوسط تكاليف المدخنين", f"${df[df['smoker']=='yes']['charges'].mean():,.2f}")

st.write("---")

# إضافة الرسم البياني التفاعلي
fig = px.scatter(df, x="age", y="charges", color="smoker", opacity=0.7, 
                 title="العلاقة بين العمر والتكاليف الطبية (حسب حالة التدخين)")
st.plotly_chart(fig, use_container_width=True)