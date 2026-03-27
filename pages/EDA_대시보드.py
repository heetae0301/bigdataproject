import streamlit as st
import pandas as pd
import numpy as np

# 페이지 설정
st.set_page_config(page_title='EDA 대시보드', layout='wide')

st.title('📊 기초 EDA 대시보드')

# -------------------------
# 데이터 생성
# -------------------------
np.random.seed(42)

df = pd.DataFrame({
    '날짜': pd.date_range('2026-01-01', periods=100),
    '카테고리': np.random.choice(['전자제품', '의류', '식품'], 100),
    '매출': np.random.randint(100, 1000, 100),
    '고객수': np.random.randint(10, 200, 100),
    '전환율': np.random.uniform(0.01, 0.20, 100)
})

# -------------------------
# 사이드바
# -------------------------
st.sidebar.header('필터')

category = st.sidebar.selectbox(
    '카테고리 선택',
    ['전체'] + list(df['카테고리'].unique())
)

rows = st.sidebar.slider('데이터 개수', 10, 100, 50)

# 데이터 필터링
filtered_df = df.head(rows)

if category != '전체':
    filtered_df = filtered_df[filtered_df['카테고리'] == category]

# -------------------------
# 탭 구성
# -------------------------
tab1, tab2 = st.tabs(['요약', '데이터'])

# -------------------------
# 탭1: 대시보드
# -------------------------
with tab1:

    st.subheader('📊 KPI 지표')

    col1, col2, col3 = st.columns(3)

    col1.metric('총 매출', f"{filtered_df['매출'].sum():,}")
    col2.metric('총 고객수', f"{filtered_df['고객수'].sum():,}")
    col3.metric('평균 전환율', f"{filtered_df['전환율'].mean():.2%}")

    st.write('---')

    st.subheader('📈 매출 추이')

    chart_data = filtered_df.groupby('날짜')['매출'].sum()

    st.line_chart(chart_data)

# -------------------------
# 탭2: 데이터
# -------------------------
with tab2:

    st.subheader('📋 원본 데이터')

    st.dataframe(filtered_df)

    # expander (접기/펼치기)
    with st.expander('통계 보기'):
        st.dataframe(filtered_df.describe())