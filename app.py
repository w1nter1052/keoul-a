import streamlit as st
import replicate
import os
import base64

# 환경변수에서 API 키 읽기
replicate_token = os.getenv("REPLICATE_API_TOKEN")
client = replicate.Client(api_token=replicate_token)

st.title("👗 거울아, AI로 옷 입혀줘")

person_image = st.file_uploader("고객 전신 사진 업로드", type=["jpg", "jpeg", "png"], key="person")
clothes_image = st.file_uploader("입혀볼 옷 사진 업로드", type=["jpg", "jpeg", "png"], key="clothes")

def to_base64(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

if person_image and clothes_image:
    st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요...")

    person_b64 = to_base64(person_image)
    clothes_b64 = to_base64(clothes_image)

    try:
        output = client.run(
            "cuupid/idm-vton",   # ✅ 버전 ID 제거
            input={
                "human": person_b64,
                "cloth": clothes_b64
            }
        )
        st.image(output, caption="AI가 입힌 스타일", use_column_width=True)

    except replicate.exceptions.ReplicateError as e:
        st.error(f"❌ 오류 발생: {str(e)}")
else:
    st.warning("고객 전신 사진과 옷 이미지를 모두 업로드해주세요.")
