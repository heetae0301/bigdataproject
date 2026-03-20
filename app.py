import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="최희태 자기소개", page_icon="🙋")

# 제목
st.title("자기소개")

# 기본 정보
st.write("## 자기소개")
st.write("**이름**: 최희태")
st.write("**학과**: 인공지능소프트웨어학과")
st.write("**학번**: 20221661")

st.write("---")

# 이번 학기 시간표
st.write("## 이번 학기 시간표")
schedule = pd.DataFrame({
    "요일": ["월", "화", "수", "목", "금"],
    "2교시": ["인공지능라이브러리", "-", "-", "-", "자연어처리"],
    "3교시": ["인공지능라이브러리", "-", "-", "-", "자연어처리"],
    "4교시": ["인공지능라이브러리", "-", "-", "-", "자연어처리"],
    "5교시": ["-", "-", "-", "-", "-"],
    "6교시": ["-", "인공지능캡스톤디자인", "-", "인공지능서비스프로젝트", "빅데이터분석프로젝트"],
    "7교시": ["-", "인공지능캡스톤디자인", "-", "인공지능서비스프로젝트", "빅데이터분석프로젝트"],
    "8교시": ["-", "인공지능캡스톤디자인", "-", "인공지능서비스프로젝트", "빅데이터분석프로젝트"]
})
st.dataframe(schedule, use_container_width=True)

st.write("---")

# 관심 분야
st.write("## 관심 분야")
st.write("- 데이터 분석")
st.write("- 머신러닝")
st.write("- 자연어처리")
st.write("- 웹 개발")

st.write("---")

# 이번 학기 목표
st.write("## 이번 학기 목표")
goals = pd.DataFrame({
    "목표": ["Streamlit 익히기", "GitHub 활용 익히기", "프로젝트 완성"],
    "달성률": [20, 30, 10]
})
st.dataframe(goals, use_container_width=True)
st.bar_chart(goals.set_index("목표"))