# 발표자료 스타일 (Presentation Style)

노무법인 청인 공공기관 제출용 발표자료·사업계획서 양식.

---

## 색상 팔레트

| 역할 | 색상 코드 | 용도 |
|------|-----------|------|
| **파란색 메인** | `#0063BA` | 타이틀, 강조 텍스트, 헤더 요소 |
| **파란색 진** | `#002060` | 섹션 타이틀 대형 텍스트 |
| **파란색 라이트** | `#AACBE9` | 카드 배경, 구분선, 연한 블록 |
| **회색** | `#9E9E9E` | 구분선, 보조 텍스트, 날짜 |
| **흰색** | `#FFFFFF` | 슬라이드 배경 |
| **검정** | `#000000` | 본문 텍스트 |

---

## 슬라이드별 레이아웃 패턴

### [커버 슬라이드]

```
┌──────────────────────────────────────────────┐
│ [좌상단 파란 직사각형] │         [제목 이벤트명] │
│ 2025. 2. 18.  ────────────────────────────── │
│                                              │
│                                              │
│         제조업 등 안전보건관리체계              │
│         구축 컨설팅 수행기관                   │
│                                              │
│        사업계획서          (파랑, 80pt+)       │
│                                              │
│                                              │
│ ────────────────────────────────────────────  │
└──────────────────────────────────────────────┘
```

**pptxgenjs 커버 핵심 코드:**
```javascript
// 좌상단 파란 직사각형 (브랜드 마크)
slide.addShape(pptx.ShapeType.rect, {
  x: 0, y: 0, w: 1.8, h: 0.25,
  fill: { color: '0063BA' }, line: { color: '0063BA' }
});
// 날짜 (좌)
slide.addText('2025. 2. 18.', {
  x: 0.3, y: 0.3, w: 2.5, h: 0.3,
  fontSize: 11, color: '9E9E9E', fontFace: '맑은 고딕'
});
// 이벤트명 (우)
slide.addText('안전보건관리체계 구축 컨설팅 수행기관 선정심사\n발표회', {
  x: 7, y: 0.28, w: 6.1, h: 0.5,
  fontSize: 10, color: '9E9E9E', align: 'right', fontFace: '맑은 고딕'
});
// 수평 구분선 (상단)
slide.addShape(pptx.ShapeType.line, {
  x: 0.3, y: 0.65, w: 12.73, h: 0,
  line: { color: '9E9E9E', width: 0.5 }
});
// 부제목
slide.addText('제조업 등 안전보건관리체계\n구축 컨설팅 수행기관', {
  x: 1, y: 2.0, w: 11.33, h: 1.0,
  fontSize: 22, color: '353535', align: 'center', fontFace: '맑은 고딕'
});
// 대제목 (파랑, 크게)
slide.addText('사업계획서', {
  x: 0.5, y: 3.2, w: 12.33, h: 1.8,
  fontSize: 80, bold: true, color: '0063BA', align: 'center',
  fontFace: '맑은 고딕'
});
// 하단 구분선
slide.addShape(pptx.ShapeType.line, {
  x: 0.3, y: 6.75, w: 12.73, h: 0,
  line: { color: '9E9E9E', width: 0.5 }
});
```

---

### [콘텐츠 슬라이드 공통 헤더]

```
[좌상단 파란 직사각형]  │  이벤트명/발표회 (우상단, 회색)
[파란색 섹션 소제목]
──────────────────────────────
[좌측 세로 대형 제목]  │  [우측 콘텐츠 영역]
```

