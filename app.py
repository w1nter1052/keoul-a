import streamlit as st
import replicate
import os
import requests

# Replicate API 토큰 설정
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
replicate.Client(api_token=REPLICATE_API_TOKEN)

# Streamlit 앱 설정
st.set_page_config(page_title="AI 옷 입히기", page_icon="👗")
st.title("👗 AI로 옷 입히기")

# 이미지 업로드
st.subheader("사람 이미지 업로드")
person_image = st.file_uploader("사람 이미지를 업로드해주세요.", type=["jpg", "jpeg", "png"])

st.subheader("옷 이미지 업로드")
garment_image = st.file_uploader("입힐 옷 이미지를 업로드해주세요.", type=["jpg", "jpeg", "png"])

# 이미지 업로드 후 Replicate CDN으로 업로드하는 함수
def upload_to_replicate_cdn(file):
    url = "https://dreambooth-api-experimental.replicate.delivery/upload"
    files = {"file": (file.name, file, file.type)}
    response = requests.post(url, files=files)

    if response.status_code != 200:
        st.error(f"CDN 업로드 실패 (상태 코드: {response.status_code})")
        st.code(response.text, language='html')
        return None
    return response.json().get("url")

# 버튼을 클릭했을 때 처리하는 함수
if person_image and garment_image:
    st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요...")

    # 이미지 URL 업로드
    person_url = upload_to_replicate_cdn(person_image)
    garment_url = upload_to_replicate_cdn(garment_image)

    # URL들이 성공적으로 업로드되면 Replicate API 호출
    if person_url and garment_url:
        try:
            output = replicate.run(
                "cuuupid/idm-vton:latest",
                input={
                    "human_img": person_url,
                    "garment_img": garment_url,
                    "garment_type": "upper_body"  # 상의에 옷을 입히는 경우
                }
            )
            st.image(output, caption="AI가 입힌 결과", use_column_width=True)
        except replicate.errors.ReplicateError as e:
            st.error(f"Replicate API 호출 오류: {str(e)}")
else:
    st.warning("사람 이미지와 옷 이미지를 업로드해 주세요.")
