import streamlit as st
import replicate
import os
import base64

st.set_page_config(page_title="거울아, AI로 옷 입혀줘 👗")

st.title("👗 거울아, AI로 옷 입혀줘")

# Replicate API 키 가져오기
replicate_token = os.getenv("REPLICATE_API_TOKEN")
if not replicate_token:
    st.error("REPLICATE_API_TOKEN 시크릿이 설정되지 않았습니다.")
    st.stop()

client = replicate.Client(api_token=replicate_token)

# 이미지 업로드
person_image = st.file_uploader("고객 전신 사진 업로드", type=["jpg", "jpeg", "png"], key="person")
clothes_image = st.file_uploader("입혀볼 옷 사진 업로드", type=["jpg", "jpeg", "png"], key="clothes")

# 이미지 → base64
def to_base64(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

# 이미지가 업로드되었을 때
if person_image and clothes_image:
    st.info("🪄 AI가 옷을 입히는 중입니다. 잠시만 기다려주세요...")

    try:
        person_b64 = to_base64(person_image)
        clothes_b64 = to_base64(clothes_image)

        # ✅ 여기에 사용할 최신 Replicate 모델 주소를 정확히 넣어줘야 함
       output = client.run(
    "cuupid/idm-vton:27b5d9d9d8106476427cc1cf9c631dd5d9f09d39b41a4dfb3177f7b66ffefb8c",
    input={
        "human": person_b64,
        "cloth": clothes_b64
    }
)

        # 출력 결과 (URL 형식)
        if isinstance(output, str):
            st.image(output, caption="🧵 AI 합성 결과", use_column_width=True)
        else:
            st.error("이미지를 불러올 수 없습니다.")

    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")

else:
    st.warning("고객 전신 사진과 옷 이미지를 모두 업로드해주세요.")
