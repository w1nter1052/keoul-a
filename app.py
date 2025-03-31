import streamlit as st
import replicate
import requests

# 환경변수 설정
REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

# Replicate에 이미지 업로드
def upload_to_replicate_cdn(image_file):
    response = requests.post(
        "https://dreambooth-api-experimental.replicate.delivery/upload",
        files={"file": image_file}
    )
    response.raise_for_status()
    return response.json()["url"]

# Streamlit UI
st.set_page_config(page_title="겨울아, AI로 옷 입혀줘 👗")
st.title("👗 겨울아, AI로 옷 입혀줘")

st.markdown("**고객 전신 사진 업로드**")
person_image = st.file_uploader("여기에서 파일 드래그 앤 드롭", type=["jpg", "jpeg", "png"])

st.markdown("**입혀볼 옷 사진 업로드**")
garment_image = st.file_uploader("여기에서 파일 드래그 앤 드롭", type=["jpg", "jpeg", "png"])

if person_image and garment_image:
    with st.spinner("AI가 옷을 입히는 중입니다... 잠시만 기다려주세요."):

        try:
            # 업로드
            person_url = upload_to_replicate_cdn(person_image)
            garment_url = upload_to_replicate_cdn(garment_image)

            # 모델 실행 (cuuupid/idm-vton 무료 모델)
            output = replicate_client.run(
                "cuuupid/idm-vton:0513734a452173b8173e907e3a59d19a36266e55b48528559432bd21c7d7e985",
                input={
                    "human_img": person_url,
                    "garment_img": garment_url
                }
            )

            st.success("완료되었습니다!")
            st.image(output, caption="AI가 생성한 결과")

        except Exception as e:
            st.error(f"오류 발생: {str(e)}")

else:
    st.info("고객 전신 사진과 옷 이미지를 모두 업로드해주세요.")
