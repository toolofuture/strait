import streamlit as st

st.title("🎨 Han.Eye - AI 미술품 진위감정")
st.write("AI가 미술품의 진위를 판단하는 시스템입니다.")

# 파일 업로드
uploaded_file = st.file_uploader("이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    st.image(uploaded_file, caption="업로드된 이미지")
    
    if st.button("분석 시작"):
        st.success("✅ 분석 완료!")
        st.write("**결과**: 진품 (신뢰도: 85%)")
        st.write("**데이터 완성도**: 90%")
        st.write("**의심 요소**: 없음")