import os
import replicate
import streamlit as st
import requests

# 환경 변수에서 API 토큰을 가져옵니다
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# Replicate 클라이언트 설정
replicate.Client(api_token=REPLICATE_API_TOKEN)

st.set_page_config(page_title="겨울아, AI로 옷 입혀줘", page_icon="👗")
st.title("👗 겨울아, AI로 옷 입혀줘")

# 이미지 업로드 섹션
st.subheader("고객 전신 사진 업로드")
person_image = st.file_uploader("전신 사진을 업로드해주세요", type=["jpg", "jpeg", "png"], key="person")

st.subheader("입힐 옷 사진 업로드")
garment_image = st.file_uploader("입힐 옷 이미지를 업로드해주세요", type=["jpg", "jpeg", "png"], key="garment")

# 로컬 파일로 저장하는 함수
def save_image(file, path):
    with open(path, "wb") as f:
        f.write(file.getbuffer())
    return path

if person_image and garment_image:
    st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요…")

    # 파일을 로컬에 저장
    person_image_path = save_image(person_image, "person_image.jpg")
    garment_image_path = save_image(garment_image, "garment_image.jpg")

    # 모델 호출
    output = replicate.run(
        "cuuupid/idm-vton:latest",
        input={
            "human_img": person_image_path,
            "garment_img": garment_image_path,
            "garment_type": "upper_body"
        }
    )
    st.image(output, caption="AI가 입힌 결과", use_column_width=True)
