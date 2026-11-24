#!/usr/bin/env python3
"""
extract_exif.py - 이미지 파일에서 EXIF 촬영일시를 추출한다.
출력: JSON {"datetime": "20240315_143022", "source": "exif|mtime|unknown"}
"""
import sys
import json
import os
from datetime import datetime

def extract_datetime(image_path: str) -> dict:
    result = {"datetime": None, "source": "unknown"}

    # 1) EXIF 시도 (pillow)
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS

        with Image.open(image_path) as img:
            exif_data = img._getexif()
            if exif_data:
                tag_map = {v: k for k, v in TAGS.items()}
                for tag_name in ("DateTimeOriginal", "DateTime"):
                    tag_id = tag_map.get(tag_name)
                    if tag_id and tag_id in exif_data:
                        raw = exif_data[tag_id]  # "2024:03:15 14:30:22"
                        dt = datetime.strptime(raw, "%Y:%m:%d %H:%M:%S")
                        result["datetime"] = dt.strftime("%Y%m%d_%H%M%S")
                        result["source"] = "exif"
                        return result
    except Exception:
        pass

    # 2) 파일 mtime 폴백
    try:
        mtime = os.path.getmtime(image_path)
        dt = datetime.fromtimestamp(mtime)
        result["datetime"] = dt.strftime("%Y%m%d_%H%M%S")
        result["source"] = "mtime"
        return result
    except Exception:
        pass

    result["datetime"] = "촬영일시미상"
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "이미지 경로를 인수로 전달하세요."}))
        sys.exit(1)
    print(json.dumps(extract_datetime(sys.argv[1]), ensure_ascii=False))
