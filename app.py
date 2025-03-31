import streamlit as st
from PIL import Image
import io
import base64
import replicate
import os
import requests

# 환경변수에서 API 토큰 불러오기
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
client = replicate.Client(api_token=REPLICATE_API_TOKEN)

# Streamlit UI
st.title("👗 거울아, AI로 옷 입혀줘")

person_image = st.file_uploader("고객 전신 사진 업로드", type=["jpg", "jpeg", "png"], key="person")
clothes_image = st.file_uploader("입혀볼 옷 사진 업로드", type=["jpg", "jpeg", "png"], key="clothes")

# 이미지 업로드 체크
if person_image and clothes_image:
    st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요...")

    def to_base64(image_file):
        img = Image.open(image_file).convert("RGB")
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    try:
        person_b64 = to_base64(person_image)
        clothes_b64 = to_base64(clothes_image)

        # 예측 실행
        prediction = client.predictions.create(
            version="0513734a452173b8173e907e3a59d19a36266e55b48528559432bd21c7d7e985",  # cuuupid/idm-vton의 버전
            input={
                "human_img": person_b64,
                "garment_img": clothes_b64
            }
        )

        # 예측 결과 기다리기
        prediction.wait()

        if prediction.status == "succeeded":
            result_url = prediction.output
            st.image(result_url, caption="👗 합성된 스타일", use_column_width=True)
            st.success("완료되었습니다!")
            st.markdown(f"[결과 이미지 보기]({result_url})")
        else:
            st.error("❌ 예측에 실패했습니다. 다시 시도해 주세요.")

    except Exception as e:
        st.error(f"에러 발생: {e}")

else:
    st.warning("고객 전신 사진과 옷 이미지를 모두 업로드해주세요.")
