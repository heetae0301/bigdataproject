# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

print("=" * 50)
print("📊 STEP 1: 데이터 로드 및 정제")
print("=" * 50)

# CSV 파일 읽기 (cp949 인코딩)
df = pd.read_csv('코스피지수 과거 데이터.csv', encoding='cp949')

print(f"\n✅ 원본 데이터 로드됨")
print(f"형태: {df.shape}")
print(f"\n첫 5행:")
print(df.head())

# 컬럼명 정리
print(f"\n현재 컬럼명: {list(df.columns)}")

# 날짜 컬럼 찾기 (여러 가능성 처리)
date_col = None
for col in df.columns:
    if '날짜' in str(col) or '일자' in str(col) or 'Date' in str(col):
        date_col = col
        break

if date_col is None:
    date_col = df.columns[0]  # 첫 컬럼이 날짜라고 가정

# 종가 컬럼 찾기
price_col = None
for col in df.columns:
    if '종가' in str(col) or '닫기' in str(col) or '종료' in str(col) or 'Close' in str(col):
        price_col = col
        break

if price_col is None:
    price_col = df.columns[-1]  # 마지막 컬럼이 종가라고 가정

print(f"\n📍 날짜 컬럼: {date_col}")
print(f"📍 종가 컬럼: {price_col}")

# 필요한 컬럼만 선택
df = df[[date_col, price_col]].copy()
df.columns = ['날짜', '종가']

# 데이터 정제
df['날짜'] = pd.to_datetime(df['날짜'])
df = df.sort_values('날짜').reset_index(drop=True)

# 종가를 숫자로 변환 (쉼표 제거)
if df['종가'].dtype == 'object':
    df['종가'] = df['종가'].astype(str).str.replace(',', '').astype(float)

# 종가를 문자열로 변환 (쉼표 포함)
df['종가'] = df['종가'].apply(lambda x: f"{x:,.2f}")

print(f"\n✅ 데이터 정제 완료")
print(f"기간: {df['날짜'].min().strftime('%Y.%m.%d')} ~ {df['날짜'].max().strftime('%Y.%m.%d')}")
print(f"거래일: {len(df)}일")
print(f"\n마지막 5행:")
print(df.tail())

# 저장
df.to_csv('kospi_data.csv', encoding='utf-8', index=False)
print("\n" + "=" * 50)
print("✅ STEP 1 완료!")
print("저장: kospi_data.csv")
print("=" * 50)
