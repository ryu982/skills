#!/usr/bin/env python3
"""
collect_files.py - 폴더 내 이미지 파일 목록을 재귀적으로 수집한다.
출력: JSON 배열 [{"path": "...", "filename": "...", "ext": "..."}]
"""
import sys
import json
import os

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".heic", ".heif"}


def collect_images(target_path: str) -> list:
    files = []

    if os.path.isfile(target_path):
        ext = os.path.splitext(target_path)[1].lower()
        if ext in SUPPORTED_EXTENSIONS:
            files.append({
                "path": os.path.abspath(target_path),
                "filename": os.path.basename(target_path),
                "ext": ext.lstrip(".")
            })
        else:
            print(json.dumps({"error": f"지원하지 않는 파일 형식입니다: {ext}"}, ensure_ascii=False))
            sys.exit(1)

    elif os.path.isdir(target_path):
        for root, _, filenames in os.walk(target_path):
            # 백업 폴더는 제외
            if "_원본백업_" in root:
                continue
            for fname in sorted(filenames):
                ext = os.path.splitext(fname)[1].lower()
                if ext in SUPPORTED_EXTENSIONS:
                    files.append({
                        "path": os.path.abspath(os.path.join(root, fname)),
                        "filename": fname,
                        "ext": ext.lstrip(".")
                    })
    else:
        print(json.dumps({"error": f"경로를 찾을 수 없습니다: {target_path}"}, ensure_ascii=False))
        sys.exit(1)

    return files


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "경로를 인수로 전달하세요."}, ensure_ascii=False))
        sys.exit(1)
    result = collect_images(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))
