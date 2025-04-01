import os
import requests
import replicate
import streamlit as st

# 비밀 API 토큰 설정
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
replicate.Client(api_token=REPLICATE_API_TOKEN)

# 이미지 업로드 함수
def upload_to_replicate_cdn(file):
    url = "https://dreambooth-api-experimental.replicate.delivery/upload"
    files = {"file": (file.name, file, file.type)}
    response = requests.post(url, files=files)

    if response.status_code != 200:
        st.error(f"CDN 업로드 실패 (상태 코드: {response.status_code})")
        return None
    
    return response.json()["url"]

# Streamlit UI 설정
st.title("AI로 옷 입히기")

# 사용자 입력 이미지 업로드
person_image = st.file_uploader("사람 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])
garment_image = st.file_uploader("입힐 옷 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

if person_image and garment_image:
    st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요…")

    # 이미지 URL 얻기
    person_url = upload_to_replicate_cdn(person_image)
    garment_url = upload_to_replicate_cdn(garment_image)

    if person_url and garment_url:
        # AI 모델 실행
        output = replicate.run(
            "cuuupid/idm-vton:latest",
            input={
                "human_img": person_url,
                "garment_img": garment_url,
                "garment_type": "upper_body"
            }
        )
        # 결과 이미지 출력
        st.image(output, caption="AI가 입힌 결과", use_column_width=True)
