st로 스트림된 가져오기
PIL 가져오기 이미지에서

st.set_page_config(페이지_title="거울아", 레이아웃="중심")

st.title("👗 거울아 - AI 스타일 피팅 체험")
st.write("고객 전신 사진과 옷 사진을 업로드하면, 입혀본 모습을 보여주는 실험 앱입니다.")

# 사용자 이미지 업로드
성 header("1. 전신 사진을 업로드하세요")
person_image = st.file_uploader ("전신 사진 업로드", type=["png", "jpg", "jpeg"], key="person")

# 옷 이미지 업로드
성 header("2. 입혀볼 옷 사진을 업로드하세요")
cloth_image = st.file_uploader ("옷 사진 업로드", type=["png", "jpg", "jpeg", key="cloth")

# 이미지 표시
만약 person_image와 cloth_image:
 col1, col2 = st. columns(2)
 col1과 함께:
 세인트 서브헤더 ("👤 원본 전신 사진")
 st.image(Image.open(사람_이미지), 사용_column_width=True)
 col2와 함께:
 세인트 서브헤더 ("👗 입혀볼 옷 이미지")
 st.image(Image.open(천_이미지), 사용_column_width=True)
    
 st.success("✨ AI 스타일 입히기는 개발 중입니다.\n\n현재는 이미지 확인까지만 지원합니다.")
그렇지 않으면:
 st.info("👆 위 두 이미지를 모두 업로드하면 결과를 확인할 수 있어요.")
