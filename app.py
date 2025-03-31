import streamlit as st
import requests
import replicate
import os

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
replicate.Client(api_token=REPLICATE_API_TOKEN)

st.set_page_config(page_title="겨울아, AI로 옷 입혀줘", page_icon="👗")
st.title("👗 겨울아, AI로 옷 입혀줘")

st.subheader("고객 전신 사진 업로드")
person_image = st.file_uploader("전신 사진을 업로드해주세요", type=["jpg", "jpeg", "png"], key="person")

st.subheader("입혀볼 옷 사진 업로드")
garment_image = st.file_uploader("입힐 옷 이미지를 업로드해주세요", type=["jpg", "jpeg", "png"], key="garment")

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
    st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요…")

    person_url = upload_to_replicate_cdn(person_image)
    garment_url = upload_to_replicate_cdn(garment_image)

    if person_url and garment_url:
        output = replicate.run(
            "cuuupid/idm-vton:latest",
            input={
                "human_img": person_url,
                "garment_img": garment_url,
                "garment_type": "upper_body"
            }
        )
        st.image(output, caption="AI가 입힌 결과", use_column_width=True)
