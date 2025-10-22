import streamlit as st
import os
import base64
import json
import time
import cv2
import numpy as np
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import requests
from dotenv import load_dotenv
from reflexion import ReflexionEngine

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Han.Eye - AI 미술품 진위 감정",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
    }
    .analysis-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

class AIAnalyzer:
    """AI 분석기 클래스"""
    
    def __init__(self):
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        self.google_key = os.getenv('GOOGLE_API_KEY')
    
    def encode_image(self, image):
        """이미지를 base64로 인코딩"""
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        buffer = image.tobytes()
        return base64.b64encode(buffer).decode('utf-8')
    
    def analyze_with_gpt4(self, image, context=None):
        """GPT-4로 분석"""
        try:
            import openai
            client = openai.OpenAI(api_key=self.openai_key)
            
            # 이미지 인코딩
            base64_image = self.encode_image(image)
            
            prompt = self._build_prompt(context)
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=2000
            )
            
            return self._parse_response(response.choices[0].message.content)
            
        except Exception as e:
            return {"error": f"GPT-4 분석 오류: {str(e)}"}
    
    def analyze_with_claude(self, image, context=None):
        """Claude로 분석"""
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.anthropic_key)
            
            base64_image = self.encode_image(image)
            
            prompt = self._build_prompt(context)
            
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": base64_image,
                                },
                            },
                            {"type": "text", "text": prompt}
                        ],
                    }
                ],
            )
            
            return self._parse_response(message.content[0].text)
            
        except Exception as e:
            return {"error": f"Claude 분석 오류: {str(e)}"}
    
    def _build_prompt(self, context=None):
        """분석 프롬프트 생성"""
        prompt = """당신은 미술품 진위 감정 전문가입니다. 제공된 이미지를 분석하여 다음 항목을 평가해주세요:

1. **진품 가능성**: 이 작품이 진품일 확률을 0-100% 사이로 평가
2. **스타일 분석**: 
   - 붓질과 기법의 일관성
   - 색채 사용과 조화
   - 구도와 원근법
3. **기술적 분석**:
   - 재료와 매체의 적절성
   - 노화와 보존 상태
   - 시대적 기법 일치 여부
4. **데이터 완성도 분석**:
   - 작가 정보 누락 여부
   - 연도/시대 정보 부족
   - 매체/기법 정보 불완전
   - 출처/소장처 정보 부재
5. **의심되는 요소**: 위작일 가능성이 있는 특징들
6. **종합 판정**: AUTHENTIC (진품), FAKE (위작), UNCERTAIN (불확실)

**중요**: 정보가 누락된(null) 작품은 위작일 가능성이 높습니다. 진품은 보통 완전한 정보를 가지고 있습니다.

응답은 반드시 JSON 형식으로 제공해주세요:
{
  "authenticity": "AUTHENTIC|FAKE|UNCERTAIN",
  "confidence_score": 0.0-1.0,
  "style_analysis": {
    "brushwork": "평가 내용",
    "color": "평가 내용",
    "composition": "평가 내용"
  },
  "technical_analysis": {
    "materials": "평가 내용",
    "aging": "평가 내용",
    "techniques": "평가 내용"
  },
  "data_completeness": {
    "artist_info": "완전|부분적|누락",
    "period_info": "완전|부분적|누락",
    "medium_info": "완전|부분적|누락",
    "provenance": "완전|부분적|누락",
    "completeness_score": 0.0-1.0
  },
  "suspicious_elements": ["요소1", "요소2"],
  "reasoning": "종합적인 판단 근거"
}"""
        
        if context:
            context_str = "\n\n**작품 정보:**\n"
            if 'artist' in context:
                context_str += f"- 작가: {context['artist']}\n"
            if 'period' in context:
                context_str += f"- 시대: {context['period']}\n"
            if 'medium' in context:
                context_str += f"- 매체: {context['medium']}\n"
            prompt += context_str
        
        return prompt
    
    def _parse_response(self, content):
        """AI 응답 파싱"""
        try:
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                
                # 진위 판정 정규화
                auth = data.get('authenticity', 'UNCERTAIN').upper()
                if auth == 'AUTHENTIC':
                    is_authentic = True
                elif auth == 'FAKE':
                    is_authentic = False
                else:
                    is_authentic = None
                
                return {
                    'is_authentic': is_authentic,
                    'confidence_score': float(data.get('confidence_score', 0.5)),
                    'style_analysis': data.get('style_analysis', {}),
                    'technical_analysis': data.get('technical_analysis', {}),
                    'data_completeness': data.get('data_completeness', {}),
                    'suspicious_elements': data.get('suspicious_elements', []),
                    'reasoning': data.get('reasoning', ''),
                    'raw_response': content
                }
        except Exception as e:
            pass
        
        # 파싱 실패시 기본값
        return {
            'is_authentic': None,
            'confidence_score': 0.5,
            'style_analysis': {},
            'technical_analysis': {},
            'data_completeness': {},
            'suspicious_elements': [],
            'reasoning': '분석 결과를 파싱할 수 없습니다.',
            'raw_response': content
        }

