"""
Step 2: 기술적 신호 계산 (수정버전)
실행: python step2_calculate_signals_fixed.py
"""

import pandas as pd
import numpy as np
import os

print("=" * 60)
print("📊 기술적 신호 계산!")
print("=" * 60)

# ===== CSV 파일 찾기 =====
# Step 1에서 생성된 파일 우선 사용
if os.path.exists('kospi_data.csv'):
    csv_file = 'kospi_data.csv'
elif os.path.exists('코스피지수_과거_데이터.csv'):
    csv_file = '코스피지수_과거_데이터.csv'
else:
    print(f"\n❌ CSV 파일을 찾을 수 없습니다!")
    print(f"현재 폴더: {os.getcwd()}")
    print(f"\n해결: python step1_load_data_fixed.py 를 먼저 실행하세요")
    exit()

try:
    # 데이터 로드
    df = pd.read_csv(csv_file, encoding='utf-8')
    
    print(f"\n✅ 파일 로드 완료: {csv_file} ({len(df)}개 행)")
    
    # 컬럼명 정리 (한글 → 영문)
    df.columns = ['날짜', '종가', '시가', '고가', '저가', '거래량', '변동률']
    df['날짜'] = pd.to_datetime(df['날짜'])
    
    # ===== RSI 계산 =====
    print("\n1️⃣ RSI 계산 중...")
    
    def calculate_rsi(prices, period=14):
        """RSI 계산"""
        if len(prices) < period + 1:
            return np.nan
        deltas = np.diff(prices)
        seed = deltas[:period+1]
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period
        rs = up / down if down != 0 else 0
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    prices = df['종가'].values
    rsi_values = []
    for i in range(len(prices)):
        if i < 14:
            rsi_values.append(np.nan)
        else:
            rsi = calculate_rsi(prices[:i+1])
            rsi_values.append(rsi)
    
    df['RSI_14'] = rsi_values
    print(f"✅ RSI 계산 완료!")
    print(f"  최신 RSI 값: {df['RSI_14'].iloc[-1]:.2f}")
    if df['RSI_14'].iloc[-1] > 70:
        print(f"  → 🔴 과매수 상태!")
    elif df['RSI_14'].iloc[-1] < 30:
        print(f"  → 🟢 과매도 상태!")
    else:
        print(f"  → ⚪ 중립 상태")
    
    # ===== MACD 계산 =====
    print("\n2️⃣ MACD 계산 중...")
    
    ema_12 = df['종가'].ewm(span=12, adjust=False).mean()
    ema_26 = df['종가'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema_12 - ema_26
    df['신호선'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    print(f"✅ MACD 계산 완료!")
    print(f"  최신 MACD: {df['MACD'].iloc[-1]:.4f}")
    print(f"  최신 신호선: {df['신호선'].iloc[-1]:.4f}")
    if df['MACD'].iloc[-1] > df['신호선'].iloc[-1]:
        print(f"  → 🟢 상승신호!")
    else:
        print(f"  → 🔴 하락신호!")
    
    # ===== 이동평균선 계산 =====
    print("\n3️⃣ 이동평균선 계산 중...")
    
    df['MA5'] = df['종가'].rolling(window=5).mean()
    df['MA20'] = df['종가'].rolling(window=20).mean()
    df['MA60'] = df['종가'].rolling(window=60).mean()
    
    print(f"✅ 이동평균선 계산 완료!")
    print(f"  MA5: {df['MA5'].iloc[-1]:.2f}")
    print(f"  MA20: {df['MA20'].iloc[-1]:.2f}")
    print(f"  MA60: {df['MA60'].iloc[-1]:.2f}")
    if df['MA5'].iloc[-1] > df['MA20'].iloc[-1]:
        print(f"  → 🟢 상승추세!")
    else:
        print(f"  → 🔴 하락추세!")
    
    # ===== 최근 10일 신호 =====
    print("\n" + "=" * 60)
    print("📊 최근 10일 신호")
    print("=" * 60)
    
    recent = df.tail(10)[['날짜', '종가', 'RSI_14', 'MACD', 'MA5', 'MA20']]
    print(recent.to_string())
    
    # CSV 저장
    output_file = 'kospi_with_signals.csv'
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n✅ 신호 포함 데이터 저장: {output_file}")
    
except Exception as e:
    print(f"\n❌ 오류 발생: {e}")
    import traceback
    traceback.print_exc()