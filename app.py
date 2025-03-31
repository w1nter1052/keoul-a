import streamlit as st
import replicate
import requests

# 페이지 설정
st.set_page_config(page_title="겨울아, AI로 옷 입혀줘 👗")

st.title("👗 겨울아, AI로 옷 입혀줘")

# 사용자 입력 - 전신 이미지
person_image = st.file_uploader("고객 전신 사진 업로드", type=["jpg", "jpeg", "png"], key="person")

# 사용자 입력 - 옷 이미지
garment_image = st.file_uploader("입혀볼 옷 사진 업로드", type=["jpg", "jpeg", "png"], key="garment")

# 업로드한 파일을 Replicate 서버에 올리는 함수
def upload_to_replicate_cdn(uploaded_file):
    if uploaded_file is None:
        return None
    files = {'file': uploaded_file.getvalue()}
    response = requests.post("https://dreambooth-api-experimental.replicate.com/v1/upload", files=files)
    if response.status_code == 200:
        return response.json()["url"]
    else:
        st.error(f"CDN 업로드 실패 (상태 코드: {response.status_code})")
        st.code(response.text, language="html")
        return None

# 실행 버튼
if st.button("AI가 옷을 입혀줘!"):
    if person_image and garment_image:
        with st.spinner("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요…"):

            # Replicate에 파일 업로드
            person_url = upload_to_replicate_cdn(person_image)
            garment_url = upload_to_replicate_cdn(garment_image)

            if person_url is None or garment_url is None:
                st.error("이미지 업로드 중 문제가 발생했습니다.")
            else:
                try:
                    # Replicate API 실행
                    output = replicate.run(
                        "wolverinn/ecommerce-virtual-try-on:dc3a7b00c21a38d83a14e95954e52edb0aa4c3f3a51e42355c7ff9ad81c97319",
                        input={
                            "image": person_url,
                            "cloth": garment_url
                        }
                    )

                    # 결과 출력
                    st.success("결과 이미지입니다!")
                    st.image(output["image"], caption="AI가 입힌 옷 결과", use_column_width=True)

                except Exception as e:
                    st.error("AI 처리 중 오류가 발생했습니다.")
                    st.exception(e)
    else:
        st.warning("전신 사진과 옷 이미지를 모두 업로드해주세요.")
