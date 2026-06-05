# -*- coding: utf-8 -*-
"""
기술적 지표 시각화
- MACD 차트
- 이동평균선 차트
- 가격 차트
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import os

print("=" * 50)
print("📊 STEP 3: 기술적 지표 시각화")
print("=" * 50)

# ===== Step 1: 한글 폰트 설정 =====
print("\n🔧 한글 폰트 설정 중...")

try:
    # Windows 한글 폰트
    plt.rcParams['font.family'] = 'Malgun Gothic'
    print("✅ Malgun Gothic 설정 완료")
except:
    print("⚠️ 한글 폰트 설정 실패, 기본 폰트 사용")

plt.rcParams['axes.unicode_minus'] = False

# ===== Step 2: 데이터 로드 =====
print("\n📂 데이터 로드 중...")

try:
    df = pd.read_csv('kospi_with_signals.csv', encoding='utf-8')
    print(f"✅ 로드 완료: {len(df)}개 행")
except FileNotFoundError:
    print("❌ kospi_with_signals.csv 파일을 찾을 수 없습니다!")
    exit(1)

df['날짜'] = pd.to_datetime(df['날짜'])

# ===== Step 3: 종가를 숫자로 변환 =====
if isinstance(df['종가'].iloc[0], str):
    df['종가_숫자'] = df['종가'].str.replace(',', '').astype(float)
else:
    df['종가_숫자'] = df['종가'].astype(float)

# ===== Step 4: MACD 차트 =====
print("\n📊 MACD 차트 생성 중...")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1]})

# 상단: 가격 + MA
ax1.plot(df['날짜'], df['종가_숫자'], label='종가', linewidth=2, color='black')
ax1.plot(df['날짜'], df['MA5'], label='MA5', linewidth=1.5, linestyle='--', color='orange')
ax1.plot(df['날짜'], df['MA20'], label='MA20', linewidth=1.5, linestyle='--', color='green')
ax1.plot(df['날짜'], df['MA60'], label='MA60', linewidth=1.5, linestyle='--', color='red')
ax1.set_ylabel('가격 (원)', fontsize=11)
ax1.set_title('KOSPI 가격 & 이동평균선', fontsize=13, fontweight='bold')
ax1.legend(loc='best')
ax1.grid(True, alpha=0.3)

# 하단: MACD
ax2.plot(df['날짜'], df['MACD'], label='MACD', linewidth=2, color='blue')
ax2.plot(df['날짜'], df['신호선'], label='신호선', linewidth=2, color='red')

# 히스토그램
colors = ['green' if x > 0 else 'red' for x in (df['MACD'] - df['신호선'])]
ax2.bar(df['날짜'], df['MACD'] - df['신호선'], label='히스토그램', color=colors, alpha=0.3)

ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
ax2.set_ylabel('MACD', fontsize=11)
ax2.set_xlabel('날짜', fontsize=11)
ax2.set_title('MACD 지표', fontsize=13, fontweight='bold')
ax2.legend(loc='best')
ax2.grid(True, alpha=0.3)

plt.tight_layout()

# 저장
output_file = 'kospi_signals.png'
plt.savefig(output_file, dpi=150, bbox_inches='tight')
print(f"✅ MACD 차트 저장: {output_file}")

# ===== Step 5: 통계 정보 출력 =====
print("\n📊 기술적 지표 통계:")
print(f"  MACD 평균: {df['MACD'].mean():.4f}")
print(f"  MACD 범위: {df['MACD'].min():.4f} ~ {df['MACD'].max():.4f}")
print(f"  신호선 평균: {df['신호선'].mean():.4f}")
print(f"  RSI 평균: {df['RSI'].mean():.2f}")

# ===== Step 6: 신호 통계 =====
print("\n🎯 신호 통계:")
signal_counts = df['신호해석'].value_counts()
for signal, count in signal_counts.items():
    percentage = (count / len(df)) * 100
    print(f"  {signal}: {count}일 ({percentage:.1f}%)")

print("\n" + "=" * 50)
print("✅ STEP 3 완료!")
print("=" * 50)
