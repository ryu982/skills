# 자문제안서 스타일 (Proposal Style)

노무법인 청인 기업용 자문제안서·법인소개서 양식.

---

## 색상 팔레트

| 역할 | 색상 코드 | 용도 |
|------|-----------|------|
| **네이비 진** | `#262D35` | 푸터 배경, 섹션 배지 |
| **네이비 메인** | `#17375E` | 카드 헤더, 주요 구분선 |
| **네이비 라이트** | `#2A3F6A` | 섹션 배지 배경, 보조 강조 |
| **금색 강조** | `#9C7839` | 키워드 텍스트 강조, 버튼 테두리 |
| **금색 라이트** | `#E3B35F` | 아이콘 테두리, 서브 강조 |
| **크림 배경** | `#F1E9DA` | 카드 내부 배경, 노트 박스 |
| **흰색** | `#FFFFFF` | 슬라이드 배경 |
| **텍스트 기본** | `#353535` | 본문 텍스트 |

---

## 슬라이드별 레이아웃 패턴

### [커버 슬라이드]

```
┌──────────────────────────────────────────────┐
│  [배경: 건물 사진 우측, 흰색 그라데이션 오버레이]       │
│                                              │
│  노무법인  청인  靑寅          (금색+네이비 혼합) │
│  [문서 제목] 대제목             (네이비, 40pt+) │
│                                              │
│  🌐 www.cheong.in                            │
│  📞 032-212-1126~8                           │
│  📍 인천시... / 서울시...                      │
│                                              │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│ 🔰 노무법인 청인   Labor Law Firm Cheong-in  │
│              [푸터: #262D35 배경, 흰 텍스트]   │
└──────────────────────────────────────────────┘
```

**pptxgenjs 커버 핵심 코드:**
```javascript
// 커버 배경 (흰색 + 반투명 오버레이로 건물 이미지 효과를 대체)
slide.addShape(pptx.ShapeType.rect, {
  x: 0, y: 0, w: '100%', h: '100%', fill: { color: 'FFFFFF' }
});
// 우측 연한 파란 그라데이션 박스 (배경 효과)
slide.addShape(pptx.ShapeType.rect, {
  x: 4.5, y: 0, w: 8.83, h: 6.8,
  fill: { type: 'solid', color: 'D6E4F0' }, line: { color: 'D6E4F0' }
});
// 법인명 (금색)
slide.addText('노무법인 ', {
  x: 0.4, y: 2.5, w: 6, h: 0.6,
  fontSize: 22, bold: true, color: '9C7839', fontFace: '맑은 고딕'
});
// 청인 靑寅 (네이비)
slide.addText('청인 靑寅', {
  x: 1.6, y: 2.5, w: 4, h: 0.6,
  fontSize: 22, bold: true, color: '17375E', fontFace: '맑은 고딕'
});
// 대제목
slide.addText('[문서 제목]', {
  x: 0.4, y: 3.2, w: 6.5, h: 1.4,
  fontSize: 40, bold: true, color: '17375E', fontFace: '맑은 고딕'
});
// 아이콘+연락처 (폰 유니코드 대체)
slide.addText('🌐  www.cheong.in', {
  x: 0.4, y: 4.9, w: 5, h: 0.35, fontSize: 12, color: '353535'
});
```

---

### [콘텐츠 슬라이드 공통 헤더]

```
[섹션배지 #2A3F6A] [01] + 슬라이드 제목 (네이비 24pt bold)
                                    [우상단 I ● II ○ III ○ 네비게이터]
" 인용구 형태의 메인 메시지 " (중앙정렬, 18pt bold, #262D35)
```

**pptxgenjs 공통 헤더 함수:**
```javascript
function addContentHeader(slide, pptx, sectionNum, title, quote, navActive) {
  // 섹션 배지
  slide.addShape(pptx.ShapeType.rect, {
    x: 0.3, y: 0.2, w: 0.55, h: 0.55,
    fill: { color: '2A3F6A' }, line: { color: '2A3F6A' }
  });
  slide.addText(String(sectionNum).padStart(2, '0'), {
    x: 0.3, y: 0.2, w: 0.55, h: 0.55,
    fontSize: 16, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle',
    fontFace: 'Arial'
  });
  // 슬라이드 제목
  slide.addText(title, {
    x: 0.95, y: 0.2, w: 9, h: 0.55,
    fontSize: 22, bold: true, color: '17375E', valign: 'middle',
    fontFace: '맑은 고딕'
  });
  // 인용구 메시지
  if (quote) {
    slide.addText(`" ${quote} "`, {
      x: 0.5, y: 1.0, w: 12.33, h: 0.55,
      fontSize: 16, bold: true, color: '262D35', align: 'center',
      fontFace: '맑은 고딕'
    });
  }
}
```

---

### [카드 그리드 레이아웃] (2열/3열 카드)

네이비 헤더 + 아이콘, 크림 배경 본문:

