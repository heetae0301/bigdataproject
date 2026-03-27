import streamlit as st
import pandas as pd
import numpy as np

st.title("📈 차트 데모")

df = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["매출", "비용", "이익"]
)

st.subheader("선 차트")
st.line_chart(df)

st.subheader("막대 차트")
st.bar_chart(df)

st.subheader("영역 차트")
st.area_chart(df)