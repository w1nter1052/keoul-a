import streamlit as st
from PIL import Image
import requests
import replicate
import os

# 🌟 환경 변수에서 Replicate API 토큰 가져오기
replicate_token = os.getenv("REPLICATE_API_TOKEN")
client = replicate.Client(api_token=replicate_token)

# ✅ Replicate CDN 업로드 함수 정의
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
                st.error("응답에 'url' 키가 없습니다.")
                st.stop()
        else:
            st.error(f"CDN 업로드 실패 (상태 코드: {response.status_code})")
            st.text(response.text)
            st.stop()
    except Exception as e:
        st.error(f"CDN 업로드 중 예외 발생: {e}")
        st.stop()

# ✅ Streamlit 앱 UI
st.set_page_config(page_title="거울아, AI로 옷 입혀줘", page_icon="👗")
st.title("👗 거울아, AI로 옷 입혀줘")

# 이미지 업로드
person_image = st.file_uploader("고객 전신 사진 업로드", type=["jpg", "jpeg", "png"], key="person")
clothes_image = st.file_uploader("입혀볼 옷 사진 업로드", type=["jpg", "jpeg", "png"], key="clothes")

# 이미지가 모두 업로드된 경우
if person_image and clothes_image:
    st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요...")

    # Replicate CDN으로 이미지 업로드
    person_url = upload_to_replicate_cdn(person_image)
    clothes_url = upload_to_replicate_cdn(clothes_image)

    # 모델 실행
    try:
        output = client.run(
            "cuuupid/idm-vton:0513734a452173b8173e907e3a59d19a36266e55b48528559432bd21c7d7e85",
            input={
                "garment_img": clothes_url,
                "human_img": person_url,
                "garment_des": "cute pink top"
            }
        )
        st.image(output, caption="🧵 AI가 입혀본 스타일", use_column_width=True)
    except Exception as e:
        st.error(f"모델 실행 중 오류 발생: {e}")
else:
    st.warning("고객 전신 사진과 옷 이미지를 모두 업로드해주세요.")
