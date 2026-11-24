---
name: cheong-in-ppt
description: >
  노무법인 청인(Cheong-in) 브랜드 스타일로 프레젠테이션을 제작하는 스킬.
  "청인 스타일로 PPT 만들어줘", "청인 양식 발표자료", "노무법인 청인 프레젠테이션",
  "제안서 만들어줘", "발표자료 만들어줘" 등의 요청 시 반드시 이 스킬을 사용하라.
  두 가지 템플릿(자문제안서 스타일 / 발표자료 스타일)을 지원하며,
  청인 브랜드 컬러·레이아웃·서체·푸터를 정확히 재현한다.
---

# CHEONG-IN-PPT 스킬

노무법인 청인의 두 가지 공식 PPT 양식을 재현한다.

---

## 1. 템플릿 선택

먼저 어느 스타일로 만들지 확인한다:

| 유형 | 선택 기준 | 참조 |
|------|-----------|------|
| **자문제안서 (Proposal)** | 기업 대상 제안서, 법인 소개서, 자문 계약용 | `references/proposal-style.md` |
| **발표자료 (Presentation)** | 공공기관 제출, 입찰·심사 발표, 컨소시엄 자료 | `references/presentation-style.md` |

사용자가 명시하지 않으면 **자문제안서 스타일을 기본값**으로 사용한다.

---

## 2. 공통 제작 규칙

### 슬라이드 크기
- **와이드스크린 기본**: `13.33" × 7.5"` (pptxgenjs 기본값 유지)

### 폰트
- **한글 제목**: `나눔고딕` → 없으면 `맑은 고딕` → 없으면 `Arial`
- **한글 본문**: `맑은 고딕`
- **영문/숫자 강조**: `Arial Black` 또는 `Arial`
- pptxgenjs에서는 `fontFace` 값으로 지정

### 공통 금지사항
- 제목 아래 장식 밑줄 사용 금지
- 전체 너비 컬러 바를 배경 장식으로 사용 금지 (푸터 바는 예외)
- 크림/베이지 배경 단독 사용 금지 (카드 내부는 허용)

---

## 3. 제작 도구

**pptxgenjs** 사용 (스크래치 생성):

```bash
npm install -g pptxgenjs
node create_ppt.js
```

pptxgenjs 상세 문법은 `/mnt/skills/public/pptx/pptxgenjs.md`를 참조한다.

---

## 4. 슬라이드 구조 패턴

각 스타일의 레이아웃 패턴은 `references/` 폴더를 참조한다:

- `references/proposal-style.md` — 자문제안서 색상·레이아웃·슬라이드 패턴
- `references/presentation-style.md` — 발표자료 색상·레이아웃·슬라이드 패턴

---

## 5. QA

```bash
# 텍스트 확인
extract-text output.pptx

# 시각 변환
python /mnt/skills/public/pptx/scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
ls -1 "$PWD"/slide-*.jpg
```

시각 검수 후 다음 항목을 반드시 확인:
- 푸터 텍스트가 잘리지 않았는가
- 섹션 번호 배지가 정렬되었는가
- 금색/파란색 강조가 과도하지 않은가 (한 슬라이드에 3곳 이내)
- 텍스트 오버플로우 없는가
