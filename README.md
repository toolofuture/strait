# 🎨 Han.Eye - Streamlit 버전

AI 기반 미술품 진위 감정 시스템의 Streamlit 구현체입니다.

## ✨ 주요 기능

- 🤖 **다중 AI 모델 지원**: GPT-4, Claude, Gemini
- 🔍 **이상탐지**: OpenCV 기반 이미지 분석
- 📊 **데이터 완성도 분석**: null 값 감지
- 🎯 **Re-flexion 시스템**: 자기개선 학습
- 📈 **실시간 시각화**: Plotly 차트
- 💬 **피드백 시스템**: 사용자 피드백 수집

## 🚀 빠른 시작

### 1. 환경 설정
```bash
# 저장소 클론
git clone <repository-url>
cd streamlit-haneye

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경변수 설정
`.env` 파일을 생성하고 API 키를 설정하세요:

```env
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

### 3. 실행
```bash
streamlit run app.py
```

## 🌐 배포

### Streamlit Cloud
1. GitHub에 코드 푸시
2. [streamlit.io](https://streamlit.io) 접속
3. "Deploy an app" 클릭
4. GitHub 저장소 연결
5. 자동 배포!

### Railway
1. [railway.app](https://railway.app) 접속
2. "Deploy from GitHub" 클릭
3. 저장소 선택
4. 자동 배포!

## 🎯 사용법

1. **이미지 업로드**: 미술품 이미지를 업로드
2. **작품 정보 입력**: 작가, 시대, 매체 정보 (선택사항)
3. **AI 모델 선택**: GPT-4, Claude, Gemini 중 선택
4. **분석 시작**: "AI 분석 시작" 버튼 클릭
5. **결과 확인**: 진위 판정, 신뢰도, 상세 분석 결과 확인
6. **피드백 제공**: 분석 결과의 정확성에 대한 피드백

## 🔧 기술 스택

- **Frontend**: Streamlit
- **AI Models**: OpenAI GPT-4, Anthropic Claude, Google Gemini
- **Computer Vision**: OpenCV, Pillow
- **Visualization**: Plotly
- **Data Processing**: NumPy, Pandas

## 📊 분석 항목

### AI 분석
- 진품 가능성 (0-100%)
- 스타일 분석 (붓질, 색채, 구도)
- 기술적 분석 (재료, 노화, 기법)
- 데이터 완성도 (작가, 연도, 매체, 출처 정보)
- 의심 요소 식별

### 이상탐지
- 텍스처 분석
- 엣지 분석
- 색상 분석
- 노이즈 분석

## 🎨 특징

- **직관적인 UI**: 사용하기 쉬운 인터페이스
- **실시간 분석**: 즉시 결과 확인
- **시각적 표현**: 차트와 그래프로 결과 표시
- **피드백 시스템**: 지속적인 학습과 개선
- **다중 모델**: 여러 AI 모델 비교 가능

## 📈 향후 계획

- [ ] Re-flexion 시스템 고도화
- [ ] 더 많은 AI 모델 지원
- [ ] 배치 분석 기능
- [ ] 사용자 계정 시스템
- [ ] 분석 히스토리 관리

## 🤝 기여

이 프로젝트에 기여하고 싶으시다면:

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 라이선스

MIT License

---

**Han.Eye** - AI와 예술이 만나 더 투명하고 신뢰할 수 있는 미술 시장을 만듭니다! 🎨✨
