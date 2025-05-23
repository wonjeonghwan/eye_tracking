# 올라락! 깨구락! (게임)

> AI 기능을 활용한 수직 플랫폼 게임<br>
> 단일 카메라에서 눈 위치 변화를 탐지하여 아이 트래킹 기능 구현

## 참여 인원
게임 파트<br>
김하늘 - 장애물 제작 <br>
이도윤 - 플레이어 기능 제작<br>
이득구 - 맵 에디팅 기능<br>

AI 파트<br>
김지민 - 맵 에셋 생성<br>
원정환 - 아이트래킹<br>
정재식 - 음성 퀴즈 제작

## 🛠 사용 기술
| 구분          | 기술/라이브러리 |
|---------------|----------------|
| Language      | Python         |
| Vision        | OpenCV, MediaPipe |
| Communication | Win32(NamedPipe)  |
| 기타          | NumPy             |


## 💧프로젝트 제작 과정
추후 링크 추가

## 🧠 프로젝트 개요

- 수직플랫폼 게임의 단조로움을 타파하고자 AI기능을 결합한 게임 개발
- 유저가 편하게 맵 생성하여 다양한 난이도와 콘텐츠를 제작할 수 있도록 함.

## 👤 담당 역할 (원정환)
### ✅ 상대 좌표 기반 아이트래킹 기능 구현

- MediaPipe FaceMesh를 활용해 눈동자 중심 좌표(468, 473번 랜드마크)를 실시간 추출
- 최초 감지된 눈동자 위치를 기준점(중앙)으로 설정한 뒤, 이전&이후 프레임의 상대적 변화량을 감지하여 시선 좌표 추정
- 눈의 움직임으로부터 dx, dy를 계산하고, 이를 화면 해상도에 맞춰 비례적으로 변환하여 커서 이동
- 너무 민감하거나 튀지 않도록 scale 값을 통해 가중치 조정
- 시선 좌표를 NamedPipe (Win32 API 기반) 를 통해 언리얼 엔진으로 실시간 전송
→ 이를 개선하기 위해 “처음 보는 위치를 화면 중앙”으로 기준화한 뒤, 상대 좌표 방식으로 부드럽게 움직이는 방식을 채택함
---

## 구현 여정
- 1st. 양쪽 눈 좌우 끝점 기준<br>
방법: Mediapipe FaceMesh에서 각 눈의 가장 왼쪽과 가장 오른쪽 랜드마크를 추출해 눈의 방향 변화를 기반으로 시선 방향을 추정.<br>
의도: "아이트래킹" 목표 설정 후 실제 구현 가능성 판단 및 방향성을 위한 프로토타입.<br>
결과: 아이트래킹 가능성은 확인하였으나, 정밀한 화면 좌표 매핑 문제로 사용자의 "시선" 을 따라가는 의도보다 '눈을 마우스볼 처럼 사용한다'는 체감이 강하여 방법 변경 시도.<br><br>

- 2nd. 코를 기준으로 상대위치 지정 + 4-points Calibration <br>
방법: 코 중심 랜드마크를 기준으로, 눈의 중심 좌표와의 상대 위치 차이를 계산하여 시선 방향을 추정.<br>
의도: 얼굴 중심을 기준으로 하여 고개 움직임 보정, '아이 트래킹' 경험 강화.<br>
개선점: 눈 위치의 변화가 코 대비 어느 방향으로 이동했는지를 파악, 4점 칼리브레이션을 통해 시선변화 기반 화면 좌표 매칭.<br>
결과: 시선을 따라가는 경험은 좋아졌으나, 얼굴 위치에 따르는 좌표값 불안정성 확대.<br><br>

- 3rd. ML을 통해 좌표 값 학습<br>
방법: 칼리브레이션 단계를 대폭 늘리고, 칼리브레이션 단계에서 수집한 시선 좌표와 얼굴 좌표 데이터를 바탕으로 선형 회귀(또는 다항 회귀)를 적용하여 화면 좌표 예측 모델을 학습.<br>
의도: 단순 기하학적 추정보다 실제 사용자 눈동자 위치와 화면 사이의 관계를 반영하기 위해 학습 기반 접근.<br>
결과: 실제 화면 좌표와의 오차를 줄이고, 다양한 얼굴 각도/거리 변화에 적용 가능한 좌표 추정 확인.<br>
또한 칼리브레이션 값을 개인별로 저장, 추가 학습 할 수 있어 사용자에 최적화된 아이트래킹 가능성 확인

- 4th. (최종 선정) 눈 위치 중심값 설정
방법: 좌우 눈의 중심 좌표(동공 또는 랜드마크 평균)를 추출 후, 해당 좌표를 화면 중심 지점으로 선정. 해당 좌표 기준으로 상대적인 변화 값을 화면에 반영. 화면에 반영하는 가중치(scale) 조절을 통해 calibration
의도: 3번째 ML을 사용한 방법에서 피로감을 유발하는 칼리브레이션 방식을 생략하고, 눈의 상대적인 이동값을 화면에 반영해보고자 함.
결과: 간편함, 화면 좌표 표현에 큰 이상치가 발생하지 않음.
## 결과(소감)
### User Experience 관점의 기술 반영<br>
- 그들은 옳고, 나는 틀리다
코 기준 상대위치, ML을 활용한 좌표값 추정 방식 모두 해당 방식을 개발하고 고민한 나(본인)는 좋은 결과를 보였으나, 주변인들에게 테스트를 시도한 결과 모두 사용에 어려움을 호소함.<br>
초기에는 "너가 잘 못써서 그런 것이다" 라고 여김. 누군가는 사용하며 움직임이 많다거나, 칼리브레이션을 하는 당시 고개를 함께 움직였고, 심지어는 칼리브레이션 때는 고개를 움직이다가 본 아이트래킹 테스트 할 때에는 눈동자만 움직이기도 하는등 다양한 행동양상을 보였음.<br>
- "개떡처럼 입력해도 찰떡처럼 알아듣는" 아이트래킹 방식을 구현하고자 기존 방식에서 얼굴 거리(크기) 변화에 따라 좌표값 변경 등을 시도하며 방법 변경 시도.<br>
하나의 카메라로 아이트래킹을 구현하는 데에 ML을 활용한 방식이 가장 '정답'에 근접하다고 고려하였으나, 팀원들 & 주변 인들의 반응은 달랐다. '칼리브레이션'의 피로도와, 해당 피로도를 감수한 이후에 합당한 범용성과 정확도를 보이지 못한다며, 빠르게 초기화 하고 사용할 수 있는 마지막 방법을 선호하였다.<br>
ML을 고수하려던 나의 태도는 '아이트래킹' 이라는 본질적인 목표에서 조금 멀어지는 방향이었을 것 이다.
