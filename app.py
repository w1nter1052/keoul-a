import streamlit as st
import replicate
import os
from PIL import Image
import io

# 1️⃣ Replicate API 키 설정
os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

# 2️⃣ 웹페이지 설정
st.set_page_config(page_title="AI 옷 입히기 👗")
st.title("👗 겨울아, AI로 옷 입혀줘")

# 3️⃣ 이미지 업로드
col1, col2 = st.columns(2)
with col1:
    person_file = st.file_uploader("👤 사람 사진 업로드", type=["jpg", "jpeg", "png"], key="person")
with col2:
    clothes_file = st.file_uploader("👗 옷 사진 업로드", type=["jpg", "jpeg", "png"], key="clothes")

# 4️⃣ 이미지 업로드 확인 후 처리
if person_file and clothes_file:
    with st.spinner("AI가 옷을 입히는 중입니다..."):

        # 이미지 바이트 읽기
        person_bytes = person_file.read()
        clothes_bytes = clothes_file.read()

        # 5️⃣ Replicate 실행 (무료 모델: wolverinn/ecommerce-virtual-try-on)
        try:
            output_url = replicate.run(
                "wolverinn/ecommerce-virtual-try-on:b278f3c471a8e64e9856ce3cb0175e02cc202c3c7c5b75d0cf5c78f30e0b3b5b",
                input={
                    "human_img": person_bytes,
                    "garment_img": clothes_bytes
                }
            )

            st.success("완성된 이미지입니다!")
            st.image(output_url, caption="👗 입혀진 결과", use_column_width=True)

        except Exception as e:
            st.error("오류가 발생했습니다:")
            st.code(str(e))
