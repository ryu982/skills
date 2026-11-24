#!/usr/bin/env python3
"""
rename_files.py - 매핑 JSON을 받아 실제 파일명을 변경한다.
원본은 _원본백업_YYYYMMDD 폴더에 복사 후 변경한다.

매핑 JSON 형식:
[
  {"original_path": "/path/to/IMG_001.jpg", "new_name": "20240315_143022_제1공장_프레스기계.jpg"},
  ...
]

사용법: python3 rename_files.py <매핑JSON경로>
"""
import sys
import json
import os
import shutil
import re
from datetime import datetime


def sanitize_name(name: str, max_len: int = 20) -> str:
    """파일명 안전 처리: 특수문자 제거, 길이 제한."""
    # 허용 안 되는 문자 제거
    name = re.sub(r'[/\\:*?"<>|()\[\]{}\s]', '', name)
    # 길이 제한
    return name[:max_len]


def build_new_name(dt_str: str, location: str, machine: str, ext: str) -> str:
    """표준 파일명 생성."""
    location_clean = sanitize_name(location)
    machine_clean = sanitize_name(machine)
    ext_clean = ext.lower().lstrip(".")
    return f"{dt_str}_{location_clean}_{machine_clean}.{ext_clean}"


def rename_files(mapping_path: str):
    with open(mapping_path, "r", encoding="utf-8") as f:
        mapping = json.load(f)

    if not mapping:
        print(json.dumps({"error": "매핑 데이터가 비어 있습니다."}, ensure_ascii=False))
        sys.exit(1)

    today_str = datetime.now().strftime("%Y%m%d")
    log_name = f"rename_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    results = {"success": [], "errors": [], "log_file": log_name}

    # 첫 번째 파일 기준으로 백업 폴더 생성
    base_dir = os.path.dirname(mapping[0]["original_path"])
    backup_dir = os.path.join(base_dir, f"_원본백업_{today_str}")
    os.makedirs(backup_dir, exist_ok=True)

    # 중복 파일명 추적
    seen_names: dict = {}

    for item in mapping:
        original_path = item["original_path"]
        new_name = item["new_name"]

        # 중복 처리
        base, ext_with_dot = os.path.splitext(new_name)
        if new_name in seen_names:
            seen_names[new_name] += 1
            new_name = f"{base}_{seen_names[new_name]:02d}{ext_with_dot}"
        else:
            seen_names[new_name] = 0

        new_path = os.path.join(os.path.dirname(original_path), new_name)

        try:
            # 원본 백업
            shutil.copy2(original_path, os.path.join(backup_dir, os.path.basename(original_path)))
            # 파일명 변경
            os.rename(original_path, new_path)
            results["success"].append({
                "original": os.path.basename(original_path),
                "renamed": new_name
            })
        except Exception as e:
            results["errors"].append({
                "file": os.path.basename(original_path),
                "error": str(e)
            })

    # 로그 저장
    log_path = os.path.join(base_dir, log_name)
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"위험성평가 사진 파일명 변경 로그\n")
        f.write(f"실행일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*60}\n\n")
        f.write(f"✅ 성공 ({len(results['success'])}건)\n")
        for r in results["success"]:
            f.write(f"  {r['original']} → {r['renamed']}\n")
        if results["errors"]:
            f.write(f"\n❌ 오류 ({len(results['errors'])}건)\n")
            for e in results["errors"]:
                f.write(f"  {e['file']}: {e['error']}\n")
        f.write(f"\n백업 위치: {backup_dir}\n")

    results["backup_dir"] = backup_dir
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "매핑 JSON 경로를 인수로 전달하세요."}, ensure_ascii=False))
        sys.exit(1)
    rename_files(sys.argv[1])
