import pandas as pd
import numpy as np

print("=" * 50)
print("📊 STEP 2: 기술적 지표 계산")
print("=" * 50)

df = pd.read_csv('kospi_data.csv', encoding='utf-8')
df['날짜'] = pd.to_datetime(df['날짜'])
df['종가_숫자'] = df['종가'].str.replace(',', '').astype(float)

# MACD 계산
df['EMA12'] = df['종가_숫자'].ewm(span=12, adjust=False).mean()
df['EMA26'] = df['종가_숫자'].ewm(span=26, adjust=False).mean()
df['MACD'] = df['EMA12'] - df['EMA26']
df['신호선'] = df['MACD'].ewm(span=9, adjust=False).mean()

# 이동평균선
df['MA5'] = df['종가_숫자'].rolling(window=5).mean()
df['MA20'] = df['종가_숫자'].rolling(window=20).mean()
df['MA60'] = df['종가_숫자'].rolling(window=60).mean()

# RSI 계산
delta = df['종가_숫자'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / loss
df['RSI'] = 100 - (100 / (1 + rs))

# 신호 판정
def get_signal_score(row):
    try:
        macd = float(row['MACD']) if pd.notna(row['MACD']) else 0
        signal = float(row['신호선']) if pd.notna(row['신호선']) else 0
        ma5 = float(row['MA5']) if pd.notna(row['MA5']) else 0
        ma20 = float(row['MA20']) if pd.notna(row['MA20']) else 0
        ma60 = float(row['MA60']) if pd.notna(row['MA60']) else 0
        
        score = 0
        if macd > signal:
            score += 2
        else:
            score -= 2
        
        if ma5 > ma20 > ma60:
            score += 2
        elif ma5 > ma20:
            score += 1
        else:
            score -= 1
        
        return score
    except:
        return 0

df['신호점수'] = df.apply(get_signal_score, axis=1)

# 신뢰도 설정
def get_reliability(score):
    if score >= 3:
        return "낮음 (~35%)"
    elif score >= 1:
        return "낮음 (~25%)"
    elif score >= -1:
        return "낮음 (~20%)"
    elif score >= -3:
        return "낮음 (~25%)"
    else:
        return "낮음 (~35%)"

df['신뢰도'] = df['신호점수'].apply(get_reliability)

df = df.fillna(method='bfill').fillna(method='ffill')

output_cols = ['날짜', '종가', 'MACD', '신호선', 'MA5', 'MA20', 'MA60', 'RSI', '신호점수', '신뢰도']
df[output_cols].to_csv('kospi_with_signals.csv', encoding='utf-8', index=False)

print(f"\n✅ STEP 2 완료!")
print(f"저장: kospi_with_signals.csv")
print(f"포함된 지표: MACD, 신호선, MA5/20/60, RSI, 신호점수, 신뢰도")
