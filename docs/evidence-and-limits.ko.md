# 실험 수치의 범위와 원천

이 페이지는 좋은 성적만 모은 표가 아닙니다. 기록에 남은 비교 중 서사를 이해하는 데 필요한 집계를 골랐습니다. 날짜와 자료·평가 단위가 다른 수치를 하나의 발전 곡선으로 연결하지 않습니다.

**원본은 비공개입니다.** 아래 SHA-256은 인용한 문서를 식별할 뿐 내용을 공개하거나 독립 재현을 가능하게 하지는 않습니다. 이번 공개 작업은 문서·숫자·링크·개인정보 경계를 확인한 작업이며, 과거 학습과 기기 시험을 다시 실행하지 않았습니다.

각 정답은 별도 설명이 없는 한 안내된 표적입니다. 실제 사람의 시선을 독립 장비로 측정한 정답과 구분합니다. 한 사람의 개발 자료를 반복 사용한 한계도 있습니다.

## force_free

- 기록 시점: 2026-08-22
- 자료 범위: SM-S 자유 조향 2회, 정답 표적 없음
- 측정: 프레임 간 이동 중앙값 감소와 수평 반전률
- 한계: 안정성이지 화면 좌표 정확도가 아니다.
- 원천: S02

```json
{
  "median_movement_reduction_percent": [
    75,
    79
  ],
  "reversal_before_percent": [
    21.6,
    26.2
  ],
  "reversal_after_percent": [
    4.7,
    4.9
  ]
}
```

## force_target

- 기록 시점: 2026-08-22
- 자료 범위: SM-S 두 세션에서 선택, 세 번째 세션 고정 홀드아웃
- 측정: 속도형 대비 탄성 추종의 정규화 중앙 2D 오차
- 한계: 직접 좌표 대비 같은 크기의 정확도 향상이 아니다. 랩 제어 후보 비교다.
- 원천: S02

```json
{
  "before": 0.59,
  "after": 0.288,
  "direct_movement_reduction_percent": 13.4
}
```

## face_pose_missing

- 기록 시점: 2026-10-08
- 자료 범위: 과거 좌표 947행과 별도 새 실측 346행
- 측정: 얼굴 변환행렬에서 계산한 자세 추정값의 연결 여부
- 한계: 수집 연결 수정이며 모델 정확도 증가율이 아니다. 외부 장비로 잰 얼굴 각도 정답이 아니다.
- 원천: S06

```json
{
  "old_rows": 947,
  "old_matched": 0,
  "new_rows": 346,
  "new_matched": 346
}
```

## eyelid

- 기록 시점: 2026-10-08
- 자료 범위: 한 사용자 학습 45행, 반복 평가 26행, 작은 눈·자세 변경 평가 29행
- 측정: 방문 균형 상중하 구분
- 한계: 연속 Y 오차는 악화했다. 실제 깜빡임 대 아래보기 정답은 없다.
- 원천: S08

```json
{
  "repeat_before_percent": 79.861,
  "repeat_after_percent": 87.5,
  "changed_before_percent": 75.0,
  "changed_after_percent": 55.556
}
```

## error_parts_y

- 기록 시점: 2026-10-08
- 자료 범위: 동결된 한 대조 모델, 두 촬영 344평가행, 세 seed
- 측정: 세로 제곱오차 구성 비율
- 한계: 수학적 분해이지 물리적 원인의 기여율이나 실제 필터 실험이 아니다.
- 원천: S09

```json
{
  "jitter_percent": 4.196,
  "shared_bias_percent": 71.059,
  "capture_disagreement_percent": 24.745,
  "rmse_before_percent": 9.542,
  "ideal_no_jitter_rmse_percent": 9.34
}
```

## eyes

- 기록 시점: 2026-10-12
- 자료 범위: 한 사용자, 입력 복구 2025관측 중 여섯 촬영 731평가관측의 개발 비교
- 측정: 촬영·표적 균형 좌중립우 점수
- 한계: 중립·먼 거리 퇴행. 의학적 주시안이나 새 사용자 정확도 아님.
- 원천: S16, S32

