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
