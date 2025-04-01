import streamlit as st
import requests
import replicate
import os

# API 토큰 설정 (Streamlit Secrets에서 설정한 값 사용)
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
replicate.Client(api_token=REPLICATE_API_TOKEN)

st.set_page_config(page_title="겨울아, AI로 옷 입혀줘", page_icon="👗")
st.title("👗 겨울아, AI로 옷 입혀줘")

st.subheader("고객 전신 사진 업로드")
person_image = st.file_uploader("전신 사진을 업로드해주세요", type=["jpg", "jpeg", "png"], key="person")

st.subheader("입혀볼 옷 사진 업로드")
garment_image = st.file_uploader("입힐 옷 이미지를 업로드해주세요", type=["jpg", "jpeg", "png"], key="garment")

# CDN에 업로드 함수
def upload_to_replicate_cdn(file):
    url = "https://dreambooth-api-experimental.replicate.delivery/upload"
    files = {"file": (file.name, file, file.type)}
    try:
        # 타임아웃 15초로 설정
        response = requests.post(url, files=files, timeout=15)  # 15초 타임아웃
        response.raise_for_status()  # 오류 발생시 예외를 발생시킴
    except requests.exceptions.RequestException as e:
        st.error(f"업로드 요청 중 오류 발생: {e}")
        return None
    
    return response.json()["url"]

# 이미지 업로드 후 AI 모델 실행
if person_image and garment_image:
    st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요…")

    # 업로드된 이미지 URL 생성
    person_url = upload_to_replicate_cdn(person_image)
    garment_url = upload_to_replicate_cdn(garment_image)

    if person_url and garment_url:
        try:
            output = replicate.run(
                "cuuupid/idm-vton:latest",
                input={
                    "human_img": person_url,
                    "garment_img": garment_url,
                    "garment_type": "upper_body"  # 예시로 "upper_body" 선택
                }
            )
            st.image(output, caption="AI가 입힌 결과", use_column_width=True)
        except Exception as e:
            st.error(f"AI 예측 요청 중 오류 발생: {e}")