class AnomalyDetector:
    """이상탐지 클래스"""
    
    def __init__(self):
        self.threshold = 0.7
    
    def detect_anomalies(self, image):
        """이미지 이상탐지"""
        try:
            # 이미지를 OpenCV 형식으로 변환
            if isinstance(image, Image.Image):
                image = np.array(image)
            
            # 그레이스케일 변환
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            # 텍스처 분석
            texture_score = self._analyze_texture(gray)
            
            # 엣지 분석
            edge_score = self._analyze_edges(gray)
            
            # 색상 분석
            color_score = self._analyze_colors(image)
            
            # 노이즈 분석
            noise_score = self._analyze_noise(gray)
            
            # 종합 이상점수
            anomaly_score = (texture_score + edge_score + color_score + noise_score) / 4
            
            return {
                'texture_anomaly': texture_score,
                'edge_anomaly': edge_score,
                'color_anomaly': color_score,
                'noise_anomaly': noise_score,
                'overall_anomaly': anomaly_score,
                'is_anomalous': anomaly_score > self.threshold
            }
            
        except Exception as e:
            return {"error": f"이상탐지 오류: {str(e)}"}
    
    def _analyze_texture(self, gray):
        """텍스처 분석"""
        # LBP (Local Binary Pattern) 계산
        from skimage.feature import local_binary_pattern
        lbp = local_binary_pattern(gray, 8, 1, method='uniform')
        hist, _ = np.histogram(lbp.ravel(), bins=10)
        hist = hist.astype(float)
        hist /= (hist.sum() + 1e-7)
        return 1.0 - np.sum(hist**2)  # 엔트로피 기반 이상점수
    
    def _analyze_edges(self, gray):
        """엣지 분석"""
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        return edge_density
    
    def _analyze_colors(self, image):
        """색상 분석"""
        # HSV 변환
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        
        # 색상 히스토그램
        hist_h = cv2.calcHist([hsv], [0], None, [180], [0, 180])
        hist_s = cv2.calcHist([hsv], [1], None, [256], [0, 256])
        hist_v = cv2.calcHist([hsv], [2], None, [256], [0, 256])
        
        # 히스토그램 분산 계산
        h_var = np.var(hist_h)
        s_var = np.var(hist_s)
        v_var = np.var(hist_v)
        
        return (h_var + s_var + v_var) / 3 / 1000  # 정규화
    
    def _analyze_noise(self, gray):
        """노이즈 분석"""
        # 라플라시안 필터로 노이즈 감지
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        noise_level = np.var(laplacian)
        return min(noise_level / 1000, 1.0)  # 정규화

