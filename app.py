import streamlit as st
import replicate
import os
import base64
import requests

# Replicate API 토큰 설정
replicate_token = os.getenv("REPLICATE_API_TOKEN")
client = replicate.Client(api_token=replicate_token)

st.title("👗 거울아, AI로 옷 입혀줘")

# 사용자 이미지 업로드
person_image = st.file_uploader("고객 전신 사진 업로드", type=["jpg", "jpeg", "png"], key="person")
clothes_image = st.file_uploader("입혀볼 옷 사진 업로드", type=["jpg", "jpeg", "png"], key="clothes")

# base64를 image URL로 변환하는 함수
def upload_to_replicate_cdn(image_file):
    response = requests.post(
        "https://dreambooth-api-experimental.replicate.com/v1/upload",
        headers={"Authorization": f"Token {replicate_token}"},
        files={"file": image_file},
    )
    return response.json()["url"]

if person_image and clothes_image:
    st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요...")

    # 이미지 업로드 → CDN URL
    person_url = upload_to_replicate_cdn(person_image)
    clothes_url = upload_to_replicate_cdn(clothes_image)

    # 모델 호출 (cuuupid/idm-vton)
    output = client.run(
        "cuuupid/idm-vton:0513734a452173b8173e907e3a59d19a36266e55b48528559432bd21c7d7e985",
        input={
            "human_img": person_url,
            "garm_img": clothes_url,
            "garment_des": "cute outfit"  # 설명 텍스트는 자유롭게!
        }
    )

    # 출력 이미지 표시
    st.image(output, caption="AI 스타일 합성 결과", use_column_width=True)
else:
    st.warning("고객 전신 사진과 옷 이미지를 모두 업로드해주세요.")
