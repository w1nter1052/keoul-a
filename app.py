st로 스트림된 가져오기
가져오기 복제본
가져오기 요청

# 환경변수 설정
복제_API_토큰 = st. secrets["복제_API_토큰"]
replicate_container = replicate.클라이언트(api_token=replicate_API)_토큰)

# Replicate에 이미지 업로드
def upload_to_replicate_cdn(image_file):
 응답 = requests.post (
 "https://dreambooth-api-실험적.replicate.배송/upload",
 files={"file": image_file}
    )
 응답.raise_for_status ()
 응답 반환.json ()["url"]

# 스트림릿 UI
st.set_page_config(페이지_title="겨울아, AI 로 옷 입혀줘 👗")
st.title("👗 겨울아, AI로 옷 입혀줘")

st.markdown("**고객 전신 사진 업로드**")
person_image = st.file_uploader ("여기에서 파일 드래그 앤 드롭", type=["jpg", "jpeg", "png"])

st.markdown("**입혀볼 옷 사진 업로드**")
가먼트_이미지 = st.file_uploader ("여기에서 파일 드래그 앤 드롭", type=["jpg", "jpeg", "png"])

만약 사람_이미지와 의복_이미지:
 세인트 스피너 (" 사용AI가 옷을 입히는 중입니다... 잠시만 기다려주세요."):

 시도:
            # 업로드
 person_url = 업로드_to_replicate_cdn(person_image)
 의류_url = 업로드_to_replicate_cdn(garment_이미지)

            # 모델 실행 (cuuupid/idm-vton 무료 모델)
 출력 = replicate_c라이언트.run(
 "cuuupid/idm-vton:0513734a452173b8173e907e3a59d19a36266e55b48528559432bd21c7d7e985",
 입력={
 "human_img": person_url,
 "garment_img": 의류_url
                }
            )

 st.success("완료되었습니다!")
 st.image(출력, 캡션="AI가 생성한 결과")

 예외: e:
 st.error(f"오류 발생: {str(e)}")

그렇지 않으면:
 st.info("고객 전신 사진과 옷 이미지를 모두 업로드해주세요.")
