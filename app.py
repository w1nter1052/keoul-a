import streamlit as st
from PIL import Image
import replicate
import os
import base64
import io

# 환경변수에서 Replicate API 키 불러오기
replicate_token = os.getenv("REPLICATE_API_TOKEN")
os.environ["REPLICATE_API_TOKEN"] = replicate_token

# 제목
st.title("👗 거울아, AI로 옷 입혀줘")

# 파일 업로드
person_image = st.file_uploader("고객 전신 사진 업로드", type=["jpg", "jpeg", "png"], key="person")
clothes_image = st.file_uploader("입혀볼 옷 사진 업로드", type=["jpg", "jpeg", "png"], key="clothes")

# 둘 다 업로드된 경우
if person_image and clothes_image:
    st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요...")

    # base64 인코딩 함수
    def to_base64(uploaded_file):
        return base64.b64encode(uploaded_file.read()).decode("utf-8")

    # base64로 변환
    person_b64 = to_base64(person_image)
    clothes_b64 = to_base64(clothes_image)

    # Replicate 모델 실행
    try:
        output_url = replicate.run(
            "cuuupid/idm-vton",  # 최신 인기 Try-On 모델
            input={
                "image": person_b64,
                "cloth": clothes_b64
            }
        )

        # 결과 이미지 출력
        st.subheader("👗 합성된 스타일")
        st.image(output_url, caption="AI가 입혀본 모습", use_container_width=True)

        # 다운로드 버튼
        st.markdown(f"[📥 결과 이미지 다운로드]({output_url})")

    except Exception as e:
        st.error(f"❌ 오류 발생: {str(e)}")

else:
    st.warning("고객 전신 사진과 옷 이미지를 모두 업로드해주세요.")
