
import pandas as pd

print("=" * 50)
print("📊 STEP 1: 데이터 로드 및 정제")
print("=" * 50)

df = pd.read_csv('코스피지수 과거 데이터.csv', encoding='cp949')

print(f"\n✅ 원본 데이터 로드됨")
print(f"형태: {df.shape}")

date_col = None
for col in df.columns:
    if '날짜' in str(col) or '일자' in str(col):
        date_col = col
        break
if date_col is None:
    date_col = df.columns[0]

price_col = None
for col in df.columns:
    if '종가' in str(col) or '닫기' in str(col):
        price_col = col
        break
if price_col is None:
    price_col = df.columns[-1]

df = df[[date_col, price_col]].copy()
df.columns = ['날짜', '종가']

df['날짜'] = pd.to_datetime(df['날짜'])
df = df.sort_values('날짜').reset_index(drop=True)

if df['종가'].dtype == 'object':
    df['종가'] = df['종가'].astype(str).str.replace(',', '').astype(float)

df['종가'] = df['종가'].apply(lambda x: f"{x:,.2f}")

print(f"\n✅ 데이터 정제 완료")
print(f"기간: {df['날짜'].min().strftime('%Y.%m.%d')} ~ {df['날짜'].max().strftime('%Y.%m.%d')}")
print(f"거래일: {len(df)}일")

df.to_csv('kospi_data.csv', encoding='utf-8', index=False)
print("\n✅ STEP 1 완료! | 저장: kospi_data.csv")
