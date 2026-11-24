---
name: "hwp-kordoc"
description: "HWP·HWPX·HWPML 한글 파일을 읽거나 검토·요약·수정할 때 kordoc으로 마크다운 변환 후 필요한 범위만 읽는다."
---

# HWP 파일 처리 (kordoc 고정)

## 원칙
- 한글 파일(.hwp/.hwpx/.hwpml)은 반드시 kordoc으로 변환한다.
- pyhwp, hwp5txt, LibreOffice 등 다른 변환 도구는 시도하지 않는다.
- 원본은 건드리지 않고, 변환 결과는 스크래치 디렉토리에 저장한다.

## 1. 변환
단일 파일:
```
npx -y kordoc "<입력파일>" -o "<스크래치>/<파일명>.md"
```
여러 파일:
```
npx -y kordoc <파일들> -d "<스크래치>/hwp_md" --jobs 4
```
사용자가 검토 범위를 지정했으면 `--pages <범위>` 옵션을 붙인다(예: `--pages 1-3`).
표 구조가 중요한 경우에는 `--format json`도 사용할 수 있다.

## 2. 읽기
- 변환된 .md 파일을 통째로 읽지 않는다.
- Grep으로 조항·키워드 위치를 먼저 찾은 뒤, Read(offset/limit)로 필요한 부분만 읽는다.
- 변환 과정은 서술하지 않고 검토 결과만 보고한다.

## 3. 실패 시
- 배포용(암호화) 문서이거나 kordoc 오류가 나면 재시도하지 않는다.
- 오류 내용을 1문장으로 알리고, 일반 저장본 또는 PDF 저장본을 요청한다.

## 4. 수정·양식 작업 (HWPX)
실행 전 `npx -y kordoc --help`로 하위 명령을 확인한다.
- 서식 보존 수정: `npx -y kordoc patch 원본.hwpx 편집.md -o 반영.hwpx`
- 양식 채우기: `npx -y kordoc fill 양식.hwpx -f '항목=값' -o 결과.hwpx`
- 마크다운을 HWPX로 변환: `npx -y kordoc generate 문서.md -o 문서.hwpx`
- 결과물은 SendUserFile로 전달한다.