"""
Step 3: 신호 시각화 (수정버전)
실행: python step3_visualize_fixed.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 한글 폰트 설정 (Windows)
plt.rcParams['font.family'] = 'Malgun Gothic'  # 맑은고딕

print("=" * 60)
print("📊 신호 시각화!")
print("=" * 60)

# ===== CSV 파일 찾기 =====
if os.path.exists('kospi_with_signals.csv'):
    csv_file = 'kospi_with_signals.csv'
elif os.path.exists('kospi_data.csv'):
    csv_file = 'kospi_data.csv'
else:
    print(f"\n❌ CSV 파일을 찾을 수 없습니다!")
    print(f"\n해결: 다음 순서로 실행하세요:")
    print(f"  1. python step1_load_data_fixed.py")
    print(f"  2. python step2_calculate_signals_fixed.py")
    exit()

try:
    # 데이터 로드
    df = pd.read_csv(csv_file, encoding='utf-8')
    df['날짜'] = pd.to_datetime(df['날짜'])
    
    print(f"\n✅ 파일 로드 완료: {csv_file} ({len(df)}개 행)")
    
    # 서브플롯 생성
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    
    # ===== 1. 가격 + 이동평균선 =====
    print("\n1️⃣ 가격 + 이동평균선 그리기...")
    
    ax1 = axes[0]
    ax1.plot(df['날짜'], df['종가'], label='종가', linewidth=2, color='black')
    
    # MA 계산 (있으면 표시, 없으면 skip)
    if 'MA5' in df.columns:
        ax1.plot(df['날짜'], df['MA5'], label='MA5', alpha=0.7, color='orange')
    if 'MA20' in df.columns:
        ax1.plot(df['날짜'], df['MA20'], label='MA20', alpha=0.7, color='green')
    if 'MA60' in df.columns:
        ax1.plot(df['날짜'], df['MA60'], label='MA60', alpha=0.7, color='red')
    
    ax1.set_title('KOSPI 가격 & 이동평균선', fontsize=12, fontweight='bold')
    ax1.set_ylabel('가격')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # ===== 2. RSI =====
    print("2️⃣ RSI 그리기...")
    
    ax2 = axes[1]
    if 'RSI_14' in df.columns:
        ax2.plot(df['날짜'], df['RSI_14'], label='RSI(14)', linewidth=2, color='blue')
    ax2.axhline(y=70, color='red', linestyle='--', label='과매수 (70)')
    ax2.axhline(y=30, color='green', linestyle='--', label='과매도 (30)')
    ax2.fill_between(df['날짜'], 30, 70, alpha=0.1, color='gray')
    ax2.set_title('RSI (상대강도지수)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('RSI')
    ax2.set_ylim(0, 100)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # ===== 3. MACD =====
    print("3️⃣ MACD 그리기...")
    
    ax3 = axes[2]
    if 'MACD' in df.columns:
        ax3.plot(df['날짜'], df['MACD'], label='MACD', linewidth=2, color='blue')
    if '신호선' in df.columns:
        ax3.plot(df['날짜'], df['신호선'], label='신호선', linewidth=2, color='red')
    
    ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    # 히스토그램
    if 'MACD' in df.columns and '신호선' in df.columns:
        histogram_colors = ['green' if x > 0 else 'red' for x in (df['MACD'] - df['신호선'])]
        ax3.bar(df['날짜'], df['MACD'] - df['신호선'], label='히스토그램', alpha=0.3, color=histogram_colors)
    
    ax3.set_title('MACD (이동평균수렴확산지수)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('MACD')
    ax3.set_xlabel('날짜')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # 저장
    output_image = 'kospi_signals.png'
    plt.savefig(output_image, dpi=150, bbox_inches='tight')
    print(f"\n✅ 그래프 저장: {output_image}")
    
    # 화면에 표시
    plt.show()
    
    # ===== 종합 신호 분석 =====
    print("\n" + "=" * 60)
    print("📊 최근 신호 분석")
    print("=" * 60)
    
    latest = df.iloc[-1]
    
    print(f"\n📈 현재 상태:")
    print(f"  날짜: {latest['날짜'].strftime('%Y-%m-%d')}")
    print(f"  종가: {latest['종가']:,.2f}")
    
    if 'RSI_14' in df.columns:
        print(f"\n🔍 RSI 신호:")
        print(f"  값: {latest['RSI_14']:.2f}")
        if latest['RSI_14'] > 70:
            print(f"  → 🔴 과매수 (매도 신호)")
        elif latest['RSI_14'] < 30:
            print(f"  → 🟢 과매도 (매수 신호)")
        else:
            print(f"  → ⚪ 중립")
    
    if 'MACD' in df.columns and '신호선' in df.columns:
        print(f"\n🔍 MACD 신호:")
        print(f"  MACD: {latest['MACD']:.4f}")
        print(f"  신호선: {latest['신호선']:.4f}")
        if latest['MACD'] > latest['신호선']:
            print(f"  → 🟢 상승신호 (매수)")
        else:
            print(f"  → 🔴 하락신호 (매도)")
    
    if 'MA5' in df.columns and 'MA20' in df.columns:
        print(f"\n🔍 이동평균선 신호:")
        print(f"  MA5: {latest['MA5']:.2f}")
        print(f"  MA20: {latest['MA20']:.2f}")
        if 'MA60' in df.columns:
            print(f"  MA60: {latest['MA60']:.2f}")
            if latest['MA5'] > latest['MA20'] > latest['MA60']:
                print(f"  → 🟢 강한 상승추세")
            elif latest['MA5'] > latest['MA20']:
                print(f"  → 🟡 약한 상승추세")
            elif latest['MA5'] < latest['MA20'] < latest['MA60']:
                print(f"  → 🔴 강한 하락추세")
            else:
                print(f"  → ⚫ 약한 하락추세")
        else:
            if latest['MA5'] > latest['MA20']:
                print(f"  → 🟢 상승추세")
            else:
                print(f"  → 🔴 하락추세")
    
    print("\n✅ 완료!")
    
except Exception as e:
    print(f"\n❌ 오류 발생: {e}")
    import traceback
    traceback.print_exc()