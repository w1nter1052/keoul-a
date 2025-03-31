import streamlit as st
import replicate
import base64
import os
from PIL import Image
import io

# ✅ 1. Replicate API 토큰 가져오기
replicate_token = os.getenv("REPLICATE_API_TOKEN")
if replicate_token is None:
    st.error("❌ Replicate API 토큰이 설정되지 않았습니다. Secrets에 REPLICATE_API_TOKEN을 입력해주세요.")
    st.stop()
else:
    replicate.Client(api_token=replicate_token)

# ✅ 2. 타이틀
st.title("👗 거울아, AI로 옷 입혀줘")

# ✅ 3. 이미지 업로드
person_image = st.file_uploader("고객 전신 사진 업로드", type=["jpg", "jpeg", "png"], key="person")
clothes_image = st.file_uploader("입혀볼 옷 사진 업로드", type=["jpg", "jpeg", "png"], key="clothes")

# ✅ 4. 이미지 업로드 확인
if person_image and clothes_image:
    st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요...")

    # 파일을 base64로 인코딩
    def to_base64(image_file):
        return base64.b64encode(image_file.read()).decode("utf-8")

    person_b64 = to_base64(person_image)
    clothes_b64 = to_base64(clothes_image)

    try:
        # ✅ 5. Replicate 모델 호출 (정확한 버전 ID 포함)
        output_url = replicate.run(
            "cuuupid/idm-vton:9b6f6d79a420fcfe0354c65fb5955c049d6608b1d23c3b6015ac44c5f2a79d06",
            input={
                "image": person_b64,
                "cloth": clothes_b64
            }
        )

        # ✅ 6. 결과 출력
        st.subheader("🧵 합성 결과")
        st.image(output_url, caption="AI가 입혀준 옷", use_column_width=True)

    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")

else:
    st.warning("고객 전신 사진과 옷 이미지를 모두 업로드해주세요.")
