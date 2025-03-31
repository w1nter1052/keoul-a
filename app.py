import streamlit as st
import replicate
import os

# API 키 설정
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

st.title("👗 AI 가상 피팅 테스트")
st.write("사람 이미지와 옷 이미지의 URL을 입력하세요.")

person_url = st.text_input("사람 이미지 URL")
clothes_url = st.text_input("입힐 옷 이미지 URL")

if person_url and clothes_url:
    st.image(person_url, caption="사람 이미지")
    st.image(clothes_url, caption="입힐 옷 이미지")
    st.write("AI가 옷을 입히는 중입니다...")

    try:
        output = replicate.run(
            "lucataco/virtual-try-on:latest",
            input={"person": person_url, "clothes": clothes_url}
        )
        st.image(output["output"], caption="AI가 입힌 결과", use_column_width=True)
    except Exception as e:
        st.error(f"AI 실행 실패: {e}")
