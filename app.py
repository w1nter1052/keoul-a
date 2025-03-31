import streamlit as st
import replicate
import requests
import os

# Replicate API 토큰 (Secrets 또는 로컬 환경에서 설정)
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

# 페이지 설정
st.set_page_config(page_title="AI 옷 입히기", page_icon="🧥")
st.title("🧥 AI로 옷 입혀보기")

# 이미지 업로더
st.subheader("👤 사람 이미지 업로드")
person_img = st.file_uploader("사람 전신 이미지 (JPG, PNG)", type=["jpg", "jpeg", "png"], key="person")

st.subheader("👗 옷 이미지 업로드")
cloth_img = st.file_uploader("입힐 옷 이미지 (JPG, PNG)", type=["jpg", "jpeg", "png"], key="cloth")

# CDN 업로드 함수
def upload_to_replicate_cdn(file):
    upload_url = "https://dreambooth-api-experimental.replicate.delivery/upload"
    files = {"file": (file.name, file, file.type)}
    response = requests.post(upload_url, files=files)

    if response.status_code != 200:
        st.error(f"이미지 업로드 실패 (상태코드 {response.status_code})")
        return None

    return response.json()["url"]

# 실행 버튼
if person_img and cloth_img:
    st.info("AI가 이미지를 처리 중입니다... 잠시만 기다려 주세요!")

    person_url = upload_to_replicate_cdn(person_img)
    cloth_url = upload_to_replicate_cdn(cloth_img)

    if person_url and cloth_url:
        output = replicate_client.run(
            "wolverinn/ecommerce-virtual-try-on",
            input={
                "human_image": person_url,
                "cloth_image": cloth_url
            }
        )
        st.success("AI 옷 입히기 완료!")
        st.image(output, caption="입혀진 결과", use_column_width=True)
