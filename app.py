import streamlit as st
import replicate
import requests

# 페이지 설정
st.set_page_config(page_title="겨울아, AI로 옷 입혀줘", page_icon="👗")
st.title("👗 겨울아, AI로 옷 입혀줘")

# Replicate API 토큰 불러오기
REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
client = replicate.Client(api_token=REPLICATE_API_TOKEN)

# 업로드 or URL 입력
st.subheader("사람 이미지 업로드 또는 URL 입력")
uploaded_person = st.file_uploader("전신 사진 업로드", type=["jpg", "jpeg", "png"])
person_url_input = st.text_input("또는 전신 사진 URL 입력")

st.subheader("입힐 옷 이미지 업로드 또는 URL 입력")
uploaded_clothes = st.file_uploader("입힐 옷 이미지 업로드", type=["jpg", "jpeg", "png"])
clothes_url_input = st.text_input("또는 옷 사진 URL 입력")


# CDN 업로드 함수
def upload_to_replicate_cdn(file):
    upload_url = "https://dreambooth-api-experimental.replicate.delivery/upload"
    files = {"file": (file.name, file, file.type)}
    response = requests.post(upload_url, files=files)

    if response.status_code == 200:
        return response.json()["url"]
    else:
        st.error(f"CDN 업로드 실패: {response.status_code}")
        return None

# 버튼
if st.button("AI가 옷을 입혀줘!"):
    if not (uploaded_person or person_url_input) or not (uploaded_clothes or clothes_url_input):
        st.warning("전신 사진과 옷 사진을 모두 입력해주세요.")
    else:
        st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요...")

        # 이미지 URL 설정
        if uploaded_person:
            person_url = upload_to_replicate_cdn(uploaded_person)
        else:
            person_url = person_url_input

        if uploaded_clothes:
            clothes_url = upload_to_replicate_cdn(uploaded_clothes)
        else:
            clothes_url = clothes_url_input

        if person_url and clothes_url:
            try:
                output = client.run(
                    "cuuupid/idm-vton:latest",
                    input={
                        "human_img": person_url,
                        "garment_img": clothes_url,
                        "garment_type": "upper_body"
                    }
                )
                st.image(output, caption="AI가 옷을 입힌 결과", use_column_width=True)
            except Exception as e:
                st.error("AI 실행 중 오류 발생")
                st.code(str(e))