```javascript
function addNavyCard(slide, x, y, w, h, headerText, bodyText) {
  // 카드 헤더 (네이비)
  slide.addShape(pptx.ShapeType.rect, {
    x, y, w, h: 0.9,
    fill: { color: '17375E' }, line: { color: '17375E' },
    rectRadius: 0.05
  });
  slide.addText(headerText, {
    x, y, w, h: 0.9,
    fontSize: 14, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle',
    fontFace: '맑은 고딕'
  });
  // 카드 본문 (크림 배경)
  slide.addShape(pptx.ShapeType.rect, {
    x, y: y + 0.9, w, h: h - 0.9,
    fill: { color: 'F1E9DA' }, line: { color: 'D4C5A9' }
  });
  slide.addText(bodyText, {
    x: x + 0.1, y: y + 1.0, w: w - 0.2, h: h - 1.1,
    fontSize: 11, color: '353535', valign: 'top', wrap: true,
    fontFace: '맑은 고딕'
  });
}
```

---

### [구분선 로우 레이아웃] (라벨+내용 행)

발표자료에도 사용되는 수평 행 카드:

```javascript
function addRowCard(slide, y, labelText, contentText, highlight) {
  // 배경 박스
  slide.addShape(pptx.ShapeType.rect, {
    x: 0.5, y, w: 12.33, h: 0.85,
    fill: { color: 'F1E9DA' }, line: { color: 'D4C5A9' }
  });
  // 레이블
  slide.addText(labelText, {
    x: 0.6, y: y + 0.05, w: 1.2, h: 0.75,
    fontSize: 11, bold: true, color: highlight || '9C7839',
    valign: 'middle', fontFace: '맑은 고딕'
  });
  // 내용
  slide.addText(contentText, {
    x: 1.9, y: y + 0.05, w: 10.8, h: 0.75,
    fontSize: 12, color: '353535', valign: 'middle', fontFace: '맑은 고딕'
  });
}
```

---

### [금색 강조 텍스트]

본문 중 키워드 강조는 금색 `#9C7839`으로, pptxgenjs `color` 속성으로 지정.
일반 텍스트와 강조 텍스트를 같은 `addText`에서 배열로 처리:

```javascript
slide.addText([
  { text: '채용 단계의 계약서 검토부터 ', options: { color: '353535' } },
  { text: '전 과정을 체계적으로 지원', options: { color: '9C7839', bold: true } },
  { text: '합니다', options: { color: '353535' } }
], { x: 0.5, y: 3.0, w: 6, h: 0.6, fontSize: 12, fontFace: '맑은 고딕' });
```

---

### [공통 푸터]

**모든 콘텐츠 슬라이드에 적용** (커버 포함):

```javascript
function addFooter(slide, pptx) {
  // 네이비 배경 바
  slide.addShape(pptx.ShapeType.rect, {
    x: 0, y: 6.9, w: '100%', h: 0.6,
    fill: { color: '262D35' }, line: { color: '262D35' }
  });
  // 로고 텍스트 (🔰 대체 — 특수문자로 처리)
  slide.addText('❧  노무법인 청인', {
    x: 0.3, y: 6.92, w: 3, h: 0.36,
    fontSize: 12, bold: true, color: 'FFFFFF', fontFace: '맑은 고딕'
  });
  slide.addText('Labor Law Firm Cheong-in', {
    x: 3.3, y: 6.95, w: 4, h: 0.3,
    fontSize: 10, color: 'AAAAAA', fontFace: 'Arial'
  });
}
```

---

## 내비게이터 (우상단 I / II / III)

섹션 구분을 나타내는 원형 버튼 3개. 현재 섹션은 네이비, 나머지는 회색.

```javascript
function addNavigator(slide, pptx, activeSection, labels) {
  // labels: ['노무법인 청인 소개', '청인의 서비스 소개', '청인의 주요실적']
  const navX = [10.5, 11.4, 12.3];
  const navLabels = ['I', 'II', 'III'];
  navLabels.forEach((label, i) => {
    const isActive = i + 1 === activeSection;
    slide.addShape(pptx.ShapeType.ellipse, {
      x: navX[i], y: 0.2, w: 0.38, h: 0.38,
      fill: { color: isActive ? '2A3F6A' : 'AAAAAA' },
      line: { color: isActive ? '2A3F6A' : 'AAAAAA' }
    });
    slide.addText(label, {
      x: navX[i], y: 0.2, w: 0.38, h: 0.38,
      fontSize: 9, bold: true, color: 'FFFFFF',
      align: 'center', valign: 'middle', fontFace: 'Arial'
    });
  });
  // 섹션 이름 레이블
  if (labels && labels[activeSection - 1]) {
    slide.addText(labels[activeSection - 1], {
      x: 9.2, y: 0.25, w: 1.2, h: 0.3,
      fontSize: 9, color: '17375E', align: 'right', fontFace: '맑은 고딕'
    });
  }
}
```