```json
{
  "old_kernel_percent": 68.01,
  "left_only_percent": 58.26,
  "right_only_percent": 62.46,
  "mean_percent": 76.18,
  "separate_percent": 77.66,
  "old_far_percent": 81.55,
  "separate_far_percent": 73.21
}
```

## neutral_new

- 기록 시점: 2026-10-13
- 자료 범위: 새 세 촬영, 학습 가능 341행, 51/54방문, 촬영 전체 제외 개발 비교
- 측정: 같은 CE 커널의 새 자료 추가 전후 조건부 점수
- 한계: 전후의 왼쪽과 기존 촬영 퇴행. 학습 승인 후 독립 홀드아웃이 아니다.
- 원천: S18

```json
{
  "before_percent": 91.63,
  "after_percent": 93.78,
  "after_all_visits_percent": 88.37,
  "observed_visits": 51,
  "planned_visits": 54
}
```

## filters

- 기록 시점: 2026-10-13
- 자료 범위: 같은 평가 7촬영, 방향 전환 122개; 별도 3촬영은 따로 검사
- 측정: 원본과 인과 필터의 전환/초, 점수, 대응 성공 방문 추가 지연 p95
- 한계: 실제 눈 반응 시간·앱 전체 지연이나 새 사용자 정확도가 아니다. 모든 비퇴행 관문 통과 아님.
- 원천: S20

```json
{
  "raw": {
    "switch_per_second": 1.692,
    "score_percent": 76.72,
    "extra_p95_ms": 0,
    "new_misses": 0
  },
  "moving_average": {
    "switch_per_second": 0.835,
    "score_percent": 77.08,
    "extra_p95_ms": 294.4,
    "new_misses": 3
  },
  "ema": {
    "switch_per_second": 1.565,
    "score_percent": 76.86,
    "extra_p95_ms": 0,
    "new_misses": 0
  },
  "one_euro": {
    "switch_per_second": 1.452,
    "score_percent": 77.55,
    "extra_p95_ms": 59.6,
    "new_misses": 0
  },
  "separate_one_euro_right_recall_drop_pp": 0.48
}
```

## state

- 기록 시점: 2026-10-15
- 자료 범위: 재사용된 같은 평가 7촬영의 단일 사용자 개발 지표
- 측정: 적격 일치도와 전체 벽시계의 판정 변경·지속 오판
- 한계: 지속 오판·지연·새 미실행 퇴행으로 기본 Android 모델 미교체.
- 원천: S21

```json
{
  "raw_score_percent": 82.01,
  "candidate_score_percent": 86.04,
  "raw_switches": 82,
  "candidate_switches": 15,
  "raw_sustained_wrong_seconds": 12.039,
  "candidate_sustained_wrong_seconds": 15.552,
  "candidate_extra_delay_p95_ms": 206.8
}
```

## rust_transform

- 기록 시점: historical
- 자료 범위: SM-S 특정 영상 변환 연산과 합성 동일성 비교
- 측정: 크기가 같은 회전 변환 계산 시간
- 한계: 전체 앱 속도·릴스 FPS·발열 개선율로 확대하지 않는다.
- 원천: S24

```json
{
  "before_ms": 1.7013,
  "after_ms": 0.6482,
  "synthetic_conditions": 1388
}
```

## 원천 식별 목록

아래 이름은 비공개 프로젝트 내 상대 문서명입니다. 접근 가능한 링크나 원본 다운로드 경로가 아닙니다. 실제 촬영·학습 파일의 경로나 해시는 공개하지 않습니다.

### S01

문서: `docs/research/gaze-history-foundations-ko.md`

SHA-256: `57f4bd2e04c50cc417f0e76c7932d08fa290065d18f55b49d8b5ca6ec998ff5c`

### S02

문서: `docs/gaze-lab-ko.md`

SHA-256: `3294f24c00bedec4cbd461417897ba5f04a30dd5326a243098bcce61acabfb9e`

### S03

문서: `docs/research/gaze-appearance-channels-20261009-ko.md`

