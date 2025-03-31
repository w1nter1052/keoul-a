import streamlit as st
from PIL import Image

st.title("🪞 거울아, 옷 입혀줘")

person_image = st.file_uploader("전신 사진 업로드", type=["png", "jpg", "jpeg"], key="person")
clothes_image = st.file_uploader("입혀볼 옷 사진 업로드", type=["png", "jpg", "jpeg"], key="clothes")

if person_image and clothes_image:
    col1, col2 = st.columns(2)
    with col1:
        st.image(person_image, caption="고객 전신 사진", use_column_width=True)
    with col2:
        st.image(clothes_image, caption="입혀볼 옷 사진", use_column_width=True)

    st.info("※ 현재는 실제 합성 기능 없이 이미지만 나란히 보여줍니다.")
else:
    st.warning("전신 사진과 옷 사진을 모두 업로드해주세요.")

from PIL import Image
import io

# 이미지 둘 다 업로드된 경우 실행
if person_image is not None and clothes_image is not None:
    person = Image.open(person_image).convert("RGBA")
    clothes = Image.open(clothes_image).convert("RGBA")

    # 옷 이미지 사이즈 줄이기 (사람 사진 너비 기준)
    new_width = int(person.width * 0.6)
    aspect_ratio = clothes.height / clothes.width
    new_height = int(new_width * aspect_ratio)
    clothes_resized = clothes.resize((new_width, new_height))

    # 옷 위치 설정 (중앙 상단 위치)
    x = (person.width - clothes_resized.width) // 2
    y = int(person.height * 0.25)  # 대충 상체 위치

    # 합성
    result = person.copy()
    result.paste(clothes_resized, (x, y), clothes_resized)

    # 결과 출력
    st.subheader("🧵 합성 결과")
    st.image(result, caption="입혀본 모습", use_container_width=True)

    # 다운로드 버튼
    img_bytes = io.BytesIO()
    result.save(img_bytes, format="PNG")
    st.download_button("📥 결과 이미지 다운로드", data=img_bytes.getvalue(), file_name="result.png", mime="image/png")

import replicate
import requests
import streamlit as st
from PIL import Image
import io

# Replicate API Key 불러오기
replicate_token = os.getenv("REPLICATE_API_TOKEN")
replicate.Client(api_token=replicate_token)

# 이미지 파일 업로드
st.title("👗 거울아, AI로 옷 입혀줘")

person_image = st.file_uploader("고객 전신 사진 업로드", type=["jpg", "jpeg", "png"], key="person")
clothes_image = st.file_uploader("입혀볼 옷 사진 업로드", type=["jpg", "jpeg", "png"], key="clothes")

if person_image and clothes_image:
    st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요...")

    # 이미지 byte로 변환
    def to_base64(image_file):
        return base64.b64encode(image_file.read()).decode("utf-8")

    person_b64 = to_base64(person_image)
    clothes_b64 = to_base64(clothes_image)

    # Replicate API 호출
    output_url = replicate.run(
        "lucataco/fashion-tryon:4e47cf45d68f9d4d92f65a3e53b6120fd8d3b6b48bdf567b570a3c2e33dcb5b0",
        input={
            "image": person_b64,
            "cloth": clothes_b64
        }
    )

    # 결과 이미지 출력
    st.image(output_url, caption="👗 합성된 스타일", use_column_width=True)
else:
    st.warning("고객 전신 사진과 옷 이미지를 모두 업로드해주세요.")
