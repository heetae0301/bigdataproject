import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from anthropic import Anthropic
import os

st.set_page_config(page_title="KOSPI MACD 분석", layout="wide")

st.title("📊 KOSPI MACD 기술적 신호 분석 (Claude AI)")
st.markdown("---")

# ===== Claude API 설정 =====
os.environ["ANTHROPIC_API_KEY"] = "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"

client = Anthropic()

@st.cache_data
def load_data():
    df = pd.read_csv('kospi_with_signals.csv', encoding='utf-8')
    df['날짜'] = pd.to_datetime(df['날짜'])
    df['종가_숫자'] = df['종가'].str.replace(',', '').astype(float)
    return df

df = load_data()

st.sidebar.header("📈 설정")

# ===== 날짜 선택 =====
st.sidebar.subheader("📅 분석 날짜 선택")
selected_date = st.sidebar.date_input(
    "날짜를 선택하세요 (선택한 날짜의 상황 분석)",
    value=df['날짜'].max(),
    min_value=df['날짜'].min(),
    max_value=df['날짜'].max()
)

# 선택한 날짜의 데이터 찾기
selected_data = df[df['날짜'].dt.date == selected_date]

if len(selected_data) == 0:
    st.sidebar.warning("⚠️ 선택한 날짜에 거래가 없습니다.")
    selected_row = df.iloc[-1]
    selected_date_display = df.iloc[-1]['날짜']
else:
    selected_row = selected_data.iloc[0]
    selected_date_display = selected_row['날짜']

# 날짜 범위 선택
start_date = st.sidebar.date_input("차트 시작 날짜", df['날짜'].min())
end_date = st.sidebar.date_input("차트 종료 날짜", df['날짜'].max())

mask = (df['날짜'].dt.date >= start_date) & (df['날짜'].dt.date <= end_date)
filtered_df = df[mask]