**공통 헤더 함수:**
```javascript
function addPresentationHeader(slide, pptx, sectionLabel, sectionTitle, eventName) {
  // 좌상단 파란 직사각형
  slide.addShape(pptx.ShapeType.rect, {
    x: 0, y: 0, w: 1.8, h: 0.25,
    fill: { color: '0063BA' }, line: { color: '0063BA' }
  });
  // 이벤트명 우상단
  slide.addText(eventName || '노무법인 청인', {
    x: 7, y: 0.05, w: 6.1, h: 0.4,
    fontSize: 10, color: '9E9E9E', align: 'right', fontFace: '맑은 고딕'
  });
  // 구분선
  slide.addShape(pptx.ShapeType.line, {
    x: 0.3, y: 0.5, w: 12.73, h: 0,
    line: { color: '9E9E9E', width: 0.5 }
  });
  // 섹션 소레이블 (파랑 대문자)
  if (sectionLabel) {
    slide.addText(sectionLabel, {
      x: 0.4, y: 0.6, w: 5, h: 0.35,
      fontSize: 11, bold: true, color: '0063BA', fontFace: 'Arial'
    });
  }
  // 섹션 제목
  slide.addText(sectionTitle, {
    x: 0.4, y: 0.9, w: 4, h: 1.2,
    fontSize: 36, bold: true, color: '0063BA', fontFace: '맑은 고딕',
    valign: 'top'
  });
  // 하단 구분선
  slide.addShape(pptx.ShapeType.line, {
    x: 0.3, y: 6.75, w: 12.73, h: 0,
    line: { color: '9E9E9E', width: 0.5 }
  });
}
```

---

### [연한 파란 카드 행 레이아웃]

라벨(파랑) + 내용(검정)의 수평 카드 행:

```javascript
function addBlueRowCard(slide, y, labelText, contentText) {
  // 카드 배경 (연한 파랑)
  slide.addShape(pptx.ShapeType.rect, {
    x: 4.0, y, w: 9.0, h: 0.9,
    fill: { color: 'AACBE9' }, line: { color: 'AACBE9' }
  });
  // 파랑 강조 세로선
  slide.addShape(pptx.ShapeType.rect, {
    x: 4.0, y: y + 0.1, w: 0.05, h: 0.7,
    fill: { color: '0063BA' }, line: { color: '0063BA' }
  });
  // 레이블
  slide.addText(labelText, {
    x: 4.15, y: y + 0.08, w: 1.3, h: 0.74,
    fontSize: 12, bold: true, color: '0063BA',
    valign: 'middle', fontFace: '맑은 고딕'
  });
  // 내용
  slide.addText(contentText, {
    x: 5.6, y: y + 0.08, w: 7.2, h: 0.74,
    fontSize: 13, color: '000000',
    valign: 'middle', fontFace: '맑은 고딕'
  });
}
```

---

### [목차 슬라이드]

```javascript
function addTocSlide(pptx, items, eventName) {
  const slide = pptx.addSlide();
  addPresentationHeader(slide, pptx, 'PRESENTATION CONTENTS', '목차', eventName);
  items.forEach((item, i) => {
    const y = 2.0 + i * 1.1;
    slide.addText(String(i + 1).padStart(2, '0'), {
      x: 5.5, y, w: 1.2, h: 0.45,
      fontSize: 22, bold: true, color: '0063BA', fontFace: 'Arial'
    });
    slide.addText(item, {
      x: 5.5, y: y + 0.4, w: 7, h: 0.55,
      fontSize: 20, color: '000000', fontFace: '맑은 고딕'
    });
  });
}
```

---

### [섹션 구분 슬라이드]

섹션 전환 시 사용하는 파랑 강조 슬라이드:

```javascript
function addSectionDivider(pptx, sectionNum, sectionTitle, eventName) {
  const slide = pptx.addSlide();
  addPresentationHeader(slide, pptx, null, '', eventName);
  slide.addShape(pptx.ShapeType.rect, {
    x: 0, y: 2.5, w: '100%', h: 2.5,
    fill: { color: '0063BA' }, line: { color: '0063BA' }
  });
  slide.addText(String(sectionNum).padStart(2, '0'), {
    x: 0.5, y: 2.7, w: 2, h: 0.8,
    fontSize: 60, bold: true, color: 'AACBE9', fontFace: 'Arial'
  });
  slide.addText(sectionTitle, {
    x: 0.5, y: 3.6, w: 12, h: 0.9,
    fontSize: 32, bold: true, color: 'FFFFFF', fontFace: '맑은 고딕'
  });
}
```
