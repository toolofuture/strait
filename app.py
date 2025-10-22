import streamlit as st
import os
import numpy as np
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import requests
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="Han.Eye - AI 미술품 진위감정",
    page_icon="🎨",
    layout="wide"
)

# 제목
st.title("🎨 Han.Eye - AI 미술품 진위감정 시스템")
st.markdown("**AI가 미술품의 진위를 판단하고 스스로 학습하는 시스템**")

# 사이드바
with st.sidebar:
    st.header("🔧 설정")
    
    # AI 모델 선택
    model = st.selectbox(
        "AI 모델 선택",
        ["GPT-4", "Claude-3", "Gemini-Pro"],
        index=0
    )
    
    # 분석 옵션
    st.subheader("📊 분석 옵션")
    include_anomaly = st.checkbox("이상탐지 분석", value=True)
    include_style = st.checkbox("스타일 분석", value=True)
    include_technical = st.checkbox("기술적 분석", value=True)

# 메인 컨텐츠
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📤 이미지 업로드")
    
    # 파일 업로드
    uploaded_file = st.file_uploader(
        "미술품 이미지를 업로드하세요",
        type=['png', 'jpg', 'jpeg'],
        help="PNG, JPG, JPEG 형식만 지원됩니다"
    )
    
    if uploaded_file is not None:
        # 이미지 표시
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드된 이미지", use_container_width=True)
        
        # 분석 버튼
        if st.button("🔍 AI 분석 시작", type="primary"):
            with st.spinner("AI가 작품을 분석 중입니다..."):
                # Mock AI 분석 결과
                analysis_result = {
                    "authenticity": "AUTHENTIC",
                    "confidence_score": 0.85,
                    "style_analysis": {
                        "brushwork": "붓질이 일관되고 자연스러움",
                        "color": "색채 사용이 시대적 특성과 일치",
                        "composition": "구도가 안정적이고 균형잡힘"
                    },
                    "technical_analysis": {
                        "materials": "재료가 시대와 일치",
                        "aging": "노화 패턴이 자연스러움",
                        "techniques": "기법이 작가 특성과 일치"
                    },
                    "data_completeness": {
                        "artist_info": "완전",
                        "period_info": "완전",
                        "medium_info": "완전",
                        "provenance": "완전",
                        "completeness_score": 0.9
                    },
                    "suspicious_elements": [],
                    "reasoning": "종합적인 분석 결과, 이 작품은 진품일 가능성이 높습니다"
                }
                
                # 세션에 결과 저장
                st.session_state.analysis_result = analysis_result
                st.session_state.analysis_time = datetime.now()
                
                st.success("✅ 분석 완료!")

with col2:
    st.header("📊 분석 결과")
    
    if hasattr(st.session_state, 'analysis_result'):
        result = st.session_state.analysis_result
        
        # 진위 판정
        st.subheader("🎯 진위 판정")
        
        if result["authenticity"] == "AUTHENTIC":
            st.success(f"✅ **진품** (신뢰도: {result['confidence_score']*100:.1f}%)")
        elif result["authenticity"] == "FAKE":
            st.error(f"❌ **위작** (신뢰도: {result['confidence_score']*100:.1f}%)")
        else:
            st.warning(f"⚠️ **불확실** (신뢰도: {result['confidence_score']*100:.1f}%)")
        
        # 데이터 완성도
        st.subheader("📋 데이터 완성도")
        completeness = result["data_completeness"]
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("작가 정보", completeness["artist_info"])
            st.metric("시대 정보", completeness["period_info"])
        with col_b:
            st.metric("매체 정보", completeness["medium_info"])
            st.metric("출처 정보", completeness["provenance"])
        
        st.progress(completeness["completeness_score"])
        st.caption(f"완성도: {completeness['completeness_score']*100:.1f}%")
        
        # 의심 요소
        if result["suspicious_elements"]:
            st.subheader("🚨 의심 요소")
            for element in result["suspicious_elements"]:
                st.warning(f"• {element}")
        
        # 상세 분석
        with st.expander("🔍 상세 분석 보기"):
            st.json(result)
        
        # 피드백
        st.subheader("💬 피드백")
        feedback = st.radio(
            "이 분석 결과가 정확한가요?",
            ["정확함", "부정확함", "확실하지 않음"],
            horizontal=True
        )
        
        if st.button("📝 피드백 제출"):
            st.success("피드백이 저장되었습니다! AI가 이를 학습하여 개선됩니다.")
            
            # Mock 학습 로그
            st.info("🧠 AI가 피드백을 학습 중...")
            st.progress(0.8)
            st.success("✅ 학습 완료! 다음 분석이 더 정확해집니다.")

# 푸터
st.markdown("---")
st.markdown("**Han.Eye** - AI가 미술품의 진위를 판단하고 스스로 성장하는 시스템")
st.caption("© 2025 Han.Eye Project. All rights reserved.")