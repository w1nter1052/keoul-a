import streamlit as st
import replicate
import requests
import os

# Replicate API 토큰 설정
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
if not REPLICATE_API_TOKEN:
    st.error("Replicate API 토큰이 설정되지 않았습니다.")
    st.stop()
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# 페이지 설정
st.set_page_config(page_title="겨울아, AI로 옷 입혀줘 👗")
st.title("👗 겨울아, AI로 옷 입혀줘")
st.write("사람 이미지와 옷 이미지를 업로드하면 AI가 가상 피팅을 해줘요!")

# 이미지 업로드
uploaded_person = st.file_uploader("사람 전신 사진을 업로드하세요", type=["jpg", "jpeg", "png"])
uploaded_clothes = st.file_uploader("입힐 옷 사진을 업로드하세요", type=["jpg", "jpeg", "png"])

def upload_to_replicate_cdn(file):
    upload_url = "https://dreambooth-api-experimental.replicate.delivery/upload"
    files = {"file": (file.name, file, file.type)}
    response = requests.post(upload_url, files=files)

    if response.status_code != 200:
        st.error(f"CDN 업로드 실패 (상태 코드: {response.status_code})")
        return None
    return response.json()["url"]

if uploaded_person and uploaded_clothes:
    st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요...")

    person_url = upload_to_replicate_cdn(uploaded_person)
    clothes_url = upload_to_replicate_cdn(uploaded_clothes)

    if person_url and clothes_url:
        try:
            output = replicate.run(
                "lucataco/virtual-try-on:latest",
                input={
                    "person": person_url,
                    "clothes": clothes_url
                }
            )
            st.image(output["output"], caption="AI가 입힌 결과", use_column_width=True)
        except Exception as e:
            st.error(f"AI 실행 중 오류 발생: {e}")
else:
    st.warning("전신 사진과 옷 사진을 모두 업로드해주세요.")
