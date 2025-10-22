import streamlit as st
import os
import base64
import json
import time
from PIL import Image
import numpy as np
from datetime import datetime

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

def mock_ai_analysis(image, context=None):
    """Mock AI analysis for demo"""
    import random
    
    # Simulate AI analysis
    confidence = random.uniform(0.65, 0.95)
    is_authentic = random.choice([True, False, None])
    
    # Simulate analysis results
    style_analysis = {
        'brushwork': '붓질이 일관되고 숙련된 기법을 보입니다.' if is_authentic else '붓질이 부자연스럽고 일관성이 부족합니다.',
        'color': '시대적 색채 사용이 적절합니다.' if is_authentic else '색채 사용이 시대와 맞지 않습니다.',
        'composition': '구도가 균형잡혀 있습니다.' if is_authentic else '구도가 부자연스럽습니다.'
    }
    
    technical_analysis = {
        'materials': '사용된 재료가 시대와 일치합니다.' if is_authentic else '재료가 시대와 맞지 않습니다.',
        'aging': '자연스러운 노화 흔적이 관찰됩니다.' if is_authentic else '노화 흔적이 부자연스럽습니다.',
        'techniques': '시대적 기법이 정확히 적용되었습니다.' if is_authentic else '기법이 시대와 맞지 않습니다.'
    }
    
    data_completeness = {
        'artist_info': '완전' if random.random() > 0.3 else '부분적',
        'period_info': '완전' if random.random() > 0.3 else '부분적',
        'medium_info': '완전' if random.random() > 0.3 else '부분적',
        'provenance': '완전' if random.random() > 0.3 else '부분적',
        'completeness_score': random.uniform(0.6, 1.0)
    }
    
    suspicious_elements = [] if is_authentic else [
        '붓질이 부자연스러움',
        '색채 조화 불일치',
        '기법이 시대와 맞지 않음'
    ]
    
    reasoning = f"""
    이 작품은 {'진품일 가능성이 높습니다' if is_authentic else '위작일 가능성이 높습니다'}. 
    신뢰도는 {confidence:.1%}이며, {'스타일과 기법이 일관되고' if is_authentic else '여러 의심스러운 요소가 발견되었습니다'}.
    """
    
    return {
        'is_authentic': is_authentic,
        'confidence_score': confidence,
        'style_analysis': style_analysis,
        'technical_analysis': technical_analysis,
        'data_completeness': data_completeness,
        'suspicious_elements': suspicious_elements,
        'reasoning': reasoning
    }

def mock_anomaly_detection(image):
    """Mock anomaly detection"""
    import random
    
    return {
        'texture_anomaly': random.uniform(0.1, 0.9),
        'edge_anomaly': random.uniform(0.1, 0.9),
        'color_anomaly': random.uniform(0.1, 0.9),
        'noise_anomaly': random.uniform(0.1, 0.9),
        'overall_anomaly': random.uniform(0.2, 0.8),
        'is_anomalous': random.choice([True, False])
    }

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
        st.info("Demo 모드로 실행 중입니다. 실제 API 키를 설정하면 정확한 분석이 가능합니다.")
    
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
                    # Mock AI 분석
                    ai_result = mock_ai_analysis(image, context)
                    
                    # Mock 이상탐지
                    anomaly_result = mock_anomaly_detection(image)
                    
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
                import plotly.graph_objects as go
                
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
            
            with col_feedback1:
                if st.button("✅ 정확함"):
                    st.success("피드백이 저장되었습니다!")
            
            with col_feedback2:
                if st.button("❌ 부정확함"):
                    st.error("피드백이 저장되었습니다!")
            
            with col_feedback3:
                if st.button("❓ 모르겠음"):
                    st.info("피드백이 저장되었습니다!")
    
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
