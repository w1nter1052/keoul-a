import streamlit as st
import replicate

# Replicate API 토큰
import os
os.environ["REPLICATE_API_TOKEN"] = "your_api_key_here"

st.set_page_config(page_title="AI 패션 트라이온", page_icon="👗")
st.title("👗 AI로 옷 입혀보기")

st.markdown("### 👤 사람 이미지와 👗 옷 이미지로 AI 패션 테스트")

# 테스트용 이미지 URL
human_img = "https://i.imgur.com/0Z8wW9I.png"
cloth_img = "https://i.imgur.com/Nn6YFyx.png"

# 원본 이미지 표시
st.image(human_img, caption="사람 이미지", width=300)
st.image(cloth_img, caption="입힐 옷 이미지", width=300)

# 실행 버튼
if st.button("AI가 옷을 입혀줘!"):
    st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요…")

    output = replicate.run(
        "wolverinn/ecommerce-virtual-try-on",
        input={
            "human_image": human_img,
            "cloth_image": cloth_img
        }
    )

    st.success("완성!")
    st.image(output, caption="AI가 입힌 결과", use_column_width=True)
