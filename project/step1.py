import pandas as pd
import os
import glob

print("="*60)
print("📊 KOSPI 데이터 로드!")
print("="*60)

# CSV 파일 찾기 (와일드카드 사용)
csv_files = glob.glob('*.csv')

print(f"\n현재 폴더: {os.getcwd()}")
print(f"현재 폴더의 CSV 파일들:")
for file in csv_files:
    print(f"  - {file}")

if not csv_files:
    print("\n❌ CSV 파일을 찾을 수 없습니다!")
    exit()

# 첫 번째 CSV 파일 사용
csv_file = csv_files[0]
print(f"\n✅ 사용할 파일: {csv_file}")

try:
    df = pd.read_csv(csv_file, encoding='utf-8')
    
    print(f"\n✅ 로드 성공!")
    print(f"행: {len(df)}, 컬럼: {len(df.columns)}")
    print(f"\n데이터 미리보기:")
    print(df.head())
    
    # 저장
    df.to_csv('kospi_data.csv', index=False, encoding='utf-8-sig')
    print(f"\n✅ 저장: kospi_data.csv")
    
except Exception as e:
    print(f"\n❌ 오류: {e}")