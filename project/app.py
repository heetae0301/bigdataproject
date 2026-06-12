import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from anthropic import Anthropic

st.set_page_config(page_title="KOSPI 신호 분석", layout="wide")
st.markdown("<h1 style='text-align: center; color: #1f77b4;'>📊 KOSPI 신호 분석</h1>", unsafe_allow_html=True)
st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_csv('kospi_with_signals.csv', encoding='utf-8')
    df['날짜'] = pd.to_datetime(df['날짜'])
    df['종가_숫자'] = df['종가'].str.replace(',', '').astype(float)
    return df.fillna(method='bfill').fillna(method='ffill')

df = load_data()
client = Anthropic()

def get_signal(row):
    try:
        macd = float(row['MACD'])
        signal = float(row['신호선'])
        ma5 = float(row['MA5'])
        ma20 = float(row['MA20'])
        ma60 = float(row['MA60'])
        
        score = 2 if macd > signal else -2
        score += 2 if ma5 > ma20 > ma60 else (1 if ma5 > ma20 else -1)
        
        signal_map = {-4: "🔴 강한 매도", -3: "🔴 강한 매도", -2: "🟠 약한 매도", 
                      -1: "🟠 약한 매도", 0: "🔵 중립", 1: "🟡 약한 매수", 
                      2: "🟡 약한 매수", 3: "🟢 강한 매수", 4: "🟢 강한 매수"}
        return signal_map.get(int(score), "🔵 중립"), int(score)
    except:
        return "🔵 중립", 0

def get_explanation(row):
    try:
        macd = float(row['MACD'])
        signal = float(row['신호선'])
        ma5 = float(row['MA5'])
        ma20 = float(row['MA20'])
        ma60 = float(row['MA60'])
        
        text = f"**{'✅' if macd > signal else '❌'} MACD {'>' if macd > signal else '<'} 신호선**\n\n"
        if ma5 > ma20 > ma60:
            text += "**✅ MA5 > MA20 > MA60**\n"
            text += "• MA5(단기): 최근 5일 평균\n"
            text += "• MA20(중기): 최근 20일 평균\n"
            text += "• MA60(장기): 최근 60일 평균\n\n"
            text += "단기가 가장 높고 중기가 중간, 장기가 가장 낮음\n"
            text += "→ **강한 상승추세!**"
        elif ma5 > ma20:
            text += "**🟡 MA5 > MA20** → 약한 상승"
        else:
            text += "**❌ MA5 < MA20 < MA60** → 하락추세"
        return text
    except:
        return "데이터 오류"

def calculate_accuracy(df):
    data = []
    try:
        for i in range(len(df) - 1):
            sig_text, score = get_signal(df.iloc[i])
            curr_price = float(str(df.iloc[i]['종가']).replace(',', ''))
            next_price = float(str(df.iloc[i+1]['종가']).replace(',', ''))
            
            if score >= 1:
                sig_type, correct = "매수", next_price > curr_price
            elif score <= -1:
                sig_type, correct = "매도", next_price < curr_price
            else:
                continue
            
            data.append({
                '날짜': df.iloc[i]['날짜'], '신호': sig_text, '신호타입': sig_type,
                '현재가': curr_price, '다음날가': next_price, '가격변화': next_price - curr_price,
                '정확도': "✅" if correct else "❌", '정확': correct
            })
    except Exception as e:
        st.error(f"정확도 계산 오류: {str(e)}")
    
    return pd.DataFrame(data) if data else pd.DataFrame()

accuracy_df = calculate_accuracy(df)

with st.sidebar:
    st.markdown("### 📅 날짜 선택")
    selected_date = st.date_input("날짜", value=df['날짜'].max(), min_value=df['날짜'].min(), max_value=df['날짜'].max(), label_visibility="collapsed")
    
    st.markdown("### 📈 차트 범위")
    col1, col2 = st.columns(2)
    with col1:
        chart_start = st.date_input("시작", df['날짜'].min(), label_visibility="collapsed")
    with col2:
        chart_end = st.date_input("종료", df['날짜'].max(), label_visibility="collapsed")
    
    st.markdown("---")
    st.error("**신뢰도: ~40%**\n🔴 위양성 주의\n📌 참고용만")

