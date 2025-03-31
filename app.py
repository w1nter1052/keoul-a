st로 스트림된 가져오기
PIL 가져오기 이미지에서

st.title("🪞 거울아, 옷 입혀줘")

person_image = st.file_uploader ("전신 사진 업로드", type=["png", "jpg", "jpeg", key="person")
clothes_image = st.file_uploader ("입혀볼 옷 사진 업로드", type=["png", "jpg", "jpeg", key="clothes")

만약 사람_이미지와 옷_이미지:
 col1, col2 = st. columns(2)
 col1과 함께:
 st.image(person_image, 캡션="고객 전신 사진", use_column_width=True)
 col2와 함께:
 st.image(clothes_image, 캡션="입혀볼 옷 사진", 사용_column_width=True)

 st.info("※ 현재는 실제 합성 기능 없이 이미지만 나란히 보여줍니다.")
그렇지 않으면:
 st.warning("전신 사진과 옷 사진을 모두 업로드해주세요.")
