import streamlit as st
from PIL import Image
import requests
import replicate
import os
import io

# 🔐 Replicate API 설정
replicate_token = os.getenv("REPLICATE_API_TOKEN")
client = replicate.Client(api_token=replicate_token)

# 📦 이미지 CDN 업로드 함수
def upload_to_replicate_cdn(image_file):
    upload_url = "https://dreambooth-api-experimental.replicate.com/v1/upload"
    headers = {"Authorization": f"Token {replicate_token}"}

    files = {"file": (image_file.name, image_file, image_file.type)}
    response = requests.post(upload_url, headers=headers, files=files)

    if response.status_code == 200:
        return response.json()["url"]
    else:
        raise Exception(f"CDN 업로드 실패 (상태 코드: {response.status_code})\n{response.text}")

# 🖼️ UI
st.title("👗 거울아, AI로 옷 입혀줘")

person_image = st.file_uploader("고객 전신 사진 업로드", type=["jpg", "jpeg", "png"], key="person")
clothes_image = st.file_uploader("입혀볼 옷 사진 업로드", type=["jpg", "jpeg", "png"], key="clothes")

if person_image and clothes_image:
    st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요...")

    try:
        # ⬆️ 이미지 업로드 to CDN
        person_url = upload_to_replicate_cdn(person_image)
        clothes_url = upload_to_replicate_cdn(clothes_image)

        # 🧠 무료 Try-On 모델 실행
        output = client.run(
            "wolverinn/ecommerce-virtual-try-on:8d9a5057a41c601f3652c66dc9f73425a8782309a8bdf66f39f44c383bedb72a",
            input={
                "image": person_url,
                "cloth": clothes_url
            }
        )

        # 🖼️ 결과 이미지 출력
        st.image(output, caption="👗 합성된 스타일", use_column_width=True)

        # 📥 다운로드 버튼
        img_bytes = requests.get(output).content
        st.download_button("📥 결과 이미지 다운로드", data=img_bytes, file_name="result.png", mime="image/png")

    except Exception as e:
        st.error(f"에러 발생: {e}")
else:
    st.info("고객 전신 사진과 옷 이미지를 모두 업로드해주세요.")