try:
    selected_row = df[df['날짜'].dt.date == selected_date].iloc[0]
except:
    selected_row = df.iloc[-1]

try:
    prev_row = df[df['날짜'] < selected_row['날짜']].iloc[-1]
except:
    prev_row = selected_row

chart_df = df[(df['날짜'].dt.date >= chart_start) & (df['날짜'].dt.date <= chart_end)]

signal_text, score = get_signal(selected_row)
prev_signal, prev_score = get_signal(prev_row)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 대시보드", "📅 날짜분석", "🔍 상세분석", "📋 일일신호", "📈 정확도"])

with tab1:
    st.subheader(f"📊 {selected_row['날짜'].strftime('%Y년 %m월 %d일')}")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("종가", f"{selected_row['종가']}")
    col2.metric("MACD", f"{float(selected_row['MACD']):.4f}")
    col3.metric("신호선", f"{float(selected_row['신호선']):.4f}")
    col4.metric("MA5", f"{float(selected_row['MA5']):,.0f}원")
    col5.metric("MA20", f"{float(selected_row['MA20']):,.0f}원")
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"### {signal_text}\n점수: {score}/4\n신뢰도: {selected_row['신뢰도']}")
    with col2:
        st.markdown(f"### 신호 이유\n{get_explanation(selected_row)}")
    with col3:
        change = score - prev_score
        st.write(f"### 어제 비교\n{'⬆️ 상승' if change > 0 else '⬇️ 하락' if change < 0 else '➡️ 동일'}\n({change:+d}점)")
    
    st.markdown("---")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("MA60", f"{float(selected_row['MA60']):,.0f}원")
    col2.metric("히스토그램", f"{(float(selected_row['MACD']) - float(selected_row['신호선'])):.4f}")
    col3.metric("10일 평균 대비", f"{float(selected_row['종가'].replace(',', '')) - df.tail(10)['종가_숫자'].mean():,.0f}원")
    col4.metric("상승추세", f"{len(df.tail(10)[df.tail(10)['MA5'] > df.tail(10)['MA20']])}/10")
    col5.metric("이후 최고가", f"{df[df['날짜'] >= selected_row['날짜']]['종가_숫자'].max():,.0f}원")
    
    st.markdown("---")
    st.markdown(f"### 📈 가격 추이")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=chart_df['날짜'], y=chart_df['종가_숫자'], name='종가', line=dict(color='black', width=2.5)))
    fig.add_trace(go.Scatter(x=chart_df['날짜'], y=chart_df['MA5'], name='MA5', line=dict(color='orange', dash='dash')))
    fig.add_trace(go.Scatter(x=chart_df['날짜'], y=chart_df['MA20'], name='MA20', line=dict(color='green', dash='dash')))
    fig.add_trace(go.Scatter(x=chart_df['날짜'], y=chart_df['MA60'], name='MA60', line=dict(color='red', dash='dash')))
    fig.add_vline(x=selected_row['날짜'], line_dash="dash", line_color="blue", opacity=0.5)
    fig.update_layout(height=400, hovermode='x unified', template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader(f"📅 {selected_row['날짜'].strftime('%Y년 %m월 %d일')} 상세분석")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("종가", selected_row['종가'])
    col2.metric("MACD", f"{float(selected_row['MACD']):.4f}")
    col3.metric("신호선", f"{float(selected_row['신호선']):.4f}")
    col4.metric("MA5", f"{float(selected_row['MA5']):,.0f}원")
    col5.metric("MA20", f"{float(selected_row['MA20']):,.0f}원")
    st.warning(f"신뢰도: {selected_row['신뢰도']}")
    st.markdown("---")
    prompt = f"금융 전문가처럼 {selected_row['날짜'].strftime('%Y년 %m월 %d일')}의 KOSPI를 3-4문장으로 분석하세요. 종가: {selected_row['종가']}, MACD: {float(selected_row['MACD']):.4f}"
    with st.spinner("분석 중..."):
        try:
            response = client.messages.create(model="claude-opus-4-1", max_tokens=300, messages=[{"role": "user", "content": prompt}])
            st.info(response.content[0].text)
        except:
            st.warning("AI 분석 불가 (API 키 확인 필요)")

with tab3:
    st.subheader("🔍 종합 분석")
    col1, col2 = st.columns(2)
    col1.metric("신호", signal_text)
    col2.metric("신호점수", f"{score}/4")
    st.error(f"신뢰도: {selected_row['신뢰도']} - 위양성 주의")
    st.markdown(f"### 신호 이유\n{get_explanation(selected_row)}")

with tab4:
    st.subheader("📋 일일 신호 추이")
    recent_df = df.tail(10).copy()
    sigs, scores = [], []
    for _, row in recent_df.iterrows():
        sig, sc = get_signal(row)
        sigs.append(sig)
        scores.append(sc)
    recent_df['신호'], recent_df['점수'] = sigs, scores
    
    display_df = recent_df[['날짜', '신호', '점수', 'MACD', '신호선', 'MA5']].copy()
    display_df['날짜'] = display_df['날짜'].dt.strftime('%Y.%m.%d')
    display_df['MACD'] = display_df['MACD'].astype(float).round(4)
    display_df['신호선'] = display_df['신호선'].astype(float).round(4)
    st.dataframe(display_df, use_container_width=True)
    
    st.markdown("### 📈 신호점수 추이")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=recent_df['날짜'], y=recent_df['점수'], mode='lines+markers', fill='tozeroy', 
                             line=dict(color='#1f77b4', width=5), marker=dict(size=15), fillcolor='rgba(31, 119, 180, 0.2)'))
    fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
    fig.add_hrect(y0=0, y1=4, fillcolor="green", opacity=0.1, layer="below")
    fig.add_hrect(y0=-4, y1=0, fillcolor="red", opacity=0.1, layer="below")
    for _, row in recent_df.iterrows():
        fig.add_annotation(x=row['날짜'], y=row['점수'], text=f"{int(row['점수'])}", showarrow=False, yshift=10)
    fig.update_layout(title='신호점수 변화', height=500, yaxis=dict(range=[-4.5, 4.5]))
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.subheader("📈 신호 정확도 검증")
    if len(accuracy_df) > 0:
        buy = accuracy_df[accuracy_df['신호타입'] == '매수']
        sell = accuracy_df[accuracy_df['신호타입'] == '매도']
        buy_acc = (buy['정확'].sum() / len(buy) * 100) if len(buy) > 0 else 0
        sell_acc = (sell['정확'].sum() / len(sell) * 100) if len(sell) > 0 else 0
        total_acc = (accuracy_df['정확'].sum() / len(accuracy_df) * 100) if len(accuracy_df) > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("전체 정확도", f"{total_acc:.1f}%")
        col2.metric("매수 정확도", f"{buy_acc:.1f}%")
        col3.metric("매도 정확도", f"{sell_acc:.1f}%")
        col4.metric("신호 수", f"{len(accuracy_df)}개")
        
        fig = go.Figure(data=[
            go.Bar(name='매수', x=['정확', '오류'], y=[len(buy[buy['정확']==True]), len(buy[buy['정확']==False])]),
            go.Bar(name='매도', x=['정확', '오류'], y=[len(sell[sell['정확']==True]), len(sell[sell['정확']==False])])
        ])
        fig.update_layout(title='정확도 분포', height=400, barmode='group')
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(accuracy_df.tail(20), use_container_width=True)
        st.info(f"전체 정확도: {total_acc:.1f}% | 위양성: {100-total_acc:.1f}%\n본 시스템은 참고용으로만 사용하세요.")
    else:
        st.warning("정확도 데이터 없음")

st.markdown("---")
st.markdown("""<div style='background-color: #ffe6e6; padding: 15px; border-radius: 5px;'>
<b>⚠️ 중요</b> • 신뢰도 ~40% • 위양성 주의 • 참고용만 사용 • 전문가 상담 필수
</div>""", unsafe_allow_html=True)
