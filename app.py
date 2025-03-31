import replicate
import streamlit as st

# Replicate API Token은 환경변수(REPLICATE_API_TOKEN)로 설정되어 있어야 함
# 예: .streamlit/secrets.toml 파일에 추가하거나 환경에서 설정

st.set_page_config(page_title="사람 이미지와 옷 이미지로 AI 패션 테스트", page_icon="🧍‍♀️👗")
st.title("🧍‍♀️ 사람 이미지와 👗 옷 이미지로 AI 패션 테스트")

# Replicate 공식 테스트 이미지 URL 사용
human_url = "https://replicate.delivery/mgxm/9d067505-728f-4cf5-987c-4e10be1c0036/human.jpg"
garment_url = "https://replicate.delivery/mgxm/427b9a2a-44ff-4b4c-9b1e-7ce8b0a08449/garment.jpg"

st.image(human_url, caption="사람 이미지", width=300)
st.image(garment_url, caption="입힐 옷 이미지", width=300)

if st.button("AI가 옷을 입혀줘!"):
    st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요...")

    try:
        output = replicate.run(
            "cuuupid/idm-vton:latest",
            input={
                "human_img": human_url,
                "garment_img": garment_url,
                "garment_type": "upper_body"
            }
        )
        st.image(output, caption="AI가 입힌 결과", use_column_width=True)
    except Exception as e:
        st.error("❌ 오류 발생: AI 실행에 실패했습니다.")
        st.exception(e)
