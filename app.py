import streamlit as st
from PIL import Image
import base64
import requests
import io
import os

# 페이지 설정
st.set_page_config(page_title="거울아, AI로 옷 입혀줘 🧵")

# 제목
st.title("👗 거울아, AI로 옷 입혀줘")

# 파일 업로드
person_image = st.file_uploader("고객 전신 사진 업로드", type=["jpg", "jpeg", "png"], key="person")
clothes_image = st.file_uploader("입혀볼 옷 사진 업로드", type=["jpg", "jpeg", "png"], key="clothes")

# 업로드한 이미지를 좌우로 나란히 보여줌
if person_image and clothes_image:
    col1, col2 = st.columns(2)
    with col1:
        st.image(person_image, caption="👤 고객 전신", use_column_width=True)
    with col2:
        st.image(clothes_image, caption="👗 입혀볼 옷", use_column_width=True)

    st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요...")

    # CDN에 업로드하는 함수
    def upload_to_replicate_cdn(file):
        api_url = "https://dreambooth-api-experimental.replicate.com/v1/upload"
        headers = {"Authorization": f"Token {os.getenv('REPLICATE_API_TOKEN')}"}
        response = requests.post(api_url, headers=headers, files={"file": file})
        if response.status_code == 200:
            return response.json()["url"]
        else:
            st.error(f"CDN 업로드 실패 (상태 코드: {response.status_code})")
            st.code(response.text, language="html")
            return None

    # 이미지 업로드
    person_url = upload_to_replicate_cdn(person_image)
    clothes_url = upload_to_replicate_cdn(clothes_image)

    # 이미지가 정상적으로 업로드되었을 때만 실행
    if person_url and clothes_url:
        # API 호출
        replicate_url = "https://api.replicate.com/v1/predictions"
        headers = {
            "Authorization": f"Token {os.getenv('REPLICATE_API_TOKEN')}",
            "Content-Type": "application/json"
        }
        payload = {
            "version": "0513734a452173b8173e907e3a59d19a36266e55b48528559432bd21c7d7e985",
            "input": {
                "garment_img": clothes_url,
                "human_img": person_url,
                "garment_des": "nice outfit"
            }
        }

        response = requests.post(replicate_url, json=payload, headers=headers)

        if response.status_code == 201:
            prediction = response.json()
            prediction_url = prediction["urls"]["get"]

            # 결과 기다리기
            status = prediction["status"]
            with st.spinner("AI 결과 생성 중..."):
                while status != "succeeded" and status != "failed":
                    result_response = requests.get(prediction_url, headers=headers)
                    result = result_response.json()
                    status = result["status"]

            if status == "succeeded":
                result_image = result["output"]
                st.subheader("🪞 AI가 입힌 결과")
                st.image(result_image, caption="✨ 완성된 스타일", use_column_width=True)
            else:
                st.error("AI가 옷 입히기에 실패했습니다.")
        else:
            st.error(f"API 요청 실패: {response.status_code}")
            st.code(response.text, language="json")

else:
    st.warning("고객 전신 사진과 옷 이미지를 모두 업로드해주세요.")
