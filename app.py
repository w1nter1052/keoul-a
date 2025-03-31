import streamlit as st
import replicate
import os

# Replicate API 키 설정
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

# 페이지 설정
st.set_page_config(page_title="AI 스타일 변환", page_icon="🎨")
st.title("🎨 사람 이미지를 AI 스타일로 변환")

# 이미지 업로드
uploaded_image = st.file_uploader("이미지를 업로드해주세요 (JPG, PNG)", type=["jpg", "jpeg", "png"])

def upload_to_replicate_cdn(file):
    upload_url = "https://dreambooth-api-experimental.replicate.delivery/upload"
    files = {"file": (file.name, file, file.type)}
    response = requests.post(upload_url, files=files)
    if response.status_code == 200:
        return response.json()["url"]
    else:
        st.error(f"업로드 실패: {response.status_code}")
        st.code(response.text, language="html")
        return None

if uploaded_image:
    st.image(uploaded_image, caption="원본 이미지", use_column_width=True)
    st.info("AI가 이미지를 변환하는 중입니다...")

    import requests
    image_url = upload_to_replicate_cdn(uploaded_image)

    if image_url:
        try:
            # 무료 모델 호출
            output = replicate.run(
                "catacolabs/vtoonify",
                input={"image": image_url}
            )
            st.image(output, caption="AI 스타일 이미지", use_column_width=True)
        except Exception as e:
            st.error("AI 실행 오류 발생")
            st.exception(e)
