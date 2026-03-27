import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 데이터 데모")

df = pd.DataFrame(
    np.random.randn(20, 5),
    columns=["매출", "비용", "이익", "고객수", "만족도"]
)

st.dataframe(df)

st.subheader("기본 통계")
st.dataframe(df.describe())