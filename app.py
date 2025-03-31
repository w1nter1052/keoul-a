import streamlit as st
import requests
import replicate
import os

# Replicate API Key 환경변수 불러오기
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
replicate.Client(api_token=REPLICATE_API_TOKEN)

# imgbb API Key 직접 입력
IMGBB_API_KEY = "3278007c7082669b8cfe8c827c562f6c"

st.set_page_config(page_title="👗 거울아, AI로 옷 입혀줘", page_icon="🪞")
st.title("👗 거울아, AI로 옷 입혀줘")

# 파일 업로드
st.subheader("고객 전신 사진 업로드")
person_image = st.file_uploader("전신 사진을 업로드해주세요", type=["jpg", "jpeg", "png"], key="person")

st.subheader("입혀볼 옷 사진 업로드")
garment_image = st.file_uploader("입힐 옷 이미지를 업로드해주세요", type=["jpg", "jpeg", "png"], key="garment")

# imgbb에 이미지 업로드하는 함수
def upload_to_imgbb(file, key):
    upload_url = "https://api.imgbb.com/1/upload"
    files = {"image": file.getvalue()}
    params = {"key": key}
    response = requests.post(upload_url, params=params, files=files)
    if response.status_code == 200:
        return response.json()['data']['url']
    else:
        st.error("imgbb 업로드 실패")
        st.code(response.text, language='json')
        return None

# AI 합성 실행
if person_image and garment_image:
    st.info("⏳ AI가 옷을 입히는 중입니다. 잠시만 기다려주세요…")

    # 이미지 업로드 → URL 획득
    person_url = upload_to_imgbb(person_image, IMGBB_API_KEY)
    garment_url = upload_to_imgbb(garment_image, IMGBB_API_KEY)

    if person_url and garment_url:
        # AI 호출
        output = replicate.run(
            "cuuupid/idm-vton:latest",
            input={
                "human_img": person_url,
                "garment_img": garment_url,
                "garment_type": "upper_body"
            }
        )

        # 결과 이미지 출력
        st.success("✅ 옷을 입힌 결과입니다!")
        st.image(output, caption="AI가 합성한 옷 입은 모습", use_column_width=True)
else:
    st.warning("전신 사진과 옷 사진을 모두 업로드해주세요.")