def main():
    # 메인 헤더
    st.markdown('<h1 class="main-header">🎨 Han.Eye</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI 기반 미술품 진위 감정 시스템</p>', unsafe_allow_html=True)
    
    # 사이드바
    with st.sidebar:
        st.header("⚙️ 설정")
        
        # AI 모델 선택
        model_choice = st.selectbox(
            "AI 모델 선택",
            ["GPT-4", "Claude", "Gemini"],
            help="사용할 AI 모델을 선택하세요"
        )
        
        # 작품 정보 입력
        st.subheader("📝 작품 정보 (선택사항)")
        artist = st.text_input("작가", placeholder="예: 반 고흐")
        period = st.text_input("시대/연도", placeholder="예: 1889년")
        medium = st.text_input("매체", placeholder="예: 유화")
        
        context = {
            'artist': artist if artist else None,
            'period': period if period else None,
            'medium': medium if medium else None
        }
        
        # API 키 상태 확인
        st.subheader("🔑 API 키 상태")
        ai_analyzer = AIAnalyzer()
        
        if model_choice == "GPT-4":
            if ai_analyzer.openai_key:
                st.success("✅ OpenAI API 키 설정됨")
            else:
                st.error("❌ OpenAI API 키가 설정되지 않음")
        elif model_choice == "Claude":
            if ai_analyzer.anthropic_key:
                st.success("✅ Anthropic API 키 설정됨")
            else:
                st.error("❌ Anthropic API 키가 설정되지 않음")
        elif model_choice == "Gemini":
            if ai_analyzer.google_key:
                st.success("✅ Google API 키 설정됨")
            else:
                st.error("❌ Google API 키가 설정되지 않음")
    
    # 메인 컨텐츠
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 이미지 업로드")
        
        uploaded_file = st.file_uploader(
            "미술품 이미지를 업로드하세요",
            type=['png', 'jpg', 'jpeg'],
            help="PNG, JPG, JPEG 형식의 이미지를 업로드하세요"
        )
        
        if uploaded_file is not None:
            # 이미지 표시
            image = Image.open(uploaded_file)
            st.image(image, caption="업로드된 이미지", use_column_width=True)
            
            # 분석 버튼
            if st.button("🔍 AI 분석 시작", type="primary"):
                with st.spinner("AI가 작품을 분석 중입니다..."):
                    # AI 분석
                    if model_choice == "GPT-4":
                        ai_result = ai_analyzer.analyze_with_gpt4(image, context)
                    elif model_choice == "Claude":
                        ai_result = ai_analyzer.analyze_with_claude(image, context)
                    else:  # Gemini
                        ai_result = ai_analyzer.analyze_with_gpt4(image, context)  # 임시로 GPT-4 사용
                    
                    # 이상탐지
                    anomaly_detector = AnomalyDetector()
                    anomaly_result = anomaly_detector.detect_anomalies(image)
                    
                    # 결과 저장
                    st.session_state['ai_result'] = ai_result
                    st.session_state['anomaly_result'] = anomaly_result
                    st.session_state['image'] = image
    
    with col2:
        st.header("📊 분석 결과")
        
        if 'ai_result' in st.session_state and 'anomaly_result' in st.session_state:
            ai_result = st.session_state['ai_result']
            anomaly_result = st.session_state['anomaly_result']
            
            # 진위 판정
            st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
            
            if ai_result.get('is_authentic') is True:
                st.success("✅ **진품으로 판정**")
            elif ai_result.get('is_authentic') is False:
                st.error("❌ **위작으로 판정**")
            else:
                st.warning("⚠️ **불확실**")
            
            # 신뢰도
            confidence = ai_result.get('confidence_score', 0.5)
            st.metric("신뢰도", f"{confidence:.1%}")
            
            # 진행바
            st.progress(confidence)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 상세 분석
            st.subheader("🔍 상세 분석")
            
            # 스타일 분석
            if 'style_analysis' in ai_result:
                st.markdown("**🎨 스타일 분석**")
                style = ai_result['style_analysis']
                if 'brushwork' in style:
                    st.write(f"• 붓질: {style['brushwork']}")
                if 'color' in style:
                    st.write(f"• 색채: {style['color']}")
                if 'composition' in style:
                    st.write(f"• 구도: {style['composition']}")
            
            # 기술적 분석
            if 'technical_analysis' in ai_result:
                st.markdown("**🔧 기술적 분석**")
                tech = ai_result['technical_analysis']
                if 'materials' in tech:
                    st.write(f"• 재료: {tech['materials']}")
                if 'aging' in tech:
                    st.write(f"• 노화: {tech['aging']}")
                if 'techniques' in tech:
                    st.write(f"• 기법: {tech['techniques']}")
            
            # 데이터 완성도
            if 'data_completeness' in ai_result:
                st.markdown("**📋 데이터 완성도**")
                completeness = ai_result['data_completeness']
                if 'completeness_score' in completeness:
                    score = completeness['completeness_score']
                    st.metric("정보 완성도", f"{score:.1%}")
                    st.progress(score)
            
            # 이상탐지 결과
            st.subheader("🚨 이상탐지 결과")
            
            if 'overall_anomaly' in anomaly_result:
                anomaly_score = anomaly_result['overall_anomaly']
                st.metric("이상점수", f"{anomaly_score:.2f}")
                
                # 이상탐지 차트
                fig = go.Figure(data=go.Bar(
                    x=['텍스처', '엣지', '색상', '노이즈'],
                    y=[
                        anomaly_result.get('texture_anomaly', 0),
                        anomaly_result.get('edge_anomaly', 0),
                        anomaly_result.get('color_anomaly', 0),
                        anomaly_result.get('noise_anomaly', 0)
                    ],
                    marker_color=['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4']
                ))
                fig.update_layout(
                    title="이상탐지 세부 점수",
                    xaxis_title="분석 항목",
                    yaxis_title="이상점수",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # 의심 요소
            if 'suspicious_elements' in ai_result and ai_result['suspicious_elements']:
                st.markdown("**⚠️ 의심 요소**")
                for element in ai_result['suspicious_elements']:
                    st.write(f"• {element}")
            
            # 종합 판단 근거
            if 'reasoning' in ai_result:
                st.markdown("**💭 종합 판단 근거**")
                st.write(ai_result['reasoning'])
            
            # 피드백 섹션
            st.subheader("💬 피드백")
            st.write("분석 결과가 정확했나요?")
            
            col_feedback1, col_feedback2, col_feedback3 = st.columns(3)
            
            # Re-flexion 엔진 초기화
            reflexion_engine = ReflexionEngine()
            
            with col_feedback1:
                if st.button("✅ 정확함"):
                    # 피드백 기록
                    reflexion_engine.record_feedback(ai_result, 'correct')
                    st.success("피드백이 저장되었습니다!")
                    st.rerun()
            
            with col_feedback2:
                if st.button("❌ 부정확함"):
                    # 피드백 기록
                    reflexion_engine.record_feedback(ai_result, 'incorrect')
                    st.error("피드백이 저장되었습니다!")
                    st.rerun()
            
            with col_feedback3:
                if st.button("❓ 모르겠음"):
                    # 피드백 기록
                    reflexion_engine.record_feedback(ai_result, 'uncertain')
                    st.info("피드백이 저장되었습니다!")
                    st.rerun()
            
            # 학습 인사이트 표시
            insights = reflexion_engine.get_learning_insights()
            if insights['total_feedback'] > 0:
                st.subheader("📈 학습 현황")
                
                col_insight1, col_insight2 = st.columns(2)
                
                with col_insight1:
                    st.metric("총 피드백 수", insights['total_feedback'])
                    st.metric("정확도", f"{insights['accuracy_rate']:.1%}")
                
                with col_insight2:
                    if insights['common_errors']:
                        st.write("**자주 발생하는 오류:**")
                        for error in insights['common_errors']:
                            st.write(f"• {error}")
                    
                    if insights['improvement_suggestions']:
                        st.write("**개선 제안:**")
                        for suggestion in insights['improvement_suggestions']:
                            st.write(f"• {suggestion}")
    
    # 푸터
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>🎨 Han.Eye - AI 기반 미술품 진위 감정 시스템</p>
            <p>Re-flexion 자기개선 시스템으로 지속적으로 성능이 향상됩니다</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
