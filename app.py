import streamlit as st
from PIL import Image
import io
import requests
import os
import replicate  # replicate 라이브러리 설치 필요: pip install replicate

# ✅ 환경변수로부터 Replicate API 키 불러오기
replicate_token = os.getenv("REPLICATE_API_TOKEN")
client = replicate.Client(api_token=replicate_token)

# ✅ Replicate 업로드 함수 정의 (이게 질문하신 전체 함수입니다!)
def upload_to_replicate_cdn(image_file):
    try:
        response = requests.post(
            "https://dreambooth-api-experimental.replicate.com/v1/upload",
            headers={"Authorization": f"Token {replicate_token}"},
            files={"file": image_file},
        )
        if response.status_code == 200:
            result = response.json()
            if "url" in result:
                return result["url"]
            else:
                st.error("응답에 'url'이 없습니다. 응답 내용: " + str(result))
                st.stop()
        else:
            st.error(f"업로드 실패 - 상태 코드: {response.status_code}")
            st.text(response.text)
            st.stop()
    except Exception as e:
        st.error(f"예외 발생: {e}")
        st.stop()

# ✅ Streamlit UI 시작
st.title("👗 거울아, AI로 옷 입혀줘")

person_image = st.file_uploader("고객 전신 사진 업로드", type=["jpg", "jpeg", "png"], key="person")
clothes_image = st.file_uploader("입혀볼 옷 사진 업로드", type=["jpg", "jpeg", "png"], key="clothes")

if person_image and clothes_image:
    st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요...")

    # ✅ CDN에 이미지 업로드
    person_url = upload_to_replicate_cdn(person_image)
    clothes_url = upload_to_replicate_cdn(clothes_image)

    # ✅ 모델 실행
    output = client.run(
        "cuuupid/idm-vton:0513734a452173b8173e907e3a59d19a36266e55b48528559432bd21c7d7e85",
        input={
            "garment_img": clothes_url,
            "human_img": person_url,
            "garment_des": "AI Fashion Try-On"
        }
    )

    # ✅ 결과 출력
    st.image(output, caption="👗 AI가 입힌 옷", use_column_width=True)
else:
    st.warning("고객 전신 사진과 옷 이미지를 모두 업로드해주세요.")
