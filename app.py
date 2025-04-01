import os
import replicate
import streamlit as st

# 비밀 API 토큰 설정
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
replicate.Client(api_token=REPLICATE_API_TOKEN)

def upload_to_replicate_cdn(file):
    url = "https://dreambooth-api-experimental.replicate.delivery/upload"
    files = {"file": (file.name, file, file.type)}
    response = requests.post(url, files=files)

    if response.status_code != 200:
        st.error(f"CDN 업로드 실패 (상태 코드: {response.status_code})")
        return None

    return response.json()["url"]

# 이미지 URL 설정 후 AI 모델 호출
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
