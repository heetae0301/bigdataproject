import pandas as pd
import numpy as np

print("="*60)
print("📊 기술적 신호 계산!")
print("="*60)

# Step 1에서 만든 파일 로드
df = pd.read_csv('kospi_data.csv', encoding='utf-8')

print(f"\n✅ 로드 완료: {len(df)}개 행")

# 컬럼명 정리
df.columns = ['날짜', '종가', '시가', '고가', '저가', '거래량', '변동률']
df['날짜'] = pd.to_datetime(df['날짜'])

# ===== RSI 계산 =====
print("\n1️⃣ RSI 계산 중...")

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return np.nan
    deltas = np.diff(prices)
    seed = deltas[:period+1]
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down if down != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    return rsi

prices = df['종가'].str.replace(',', '').astype(float).values
rsi_values = []
for i in range(len(prices)):
    if i < 14:
        rsi_values.append(np.nan)
    else:
        rsi = calculate_rsi(prices[:i+1])
        rsi_values.append(rsi)

df['RSI_14'] = rsi_values
print(f"✅ RSI 계산 완료! 최신 값: {df['RSI_14'].iloc[-1]:.2f}")

# ===== MACD 계산 =====
print("\n2️⃣ MACD 계산 중...")

prices_clean = df['종가'].str.replace(',', '').astype(float)
ema_12 = prices_clean.ewm(span=12, adjust=False).mean()
ema_26 = prices_clean.ewm(span=26, adjust=False).mean()
df['MACD'] = ema_12 - ema_26
df['신호선'] = df['MACD'].ewm(span=9, adjust=False).mean()

print(f"✅ MACD 계산 완료! 최신 값: {df['MACD'].iloc[-1]:.4f}")

# ===== 이동평균선 계산 =====
print("\n3️⃣ 이동평균선 계산 중...")

df['MA5'] = prices_clean.rolling(window=5).mean()
df['MA20'] = prices_clean.rolling(window=20).mean()
df['MA60'] = prices_clean.rolling(window=60).mean()

print(f"✅ 이동평균선 계산 완료!")

# ===== 최근 10일 신호 =====
print("\n" + "="*60)
print("📊 최근 10일 신호")
print("="*60)

recent = df.tail(10)[['날짜', '종가', 'RSI_14', 'MACD', 'MA5', 'MA20']]
print(recent.to_string())

# CSV 저장
df.to_csv('kospi_with_signals.csv', index=False, encoding='utf-8-sig')
print(f"\n✅ 저장: kospi_with_signals.csv")