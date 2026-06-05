# ==========================================
# 0. كود التثبيت الذاتي الإجباري (حل مشكلة السيرفر)
# ==========================================
import sys
import subprocess

# محاولة استدعاء المكتبات، وإذا لم تكن موجودة يتم تثبيتها فوراً
try:
    import plotly
    import statsmodels
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly", "statsmodels"])
# ==========================================

# الآن يبدأ الكود الطبيعي الخاص بكِ:
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ... (باقي الكود الخاص بالـ Dashboard كما هو بدون أي تغيير)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ==========================================
# 1. إعداد الصفحة والمظهر العام
# ==========================================
st.set_page_config(
    page_title="Executive Medical Insurance BI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم كروت المؤشرات (KPI Cards) لتشبه Power BI
st.markdown("""
    <style>
    div[data-testid="metric-container"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 5% 5% 5% 10%;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 4px 4px 0px 0px;
        padding-top: 10px;
        padding-bottom: 10px;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. قراءة البيانات وهندسة الميزات
# ==========================================
@st.cache_data
def load_and_preprocess_data():
    """قراءة ملف البيانات وتجهيز الفئات للتحليل الاحترافي"""
    # قراءة الملف من نفس المجلد مباشرة
    df = pd.read_csv("medical-insurance-dataset Train_Data.csv")
    
    # تنظيف النصوص
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip().str.lower()
        
    # إنشاء فئات الأعمار والـ BMI لسهولة التصفية والتحليل
    df['age'] = np.floor(df['age']).astype(int)
    df['age_group'] = pd.cut(df['age'], bins=[0, 25, 40, 55, 100], 
                             labels=['18-25', '26-40', '41-55', '56+'])
    df['bmi_category'] = pd.cut(df['bmi'], bins=[0, 18.5, 24.9, 29.9, 100], 
                                labels=['Underweight', 'Normal', 'Overweight', 'Obese'])
    return df

df = load_and_preprocess_data()

# ==========================================
# 3. القائمة الجانبية (لوحة التحكم بالفلاتر)
# ==========================================
st.sidebar.title("🗂️ لوحة الفلاتر الديناميكية")
st.sidebar.markdown("---")

# فلاتر النصوص
selected_region = st.sidebar.multiselect("المنطقة الجغرافية (Region)", options=df['region'].unique(), default=df['region'].unique())
selected_smoker = st.sidebar.multiselect("حالة التدخين (Smoker)", options=df['smoker'].unique(), default=df['smoker'].unique())
selected_sex = st.sidebar.multiselect("الجنس (Gender)", options=df['sex'].unique(), default=df['sex'].unique())

# فلاتر الأرقام (Sliders)
age_min, age_max = st.sidebar.slider("نطاق العمر", int(df['age'].min()), int(df['age'].max()), (int(df['age'].min()), int(df['age'].max())))
bmi_min, bmi_max = st.sidebar.slider("نطاق كتلة الجسم (BMI)", float(df['bmi'].min()), float(df['bmi'].max()), (float(df['bmi'].min()), float(df['bmi'].max())))

# تطبيق الفلاتر على البيانات فوراً
filtered_df = df[
    (df['region'].isin(selected_region)) &
    (df['smoker'].isin(selected_smoker)) &
    (df['sex'].isin(selected_sex)) &
    (df['age'].between(age_min, age_max)) &
    (df['bmi'].between(bmi_min, bmi_max))
]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**عدد السجلات المحددة: {len(filtered_df):,} / {len(df):,}**")

# ==========================================
# 4. الواجهة الرئيسية والتبويبات الاحترافية
# ==========================================
st.title("منصة تحليل بيانات واستشارات التأمين الطبي 📊")
st.markdown("لوحة تحكم تفاعلية مخصصة للإدارة التنفيذية لدراسة تكاليف التامين والمخاطر.")

# إنشاء التبويبات (Tabs) مثل Power BI
tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 الملخص التنفيذي (Executive)", 
    "📈 تحليل محركات التكلفة (Cost Drivers)", 
    "🧠 تحليلات متقدمة وعزل المخاطر", 
    "🗃️ مستكشف البيانات (Explorer)"
])

# ------------------------------------------
# التبويب الأول: الملخص التنفيذي
# ------------------------------------------
with tab1:
    st.markdown("### المؤشرات الرئيسية للمحفظة التأمينية (KPIs)")
    
    # الحسابات
    total_lives = len(filtered_df)
    total_charges = filtered_df['charges'].sum()
    avg_charges = filtered_df['charges'].mean()
    smoker_pct = (filtered_df[filtered_df['smoker'] == 'yes'].shape[0] / total_lives * 100) if total_lives > 0 else 0
    
    # عرض الكروت
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("إجمالي المؤمن عليهم", f"{total_lives:,}")
    kpi2.metric("إجمالي التكاليف الكلية", f"${total_charges:,.0f}")
    kpi3.metric("متوسط القسط السنوي", f"${avg_charges:,.2f}")
    kpi4.metric("نسبة اختراق المدخنين", f"{smoker_pct:.1f}%")
    
    st.write("---")
    
    col1, col2 = st.columns([6, 4])
    with col1:
        st.markdown("#### توزيع المصاريف السنوية حسب حالة التدخين")
        fig_dist = px.histogram(
            filtered_df, x="charges", color="smoker", nbins=50, 
            marginal="box", opacity=0.75, barmode="overlay",
            color_discrete_sequence=["#1f77b4", "#ff7f0e"],
            template="plotly_white"
        )
        st.plotly_chart(fig_dist, use_container_width=True)
        
    with col2:
        st.markdown("#### التوزيع الديموغرافي (منطقة / تدخين / جنس)")
        fig_sun = px.sunburst(
            filtered_df, path=['region', 'smoker', 'sex'], values='charges',
            color='charges', color_continuous_scale='Blues',
            template="plotly_white"
        )
        st.plotly_chart(fig_sun, use_container_width=True)

# ------------------------------------------
# التبويب الثاني: تحليل محركات التكلفة
# ------------------------------------------
with tab2:
    st.markdown("### ما الذي يرفع أسعار التأمين الطبي؟")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### الأثر المركب: كتلة الجسم (BMI) ضد التكلفة حسب التدخين")
        fig_scatter = px.scatter(
            filtered_df, x="bmi", y="charges", color="smoker", 
            size="age", hover_data=['sex', 'region'],
            color_discrete_map={"yes": "#e74c3c", "no": "#2ecc71"},
            template="plotly_white", trendline="ols"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with col2:
        st.markdown("#### توزيع التكاليف حسب الفئات العمرية والتدخين")
        fig_box = px.box(
            filtered_df, x="age_group", y="charges", color="smoker",
            category_orders={"age_group": ["18-25", "26-40", "41-55", "56+"]},
            template="plotly_white"
        )
        st.plotly_chart(fig_box, use_container_width=True)

# ------------------------------------------
# التبويب الثالث: تحليلات متقدمة
# ------------------------------------------
with tab3:
    st.markdown("### التحليل الإحصائي وعزل الحالات الحرجة")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### مصفوفة الارتباط (Correlation Matrix)")
        base_num_cols = ['age', 'bmi', 'children', 'charges']
        corr_matrix = filtered_df[base_num_cols].corr()
        fig_corr = px.imshow(corr_matrix, text_auto=".2f", color_continuous_scale="RdBu_r")
        st.plotly_chart(fig_corr, use_container_width=True)
        
    with col2:
        st.markdown("#### متوسط التكلفة حسب تصنيف الوزن العالمي")
        avg_bmi_cat = filtered_df.groupby('bmi_category', observed=True)['charges'].mean().reset_index()
        fig_funnel = px.funnel(avg_bmi_cat, x='charges', y='bmi_category', color_discrete_sequence=["#e67e22"])
        st.plotly_chart(fig_funnel, use_container_width=True)
        
    st.markdown("---")
    st.markdown("#### 🚨 رصد أعلى 5% من العملاء تكلفة (عزل المخاطر العالية)")
    if not filtered_df.empty:
        threshold_95 = filtered_df['charges'].quantile(0.95)
        top_5_percent = filtered_df[filtered_df['charges'] >= threshold_95].sort_values(by='charges', ascending=False)
        
        st.warning(f"تم رصد **{len(top_5_percent)}** شخص يمثلون الفئة الأعلى خطورة وتكلفة (تكلفتهم السنوية تتخطى ${threshold_95:,.2f})")
        st.dataframe(top_5_percent, use_container_width=True)

# ------------------------------------------
# التبويب الرابع: مستكشف البيانات
# ------------------------------------------
with tab4:
    st.markdown("### استعراض وتصدير البيانات المفلترة")
    st.dataframe(filtered_df, use_container_width=True)
    
    # زر تحميل البيانات المفلترة كملف CSV
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 تحميل البيانات الحالية كـ CSV",
        data=csv,
        file_name='filtered_insurance_data.csv',
        mime='text/csv',
    )
