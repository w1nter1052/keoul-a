import streamlit as st
import requests
import replicate
import os
from PIL import Image

# Replicate API Token 설정
REPLICATE_API_TOKEN = "발급받은_토큰_여기에_입력"
replicate.Client(api_token=REPLICATE_API_TOKEN)

# Streamlit 페이지 설정
st.set_page_config(page_title="AI로 옷 입혀주기", page_icon="👗")
st.title("👗 AI로 옷 입혀줘")

# 이미지 업로드 받기
st.subheader("전신 사진 업로드")
person_image = st.file_uploader("전신 사진을 업로드해주세요", type=["jpg", "jpeg", "png"], key="person")

st.subheader("입혀볼 옷 사진 업로드")
garment_image = st.file_uploader("입힐 옷 이미지를 업로드해주세요", type=["jpg", "jpeg", "png"], key="garment")

# 업로드된 이미지들을 Replicate에 전달하여 결과 얻기
def upload_to_replicate_cdn(file):
    url = "https://dreambooth-api-experimental.replicate.delivery/upload"
    files = {"file": (file.name, file, file.type)}
    response = requests.post(url, files=files)

    if response.status_code != 200:
        st.error(f"CDN 업로드 실패 (상태 코드: {response.status_code})")
        st.code(response.text, language='html')
        return None
    return response.json()["url"]

if person_image and garment_image:
    st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요...")

    # 사진을 CDN에 업로드
    person_url = upload_to_replicate_cdn(person_image)
    garment_url = upload_to_replicate_cdn(garment_image)

    # 두 이미지 URL을 이용해 Replicate 모델에 요청
    if person_url and garment_url:
        output = replicate.run(
            "cuuupid/idm-vton:latest",
            input={
                "human_img": person_url,
                "garment_img": garment_url,
                "garment_type": "upper_body"  # 옷의 종류(상체, 하체) 설정
            }
        )
        st.image(output, caption="AI가 입힌 결과", use_column_width=True)
else:
    st.warning("전신 사진과 옷 이미지를 모두 업로드해주세요.")
