# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

print("=" * 50)
print("📊 STEP 2: 기술적 지표 계산")
print("=" * 50)

df = pd.read_csv('kospi_data.csv', encoding='utf-8')
df['날짜'] = pd.to_datetime(df['날짜'])

# 종가를 숫자로 변환
df['종가_숫자'] = df['종가'].str.replace(',', '').astype(float)

# MACD 계산
print("\n📈 MACD 계산 중...")
ema_12 = df['종가_숫자'].ewm(span=12, adjust=False).mean()
ema_26 = df['종가_숫자'].ewm(span=26, adjust=False).mean()
df['MACD'] = ema_12 - ema_26
df['신호선'] = df['MACD'].ewm(span=9, adjust=False).mean()
df['히스토그램'] = df['MACD'] - df['신호선']

# MA 계산
print("📈 이동평균선(MA) 계산 중...")
df['MA5'] = df['종가_숫자'].rolling(window=5).mean()
df['MA20'] = df['종가_숫자'].rolling(window=20).mean()
df['MA60'] = df['종가_숫자'].rolling(window=60).mean()

# RSI 계산
print("📈 RSI 계산 중...")
def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

df['RSI'] = calculate_rsi(df['종가_숫자'], 14)

# 신호점수 계산 (MACD + MA 기반)
print("📊 신호점수 계산 중...")
def generate_signal(row):
    if pd.isna(row['MACD']) or pd.isna(row['MA5']):
        return 0
    
    score = 0
    
    # MACD 신호
    if row['MACD'] > row['신호선']:
        score += 2
    else:
        score -= 2
    
    # MA 신호
    if row['MA5'] > row['MA20'] > row['MA60']:
        score += 2
    elif row['MA5'] > row['MA20']:
        score += 1
    elif row['MA5'] < row['MA20'] < row['MA60']:
        score -= 2
    else:
        score -= 1
    
    return score

df['신호점수'] = df.apply(generate_signal, axis=1)

def interpret_signal(score):
    if score >= 3:
        return "🟢 강한 매수"
    elif score >= 1:
        return "🟡 약한 매수"
    elif score >= -1:
        return "🔵 중립"
    elif score >= -3:
        return "🟠 약한 매도"
    else:
        return "🔴 강한 매도"

df['신호해석'] = df['신호점수'].apply(interpret_signal)

# ⚠️ 신뢰도 계산 (낮음)
print("⚠️ 신뢰도 계산 중...")
def get_confidence(score):
    """신뢰도 (교수님 피드백 반영: ~40%)"""
    if score >= 3:
        return "낮음 (~35%)"
    elif score >= 1:
        return "매우낮음 (~25%)"
    elif score >= -1:
        return "극저 (~20%)"
    elif score >= -3:
        return "매우낮음 (~25%)"
    else:
        return "낮음 (~35%)"

df['신뢰도'] = df['신호점수'].apply(get_confidence)

print(f"\n✅ 지표 계산 완료")
print(f"\n마지막 5행:")
print(df[['날짜', '종가', 'MACD', '신호선', 'MA5', 'MA20', '신호해석', '신뢰도']].tail())

# NaN 처리
df = df.fillna(method='bfill').fillna(method='ffill')

# 저장
df.to_csv('kospi_with_signals.csv', encoding='utf-8', index=False)
print("\n" + "=" * 50)
print("✅ STEP 2 완료!")
print("저장: kospi_with_signals.csv")
print("=" * 50)

# 신호 분포
print("\n📊 신호 분포:")
print(df['신호해석'].value_counts())

print("\n⚠️ 신뢰도 분포:")
print(df['신뢰도'].value_counts()
