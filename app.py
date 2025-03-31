import streamlit as st
import requests
from PIL import Image
import io
import os
import replicate

# ⛳ 환경 변수로부터 Replicate API 토큰 불러오기
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
client = replicate.Client(api_token=REPLICATE_API_TOKEN)

# CDN 업로드 함수 (이미지 → URL 변환)
def upload_to_replicate_cdn(image_file):
    upload_url = "https://dreambooth-api-experimental.replicate.com/v1/upload"
    headers = {"Authorization": f"Token {REPLICATE_API_TOKEN}"}

    file_bytes = image_file.read()  # ✔ 파일 바이트로 읽기
    files = {"file": (image_file.name, file_bytes)}

    response = requests.post(upload_url, headers=headers, files=files)

    if response.status_code == 200:
        return response.json()["url"]
    else:
        raise Exception(f"CDN 업로드 실패 (상태 코드: {response.status_code})\n{response.text}")


# 🖼️ Streamlit 인터페이스
st.title("👗 거울아, AI로 옷 입혀줘")

person_image = st.file_uploader("고객 전신 사진 업로드", type=["jpg", "jpeg", "png"], key="person")
clothes_image = st.file_uploader("입혀볼 옷 사진 업로드", type=["jpg", "jpeg", "png"], key="clothes")

if person_image and clothes_image:
    st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요...")

    try:
        # ⬆️ 이미지 업로드 → CDN URL
        person_url = upload_to_replicate_cdn(person_image)
        clothes_image.seek(0)  # 파일 다시 읽기 위해 포인터 초기화
        clothes_url = upload_to_replicate_cdn(clothes_image)

        # ▶️ 무료 모델 실행: cuuupid/idm-vton
        model_version = "cuuupid/idm-vton:0513734a452173b8173e907e3a59d19a36266e55b48528559432bd21c7d7e985"
        output = client.run(
            model_version,
            input={
                "human_img": person_url,
                "garment_img": clothes_url,
                "garment_des": "test cloth"
            }
        )

        # 결과 출력
        st.subheader("👚 합성 결과")
        st.image(output, caption="AI가 옷을 입힌 모습", use_column_width=True)

        # 다운로드 버튼
        img_response = requests.get(output)
        if img_response.status_code == 200:
            st.download_button("📥 결과 다운로드", data=img_response.content, file_name="ai_tryon_result.jpg", mime="image/jpeg")

    except Exception as e:
        st.error(f"에러 발생: {e}")

else:
    st.info("고객 전신 사진과 옷 이미지를 모두 업로드해주세요.")
