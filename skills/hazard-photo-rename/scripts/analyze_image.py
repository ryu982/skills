#!/usr/bin/env python3
"""
analyze_image.py - Anthropic Vision API로 이미지를 분석하여 촬영장소와 기계/물질 종류를 추출한다.
출력: JSON {"location": "제1공장", "machine_or_material": "프레스기계", "confidence": "high|medium|low"}
"""
import sys
import json
import base64
import os
import re

def encode_image(image_path: str) -> tuple[str, str]:
    """이미지를 base64로 인코딩하고 media_type을 반환한다."""
    ext = os.path.splitext(image_path)[1].lower()
    media_type_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    media_type = media_type_map.get(ext, "image/jpeg")

    with open(image_path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode("utf-8")
    return data, media_type


def analyze_image(image_path: str) -> dict:
    try:
        import anthropic
        client = anthropic.Anthropic()
    except ImportError:
        return _fallback_analysis(image_path)

    image_data, media_type = encode_image(image_path)

    prompt = """이 사진은 산업 현장의 위험성평가를 위해 촬영된 사진입니다.
아래 두 가지 정보를 한국어로 간결하게 추출해 주세요.

1. 촬영장소: 공장 구역명, 작업장, 창고, 사무실 등 (예: 제1공장, 용접작업장, 원자재창고, 도장작업장)
2. 기계및물질종류: 사진에서 가장 두드러지는 기계 장비명 또는 화학물질명 (예: 프레스기계, LPG가스, 황산, 컨베이어벨트, 지게차, 아세틸렌)

반드시 아래 JSON 형식으로만 응답하세요 (다른 텍스트 없이):
{
  "location": "촬영장소",
  "machine_or_material": "기계및물질종류",
  "confidence": "high 또는 medium 또는 low"
}

- 확실하지 않은 항목에는 추정 내용 뒤에 _추정을 붙이세요 (예: "용접작업장_추정")
- 전혀 알 수 없으면 "미상"으로 입력하세요
- 공백, 특수문자, 괄호는 사용하지 마세요"""

    try:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=256,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data,
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )
        raw = response.content[0].text.strip()
        # JSON 블록 추출
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        return json.loads(raw)
    except Exception as e:
        return {"location": "미상", "machine_or_material": "미상", "confidence": "low", "error": str(e)}


def _fallback_analysis(image_path: str) -> dict:
    """anthropic 패키지가 없을 때의 폴백."""
    return {
        "location": "촬영장소미상",
        "machine_or_material": "기계물질미상",
        "confidence": "low",
        "error": "anthropic 패키지가 설치되지 않았습니다."
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "이미지 경로를 인수로 전달하세요."}, ensure_ascii=False))
        sys.exit(1)
    result = analyze_image(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))