SHA-256: `7a5974bc6bed507b47cab5e54a51fa0a41dace2c7769af70a662802fb6b34dc5`

### S04

문서: `docs/blinkline-product-brief-ko.md`

SHA-256: `3f7c4931fa89a5cb66a90395a7d5675e6277fe386b33b6c7106ffdeb844fa873`

### S05

문서: `docs/research/gaze-blink-grammar-experiment-20260919-ko.md`

SHA-256: `b69bf3affc66ef5ac7fa4a04aadb33032fd60409b900b0b84f43fc32e44a94e8`

### S06

문서: `docs/research/gaze-face-angle-xy-20261008-ko.md`

SHA-256: `5986a29de61914f3726059d1d129d35bb860fd35be23353dacfec9fb77c6e578`

### S07

문서: `docs/research/gaze-face-first-20261008-ko.md`

SHA-256: `2cfb922c6ae3c90bd5fedffa6a5a1936a480c2fe1be0676c133ecbdfebe4b807`

### S08

문서: `docs/research/gaze-eyelid-vertical-20261008-ko.md`

SHA-256: `6be233ad54713901beb1242af51aae543611229bbfe6b7e1f7af62f43528b417`

### S09

문서: `docs/research/gaze-error-parts-20261008-ko.md`

SHA-256: `799c09dc678e5c3be8134a6142ced8048e8e7ab4518208ceb091a570c892c5ff`

### S10

문서: `docs/research/gaze-grid3-success-contract-20261009-ko.md`

SHA-256: `fb99c5ba723eda91c35e6955e1370314b430c07494efa31280eb8d246f477c45`

### S11

문서: `docs/research/gaze-grid3-axis-update-20261010-ko.md`

SHA-256: `b54f1f090c16380d3a8916c9f482b0b6fd8d84538da2545b3477396ffd5fc6f7`

### S12

문서: `docs/research/gaze-horizontal-root-cause-20261012-ko.md`

SHA-256: `3a7f19596bd44ea02f8302625702b4d4d210c3a683c7a26babbae1fe6ff764f8`

### S13

문서: `docs/research/gaze-horizontal-native-20261012-ko.md`

SHA-256: `e42dad5929a9d23e40d39536a81d4d85dcf73042e80954fb1f9b8e959dce92fd`

### S14

문서: `docs/research/gaze-periocular-20261012-ko.md`

SHA-256: `41a87e3de6cb1024f5071b233673afa43c2470a6f5837a88a8fa344e7d2d645b`

### S15

문서: `docs/research/gaze-horizontal-geometry-kernel-20261012-ko.md`

SHA-256: `9250d5be90937a82226ca9f0e7b7025b2ac9f5279d2d859792bdeebd262a8582`

### S16

문서: `docs/research/gaze-horizontal-eye-side-20261012-ko.md`

SHA-256: `c45663dde22c723bbeb0be4f9b15a4cb2e2a785d50ecb7e3eb89f64a701ce58d`

### S17

문서: `docs/research/gaze-eye-input-root-cause-20261013-ko.md`

SHA-256: `e9b314d648082c3d1b33d54b05cbb568aa990d35614f558e05cb1e9bd63ea7e0`

### S18

문서: `docs/research/gaze-neutral-cohort-training-20261013-ko.md`

SHA-256: `7a35dfc41a99f835e63a885cfeefff00c51cd0a97c997869032196bddbff2ec5`

### S19

문서: `docs/research/gaze-neutral-live-comparison-20261013-ko.md`

SHA-256: `c418a9bc6322610e0da5436bdad03bdf0ad414c183eba91a7946e09997a3e456`

### S20

문서: `docs/research/gaze-score-filters-20261013-ko.md`

SHA-256: `c89117e22f9708ef75258d66b944ea750919da32483ef2ae7da97d5398e01601`

### S21

문서: `docs/research/gaze-motion-state-20261015-ko.md`

SHA-256: `3a901958752182f8c1f8f23e2e96721eea6d1082f7e7462e3d5e4cd213257957`

### S22

문서: `docs/system-overview-ko.md`

