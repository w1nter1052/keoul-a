import streamlit as st
import requests
import replicate
import os

# ✅ Replicate API 토큰 불러오기 (반드시 Secrets에 등록되어 있어야 함)
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

# ✅ 페이지 설정
st.set_page_config(page_title="겨울아, AI로 옷 입혀줘", page_icon="👗")
st.title("👗 겨울아, AI로 옷 입혀줘")
st.caption("사람 이미지와 옷 이미지를 업로드하면 AI가 가상 피팅을 해줘요!")

# ✅ 파일 업로드
uploaded_person = st.file_uploader("사람 전신 사진을 업로드하세요", type=["jpg", "jpeg", "png"], key="person")
uploaded_garment = st.file_uploader("입힐 옷 사진을 업로드하세요", type=["jpg", "jpeg", "png"], key="garment")

# ✅ Replicate CDN에 이미지 업로드 함수
def upload_to_replicate_cdn(file):
    upload_url = "https://dreambooth-api-experimental.replicate.delivery/upload"
    files = {"file": (file.name, file, file.type)}
    response = requests.post(upload_url, files=files)

    if response.status_code != 200:
        st.error(f"이미지 업로드 실패! (코드: {response.status_code})")
        st.code(response.text)
        return None
    
    return response.json()["url"]

# ✅ AI 실행
if uploaded_person and uploaded_garment:
    st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요…")

    person_url = upload_to_replicate_cdn(uploaded_person)
    garment_url = upload_to_replicate_cdn(uploaded_garment)

    if person_url and garment_url:
        try:
            output = replicate_client.run(
                "cuuupid/idm-vton:latest",
                input={
                    "human_img": person_url,
                    "garment_img": garment_url,
                    "garment_type": "upper_body"
                }
            )
            st.success("✨ AI가 옷을 입혔어요!")
            st.image(output, caption="AI 결과 이미지", use_column_width=True)
        except Exception as e:
            st.error("❌ AI 실행 실패!")
            st.code(str(e))
    else:
        st.warning("전신 사진과 옷 이미지를 모두 업로드해주세요.")
