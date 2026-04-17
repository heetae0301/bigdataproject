import ollama
import json

reviews = [
    "배송 빠르고 제품 품질도 좋아요! 재구매 의사 있습니다.",
    "불량품이 왔는데 교환도 안 해주네요. 최악입니다.",
    "가격은 저렴한데 품질은 보통이에요."
]

results = []

for review in reviews:
    response = ollama.chat(
        model="gemma3:4b",
        messages=[
            {
                "role": "system",
                "content": """당신은 쇼핑몰 리뷰 감성 분석 전문가입니다.
주어진 리뷰를 분석하고 반드시 아래 JSON 형식으로만 응답하세요.
다른 설명, 문장, 코드블록, 마크다운 없이 JSON만 출력하세요.

규칙:
1. sentiment는 "긍정", "부정", "중립" 중 하나
2. confidence는 0~1 사이 소수
3. keywords는 핵심 키워드 2개 이상
4. review_summary 필드에 리뷰를 한 문장으로 짧게 요약

출력 형식:
{"sentiment": "긍정/부정/중립", "confidence": 0.0, "keywords": ["키워드1", "키워드2"], "review_summary": "한 줄 요약"}"""
            },
            {
                "role": "user",
                "content": review
            }
        ]
    )

    raw = response["message"]["content"]

    try:
        clean = raw.strip()
        if "```json" in clean:
            clean = clean.split("```json")[1].split("```")[0].strip()
        elif "```" in clean:
            clean = clean.split("```")[1].split("```")[0].strip()

        data = json.loads(clean)
        results.append(data)

        print(f"리뷰: {review}")
        print(f"감성: {data['sentiment']}")
        print(f"확신도: {data['confidence']}")
        print(f"키워드: {data['keywords']}")
        print(f"요약: {data['review_summary']}")
    except json.JSONDecodeError:
        print(f"JSON 파싱 실패: {raw[:100]}")

    print("-" * 50)

print(f"\n총 {len(results)}개 리뷰 분석 완료")