SHA-256: `d6ef797c9711990eddcc64cd53d9229c6f74097fa0f70b3dacee8538f7b000c6`

### S23

문서: `docs/release-status-ko.md`

SHA-256: `ae58f68b7bc8110288257c489183fe3294b84f62d926be0ce1ec7efabd57c62f`

### S24

문서: `docs/image-preprocessing-quality-ko.md`

SHA-256: `85819b1931a2a1dc734e4f7d2e666d78f282901f43bc61f48cac5b6ab13215e2`

### S25

문서: `docs/problem-resolution-register-ko.md`

SHA-256: `25cc69c425d5da5e188bea36b01a827bede2fb63fc0c0569dd20fe73125c23cb`

### S26

문서: `docs/blinkroll-language-v2-ko.md`

SHA-256: `6d79cc7698d03f3f5ac0db3586bf57d84e99b34e78a4f9bfdb87c185900e90d0`

### S27

문서: `docs/product-evolution-and-decisions-ko.md`

SHA-256: `ec6d6267bbe6278a547910b166bdcc189c62a818532e54043a2588ff5c788a10`

### S28

문서: `docs/patent/CURRENT.md`

SHA-256: `c7fc41599d3e8acd771e8d6c11472482eb05f29b0c4edef4728149d6e09f31d0`

### S29

문서: `docs/research/gaze-blink-clutch-20261013-ko.md`

SHA-256: `dd50411041f46354b9fbe5609c3eda0c6be7206c611c85a5b9fc0bf4e241a48c`

### S30

문서: `docs/research/gaze-coordinate-feasibility-20261008-ko.md`

SHA-256: `d7e6b6e4c0c7f70474f0987bc5dde83a7905a41fecec2b99660db79b8db825a4`

### S31

문서: `docs/research/gaze-horizontal-high-resolution-20261012-ko.md`

SHA-256: `b90c7a189738614f78ffb54dacdbde57c4149f199a860260c26cdcd4ed88eefa`

### S32

문서: `docs/research/gaze-eye-neutral-scale-20261012-ko.md`

SHA-256: `188f5733dae39371379c210aa1d71643576b3969e585bd55fc1492310855396f`

### S33

문서: `docs/audits/20261007-sm-s-held-cadence-ko.md`

SHA-256: `ed9a9e45873de545ea1007136010575ea2a0e5694a7d99a2324f4250b446f7f6`

### S34

문서: `docs/audits/20261006-roll-unlock-practice-ownership.md`

SHA-256: `e6fe841896d0c4bc041fe942a5a56260696ae1b2390743982bad29b5e91eb815`

### S35

문서: `docs/audits/20260906-inference-capacity-root-fix.md`

SHA-256: `5a2588b17ccd4b71a32026d69a48f96e49601b6a2c8a8b927f0432a2feff165c`

### S36

문서: `docs/audits/20260906-variant-boundaries.md`

SHA-256: `f5a3e8835f22abe2f9f9a2ba4f1c49b8fd5ffe035a32a35ae045b62829b5a09d`

### S37

문서: `docs/play-release/r8-smoke-approval-gate-ko.md`

SHA-256: `090245c2519e01f8a559d58d36955f2df63190980511d1349420f26f0bf7174b`

### S38

문서: `docs/play-release/reading-native-20261013-ko.md`

SHA-256: `a4068d0940982cf6f7377842ef8b1a899e64b1651814df60a2c115a7352808bd`

### S39

문서: `docs/codex-work-history-analysis-2026-08-01-ko.md`

SHA-256: `95a90cd2479b6854a80b362cc494989f3b3e7b4e9ea482a801052ed082b730e9`

### S40

문서: `docs/operations/reading-practice-native-meta-20261013-ko.md`

SHA-256: `a5f25578de7d1606e1329f14484165231a8211bcbeeee8f02b48708a7a18d100`

### S41

문서: `docs/audits/20261007-current-model-input-replay-ko.md`

SHA-256: `f5d63145b29e66c1108cc02031ea3cb744e0458ee6d320db9023ee09dd140159`
