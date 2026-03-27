import streamlit as st
import pandas as pd
import numpy as np

st.title("🌍 지도 데모")

map_data = pd.DataFrame(
    np.random.randn(200, 2) / [100, 100] + [37.5005419, 126.8676709],
    columns=["lat", "lon"]
)

st.map(map_data)