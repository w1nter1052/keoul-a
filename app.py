import streamlit as st
import replicate
import os
import io
import base64
from PIL import Image

# Replicate API Key 불러오기
replicate_token = os.getenv("REPLICATE_API_TOKEN")
replicate.Client(api_token=replicate_token)

# Streamlit 제목
st.title("👗 거울아, AI로 옷 입혀줘")

# 이미지 업로드
person_image = st.file_uploader("고객 전신 사진 업로드", type=["jpg", "jpeg", "png"], key="person")
clothes_image = st.file_uploader("입혀볼 옷 사진 업로드", type=["jpg", "jpeg", "png"], key="clothes")

# 이미지 → base64 변환 함수
def to_base64(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

# 이미지가 모두 업로드된 경우 실행
if person_image and clothes_image:
    st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요...")

    person_b64 = to_base64(person_image)
    clothes_b64 = to_base64(clothes_image)

    # Replicate API 호출
    try:
        output_url = replicate.run(
            "lucataco/fashion-tryon:4e47cf45d68f9d4d92f65a3e53b6120fd8d3b6b48bdf567b570a3c2e33dcb5b0",
            input={
                "image": person_b64,
                "cloth": clothes_b64
            }
        )

        # 결과 이미지 출력
        st.subheader("🧵 합성 결과")
        st.image(output_url, caption="AI가 입혀준 스타일", use_container_width=True)

        st.markdown(f"[📥 결과 이미지 다운로드]({output_url})")

    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
else:
    st.warning("고객 전신 사진과 옷 이미지를 모두 업로드해주세요.")
