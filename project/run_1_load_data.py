"""
Step 1: 데이터 로드 및 확인 (수정버전)
실행: python step1_load_data_fixed.py
"""

import pandas as pd
import numpy as np
import os

print("=" * 60)
print("📊 KOSPI 데이터 로드!")
print("=" * 60)

# ===== CSV 파일 찾기 =====
csv_file = '코스피지수_과거_데이터.csv'

if not os.path.exists(csv_file):
    print(f"\n❌ 파일을 찾을 수 없습니다: {csv_file}")
    print(f"\n현재 폴더: {os.getcwd()}")
    print(f"현재 폴더의 파일들:")
    for file in os.listdir('.'):
        print(f"  - {file}")
    exit()

try:
    # 데이터 로드
    df = pd.read_csv(csv_file, encoding='utf-8')
    
    print(f"\n✅ 파일 로드 성공: {csv_file}")
    print("=" * 60)
    
    # 기본 정보
    print(f"\n📈 데이터 기본 정보:")
    print(f"  행 수: {len(df)}")
    print(f"  컬럼: {list(df.columns)}")
    print(f"  기간: {df.iloc[0, 0]} ~ {df.iloc[-1, 0]}")
    
    # 데이터 미리보기
    print(f"\n📋 데이터 미리보기 (처음 5개):")
    print(df.head())
    
    print(f"\n📋 데이터 미리보기 (마지막 5개):")
    print(df.tail())
    
    # 기본 통계
    print(f"\n📊 기본 통계:")
    print(df.describe())
    
    # 결측치 확인
    print(f"\n✅ 결측치 확인:")
    missing = df.isnull().sum()
    print(missing)
    
    # 현재 폴더에 저장
    output_file = 'kospi_data.csv'
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n✅ 저장 완료: {output_file}")
    
except Exception as e:
    print(f"\n❌ 오류 발생: {e}")
    print(f"파일 경로: {csv_file}")