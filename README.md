# PsyBer: Handsign Translator

본 프로젝트는 덕성여자대학교 사이버보안전공 졸업 작품인 지능보안프로젝트(캡스톤디자인)의 일환으로 제작된 수어 번역 시스템이다.  

한국어 음성과 수어 동작을 상호 변환하는 양방향 번역 기능을 중심으로, 청인과 농인 간의 의사소통을 보조하고 한국 수어에 대한 접근성을 높이는 것을 목표로 한다.

---

## 1. Project Motivation

한국 수어는 여전히 접근성이 낮은 언어이며, 많은 청인들이 이를 배우기 어려운 환경에 놓여 있다.  

본 프로젝트는 이러한 문제를 해결하기 위해, 사용자가 일상적인 환경에서 쉽게 수어를 접하고 학습할 수 있는 시스템을 구축하는 것을 목표로 한다.

특히 다음 두 가지를 핵심 목표로 설정하였다.

- 청인이 한국 수어를 쉽게 학습하고 활용할 수 있도록 지원  
- 수어 인식 모델을 이용하여 LSTM과 Transformer의 성능을 비교 및 분석  

---

## 2. System Overview

한국어 음성과 수어 동작을 상호 변환하는 양방향 수어 번역 시스템

본 시스템은 다음과 같은 세 가지 주요 기능으로 구성된다.

### 2.1 Sign to Korean (수어 → 한국어)

사용자가 웹캠 앞에서 수어 동작을 수행하면,  
MediaPipe Holistic을 통해 실시간으로 추출된 랜드마크 데이터를 기반으로  
학습된 모델이 이를 분석하여 해당하는 한국어 단어를 출력한다.

구현 과정은 다음과 같다.

- 데이터 수집 (Data Collection)  
- 특징 추출 (Extracting)  
- 모델 학습 (Training)  
- 실시간 추론 (Inference)  

---

### 2.2 Korean to Sign (한국어 → 수어)

사용자가 마이크를 통해 한국어를 입력하면,  
Speech-to-Text(STT)를 통해 음성을 텍스트로 변환하고  
해당 단어에 대응하는 수어 영상을 재생한다.

---

### 2.3 Sign Dictionary (수어 사전)

학습된 단어 목록을 기반으로 사전 형태의 인터페이스를 제공한다.  

사용자가 단어를 선택하면 국립국어원 수어사전 페이지로 연결되어  
수어 영상, 수형 사진, 설명을 확인할 수 있다.

---

## 3. Technical Approach

### 3.1 MediaPipe Holistic

Google의 MediaPipe Holistic 모델을 사용하여 다음 정보를 실시간으로 추출한다.

- Pose landmarks (33개)  
- Face landmarks (468개)  
- Hand landmarks (21개 × 2)  

총 543개의 랜드마크를 기반으로  
각 프레임을 1662차원의 벡터로 변환하여 시계열 데이터로 구성한다.

---

### 3.2 Sequence Modeling

수어 동작은 시간에 따라 변화하는 시계열 데이터이므로  
다음 두 가지 모델을 사용하여 비교 실험을 진행하였다.

#### LSTM

- 시계열 데이터 처리에 적합한 순환 신경망  
- 장기 의존성 문제를 완화하는 구조  

#### Transformer

- Self-Attention 기반 모델  
- 시계열 전체를 병렬적으로 처리  
- 장기 의존성 문제 해결에 효과적  

---

## 4. Model Comparison

본 프로젝트는 단순 구현을 넘어, LSTM과 Transformer 모델의 실제 성능 차이를 비교하는 것을 중요한 목표로 한다.

두 모델을 동일한 데이터셋으로 학습 및 평가한 결과:

- LSTM과 Transformer 모두 시계열 처리에 적합한 성능을 보였음  
- Transformer 모델이 전반적으로 더 높은 인식률을 기록  

따라서 최종 시스템에서는 Transformer 기반 모델이 더 적합하다고 판단하였다.

---

## 5. Project Structure

PsyBer/
├── app/
│ ├── main.py
│ ├── stt_to_sign.py
│ ├── sign_to_korean.py
│ └── sign_dictionary.py
│
├── training/
│ ├── extract_keypoints.py
│ ├── train_lstm.py
│ ├── infer_lstm.py
│ ├── train_transformer.py
│ └── infer_transformer.py
│
├── sample_data/
│ └── example_sequences/
│
├── assets/
│ ├── fonts/
│ └── sign_videos/
│
├── docs/
│ └── final_report.pdf
│
└── web/

---

## 6. Sample Data

본 저장소에는 모델 구조 이해 및 테스트를 위한 일부 샘플 데이터가 포함되어 있다.

- sample_data/ 디렉토리에서 확인 가능  
- 전체 학습 데이터셋은 용량 문제로 포함되어 있지 않음  

---

## 7. How to Run

pip install -r requirements.txt
python app/main.py

---

## 8. Expected Impact

본 프로젝트를 통해 다음과 같은 효과를 기대한다.

- 청인이 수어를 보다 쉽게 학습할 수 있는 환경 제공  
- 수어 학습에 대한 진입 장벽 감소  
- 농인과 청인 간의 의사소통 활성화  

또한 사용자가 직접 수어를 수행하고 결과를 확인함으로써  
능동적인 학습 경험을 제공할 수 있다.

---

## 9. Contribution

- 데이터 수집 및 전처리  
- Feature Extracting  
- LSTM / Transformer 모델 학습 및 추론  
- 성능 비교 분석  
- STT 및 영상 출력 기능 구현  
- 수어 사전 기능 구현  
- 웹 전시 페이지 제작  
- 시스템 분석 및 개선 방향 도출  

---

## 10. Conclusion

본 프로젝트는 실생활 문제인 의사소통의 불편함에서 출발하여,  
딥러닝 기반 기술을 활용한 실질적인 해결 방안을 제시하였다.

향후에는 다음과 같은 방향으로 확장 가능하다.

- 문장 단위 번역 모델 개발  
- 데이터셋 확장  
- 실시간 정확도 개선  
- 모바일 및 웹 서비스화  

---

## 11. Author

Kim Hyunjin  
Duksung Women's University, Cyber Security Major  

---

## Tech Stack

- Python  
- PyQt5  
- OpenCV  
- MediaPipe  
- TensorFlow / Keras  
- SpeechRecognition  
- NumPy / Scikit-learn  