# ===== Claude AI 분석 함수 =====
def analyze_specific_date(date_data, date_str):
    """특정 날짜에 대한 Claude AI 분석"""
    
    prompt = f"""
당신은 KOSPI 기술적 분석 전문가입니다.

{date_str}의 KOSPI 거래 데이터:
- 현재 가격: {date_data['종가']}
- 시가: {date_data['시가']}
- 고가: {date_data['고가']}
- 저가: {date_data['저가']}
- MACD: {date_data['MACD']:.4f}
- 신호선: {date_data['신호선']:.4f}
- 히스토그램: {date_data['MACD'] - date_data['신호선']:.4f}
- MA5: {date_data['MA5']:.2f}
- MA20: {date_data['MA20']:.2f}
- MA60: {date_data['MA60']:.2f}
- 거래량: {date_data['거래량']}

이 데이터를 기반으로:
1. 이 날짜의 시장 상황 분석
2. 기술적 지표가 의미하는 바
3. 투자자들의 심리 (강세/약세)
4. 이 날의 특징

한국어로 전문적이고 흥미롭게 설명해주세요. 4-5문장으로 명확하게.
"""
    
    response = client.messages.create(
        model="claude-opus-4-1",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.content[0].text

def analyze_with_claude(latest_data):
    """Claude AI로 KOSPI 분석"""
    
    prompt = f"""
당신은 KOSPI 기술적 분석 전문가입니다.

현재 KOSPI 데이터:
- 현재 가격: {latest_data['종가']}
- MACD: {latest_data['MACD']:.4f}
- 신호선: {latest_data['신호선']:.4f}
- 히스토그램: {latest_data['MACD'] - latest_data['신호선']:.4f}
- MA5: {latest_data['MA5']:.2f}
- MA20: {latest_data['MA20']:.2f}
- MA60: {latest_data['MA60']:.2f}

이 데이터를 기반으로:
1. 현재 시장 신호 분석 (매수/매도)
2. 신뢰도와 근거
3. 투자 추천 (구체적인 액션)
4. 주의사항

한국어로 전문적이고 명확하게 답변해주세요. 3-4문장 정도로 간결하게.
"""
    
    response = client.messages.create(
        model="claude-opus-4-1",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.content[0].text

def chat_with_claude(user_message, conversation_history):
    """Claude AI 챗봇"""
    
    latest = df.iloc[-1]
    
    system_prompt = f"""
당신은 KOSPI 기술적 분석 AI 어시스턴트입니다.

현재 KOSPI 데이터:
- 가격: {latest['종가']}
- MACD: {latest['MACD']:.4f}
- 신호선: {latest['신호선']:.4f}
- MA5: {latest['MA5']:.2f}
- MA20: {latest['MA20']:.2f}
- MA60: {latest['MA60']:.2f}

사용자의 질문에 대해 한국어로 전문적이고 명확하게 답변하세요.
금융 조언보다는 기술적 분석 정보 제공에 중점을 두세요.
항상 투자 위험성을 언급하세요.
"""
    
    messages = conversation_history + [{"role": "user", "content": user_message}]
    
    response = client.messages.create(
        model="claude-opus-4-1",
        max_tokens=500,
        system=system_prompt,
        messages=messages
    )
    
    return response.content[0].text

def analyze_signal(latest):
    """AI 점수 계산"""
    
    macd = latest['MACD']
    signal = latest['신호선']
    ma5 = latest['MA5']
    ma20 = latest['MA20']
    ma60 = latest['MA60']
    histogram = macd - signal
    
    score = 0
    reasons = []
    
    if macd > signal:
        score += 2
        reasons.append("✅ MACD > 신호선 (강한 상승신호)")
    else:
        score -= 2
        reasons.append("❌ MACD < 신호선 (강한 하락신호)")
    
    if abs(histogram) > 0.01:
        score += 1
        reasons.append("✅ 히스토그램 확대 (신호 강함)")
    else:
        reasons.append("⚠️ 히스토그램 축소 (신호 약함)")
    
    if ma5 > ma20 > ma60:
        score += 2
        reasons.append("✅ MA5 > MA20 > MA60 (강한 상승추세)")
    elif ma5 > ma20:
        score += 1
        reasons.append("✅ MA5 > MA20 (약한 상승추세)")
    elif ma5 < ma20 < ma60:
        score -= 2
        reasons.append("❌ MA5 < MA20 < MA60 (강한 하락추세)")
    else:
        score -= 1
        reasons.append("❌ MA5 < MA20 (약한 하락추세)")
    
    if score >= 3:
        recommendation = "🟢 강한 매수 신호"
        confidence = "매우 높음 (95%)"
        action = "지금 사기 좋은 타이밍"
    elif score >= 1:
        recommendation = "🟡 약한 매수 신호"
        confidence = "중간 (70%)"
        action = "신중하게 매수 검토"
    elif score >= -1:
        recommendation = "🔵 중립"
        confidence = "낮음 (50%)"
        action = "더 명확한 신호 대기"
    elif score >= -3:
        recommendation = "🟠 약한 매도 신호"
        confidence = "중간 (70%)"
        action = "신중하게 매도 검토"
    else:
        recommendation = "🔴 강한 매도 신호"
        confidence = "매우 높음 (95%)"
        action = "지금 팔기 좋은 타이밍"
    
    return {
        'score': score,
        'recommendation': recommendation,
        'confidence': confidence,
        'action': action,
        'reasons': reasons
    }

# ===== 탭 =====
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📊 대시보드", "📅 날짜 분석", "🤖 Claude AI 분석", "💬 Claude 챗봇", "⚡ MACD", "📈 가격", "📉 MA"])

# ===== Tab 1: 대시보드 =====
with tab1:
    st.subheader("📊 현재 상태")
    
    latest = df.iloc[-1]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("현재 가격", latest['종가'])
    with col2:
        st.metric("MACD", f"{latest['MACD']:.4f}")
    with col3:
        st.metric("신호선", f"{latest['신호선']:.4f}")
    with col4:
        st.metric("MA5", f"{latest['MA5']:.2f}")
    
    st.markdown("---")
    
    macd_value = latest['MACD']
    signal_value = latest['신호선']
    histogram = macd_value - signal_value
    
    st.write(f"**MACD 값**: {macd_value:.4f}")
    st.write(f"**신호선 값**: {signal_value:.4f}")
    st.write(f"**히스토그램**: {histogram:.4f}")
    
    st.markdown("---")
    
    if macd_value > signal_value:
        st.success("### 🟢 상승신호! (매수)")
        st.write(f"MACD ({macd_value:.4f}) **>** 신호선 ({signal_value:.4f})")
    else:
        st.error("### 🔴 하락신호! (매도)")
        st.write(f"MACD ({macd_value:.4f}) **<** 신호선 ({signal_value:.4f})")
    
    st.markdown("---")
    
    if latest['MA5'] > latest['MA20'] > latest['MA60']:
        st.info("🟢 강한 상승추세 (MA5 > MA20 > MA60)")
    elif latest['MA5'] > latest['MA20']:
        st.info("🟡 약한 상승추세 (MA5 > MA20)")
    elif latest['MA5'] < latest['MA20'] < latest['MA60']:
        st.warning("🔴 강한 하락추세 (MA5 < MA20 < MA60)")
    else:
        st.warning("⚫ 약한 하락추세 (MA5 < MA20)")

# ===== Tab 2: 날짜 분석 =====
with tab2:
    st.subheader(f"📅 {selected_date_display.strftime('%Y년 %m월 %d일')} 분석")
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("종가", selected_row['종가'])
    with col2:
        st.metric("MACD", f"{selected_row['MACD']:.4f}")
    with col3:
        st.metric("신호선", f"{selected_row['신호선']:.4f}")
    with col4:
        st.metric("MA5", f"{selected_row['MA5']:.2f}")
    
    st.markdown("---")
    
    st.subheader("💡 이 날의 상황 분석")
    
    with st.spinner(f"🤖 {selected_date_display.strftime('%Y년 %m월 %d일')}의 분석을 진행 중입니다..."):
        try:
            date_analysis = analyze_specific_date(selected_row, selected_date_display.strftime('%Y년 %m월 %d일'))
            st.info(date_analysis)
        except Exception as e:
            st.error(f"❌ API 오류: {str(e)}")
    
    st.markdown("---")
    
    st.subheader("📊 이 날의 지표")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**시가**: {selected_row['시가']}")
        st.write(f"**고가**: {selected_row['고가']}")
        st.write(f"**저가**: {selected_row['저가']}")
        st.write(f"**종가**: {selected_row['종가']}")
    
    with col2:
        st.write(f"**MACD**: {selected_row['MACD']:.4f}")
        st.write(f"**신호선**: {selected_row['신호선']:.4f}")
        st.write(f"**히스토그램**: {selected_row['MACD'] - selected_row['신호선']:.4f}")
        st.write(f"**거래량**: {selected_row['거래량']}")
    
    st.markdown("---")
    
    analysis = analyze_signal(selected_row)
    
    st.subheader("🎯 기술적 신호")
    st.metric("AI 추천", analysis['recommendation'])
    
    for reason in analysis['reasons']:
        st.write(reason)

# ===== Tab 3: Claude AI 분석 =====
with tab3:
    st.subheader("🤖 Claude AI 분석 & 추천")
    
    latest = df.iloc[-1]
    analysis = analyze_signal(latest)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("AI 추천", analysis['recommendation'])
    with col2:
        st.metric("신뢰도", analysis['confidence'])
    
    st.markdown("---")
    
    st.subheader("📋 기술적 분석")
    
    for reason in analysis['reasons']:
        st.write(reason)
    
    st.markdown("---")
    
    st.subheader("💡 Claude AI 상세 분석")
    
    with st.spinner("🤖 Claude가 분석 중입니다..."):
        try:
            claude_analysis = analyze_with_claude(latest)
            st.info(claude_analysis)
        except Exception as e:
            st.error(f"❌ API 오류: {str(e)}")
    
    st.markdown("---")
    
    st.subheader("📌 추천 액션")
    st.success(f"### {analysis['action']}")
    
    st.markdown("---")
    
    st.subheader("⚠️ 리스크 경고")
    st.warning("""
    - 🎯 이 분석은 기술적 분석일 뿐입니다
    - 📉 시장 뉴스와 경제 지표도 함께 고려하세요
    - 💰 전체 자산의 5% 이상을 한번에 투자하지 마세요
    - 🛑 손절매 계획을 미리 세우세요
    """)

# ===== Tab 4: Claude 챗봇 =====
with tab4:
    st.subheader("💬 Claude AI 챗봇")
    
    st.write("KOSPI 기술적 분석에 대해 물어보세요!")
    st.write("예: '지금 매수하면 좋을까?', 'MACD가 뭐야?', '위험성은?'")
    
    st.markdown("---")
    
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    
    for message in st.session_state.chat_messages:
        if message['role'] == 'user':
            st.write(f"👤 **당신**: {message['content']}")
        else:
            st.write(f"🤖 **Claude**: {message['content']}")
    
    st.markdown("---")
    
    user_input = st.text_input("질문을 입력하세요:")
    
    if user_input:
        st.session_state.chat_messages.append({
            'role': 'user',
            'content': user_input
        })
        
        with st.spinner("🤖 Claude가 답변 중입니다..."):
            try:
                response = chat_with_claude(
                    user_input,
                    st.session_state.chat_messages[:-1]
                )
                
                st.session_state.chat_messages.append({
                    'role': 'assistant',
                    'content': response
                })
                
                st.rerun()
            except Exception as e:
                st.error(f"❌ API 오류: {str(e)}")

# ===== Tab 5: MACD =====
with tab5:
    st.subheader("⚡ MACD 상세 분석")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=filtered_df['날짜'], 
        y=filtered_df['MACD'],
        name='MACD',
        mode='lines',
        line=dict(color='blue', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=filtered_df['날짜'], 
        y=filtered_df['신호선'],
        name='신호선',
        mode='lines',
        line=dict(color='red', width=2)
    ))
    
    histogram_colors = ['green' if x > 0 else 'red' for x in (filtered_df['MACD'] - filtered_df['신호선'])]
    fig.add_trace(go.Bar(
        x=filtered_df['날짜'],
        y=filtered_df['MACD'] - filtered_df['신호선'],
        name='히스토그램',
        marker=dict(color=histogram_colors),
        opacity=0.4
    ))
    
    fig.add_hline(y=0, line_color="black", line_width=1)
    
    fig.update_layout(
        title='MACD',
        xaxis_title='날짜',
        yaxis_title='MACD',
        hovermode='x unified',
        height=600,
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ===== Tab 6: 가격 =====
with tab6:
    st.subheader("📈 가격 추이")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_df['날짜'], y=filtered_df['종가_숫자'], name='종가', line=dict(color='black', width=2)))
    fig.add_trace(go.Scatter(x=filtered_df['날짜'], y=filtered_df['MA5'], name='MA5', line=dict(color='orange', dash='dash')))
    fig.add_trace(go.Scatter(x=filtered_df['날짜'], y=filtered_df['MA20'], name='MA20', line=dict(color='green', dash='dash')))
    fig.add_trace(go.Scatter(x=filtered_df['날짜'], y=filtered_df['MA60'], name='MA60', line=dict(color='red', dash='dash')))
    
    fig.update_layout(title='KOSPI 가격 & 이동평균선', xaxis_title='날짜', yaxis_title='가격', height=500, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

# ===== Tab 7: MA =====
with tab7:
    st.subheader("📉 이동평균선 분석")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_df['날짜'], y=filtered_df['종가_숫자'], name='종가', line=dict(color='black', width=2)))
    fig.add_trace(go.Scatter(x=filtered_df['날짜'], y=filtered_df['MA5'], name='MA5', line=dict(color='orange', width=2)))
    fig.add_trace(go.Scatter(x=filtered_df['날짜'], y=filtered_df['MA20'], name='MA20', line=dict(color='green', width=2)))
    fig.add_trace(go.Scatter(x=filtered_df['날짜'], y=filtered_df['MA60'], name='MA60', line=dict(color='red', width=2)))
    
    fig.update_layout(title='이동평균선', xaxis_title='날짜', yaxis_title='가격', height=500, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.write("📊 KOSPI MACD 기술적 신호 분석 (Claude AI) - 기말 프로젝트")
st.write("⚠️ 이 서비스는 학습용입니다. 실제 투자 결정의 책임은 사용자에게 있습니다.")
