import io
import replicate

# 📌 Streamlit 페이지 제목
st.set_page_config(page_title="거울아, AI로 옷 입혀줘 👗")
st.title("👗 거울아, AI로 옷 입혀줘")

# 📌 파일 업로드 받기
person_image = st.file_uploader("고객 전신 사진 업로드", type=["jpg", "jpeg", "png"])
clothes_image = st.file_uploader("입혀볼 옷 사진 업로드", type=["jpg", "jpeg", "png"])

# ✅ Replicate CDN에 이미지 업로드하는 함수
def upload_to_replicate_cdn(image_file):
    upload_init_url = "https://dreambooth-api-experimental.replicate.com/v1/upload"

    headers = {
        "Authorization": f"Token {os.getenv('REPLICATE_API_TOKEN')}",
        "Content-Type": "application/json",
    }

    init_response = requests.post(
        upload_init_url,
        headers=headers,
        json={"filename": image_file.name}
    )

    if init_response.status_code != 200:
        st.error(f"CDN 업로드 실패 (상태 코드: {init_response.status_code})\n\n{init_response.text}")
        return None

    upload_data = init_response.json()
    upload_url = upload_data["upload_url"]
    final_url = upload_data["final_url"]

    # 이미지 실제 업로드 (PUT)
    put_response = requests.put(
        upload_url,
        data=image_file.getvalue(),
        headers={"Content-Type": "application/octet-stream"}
    )

    if put_response.status_code != 200:
        st.error(f"이미지 전송 실패 (상태 코드: {put_response.status_code})")
        return None

    return final_url

# ✅ 실제 실행
if person_image and clothes_image:
    st.info("AI가 옷을 입히는 중입니다. 잠시만 기다려주세요...")

    person_url = upload_to_replicate_cdn(person_image)
    clothes_url = upload_to_replicate_cdn(clothes_image)

    if person_url and clothes_url:
        try:
            # Replicate 실행
            output = replicate.run(
                "cuuupid/idm-vton",
                input={
                    "human_img": person_url,
                    "garment_img": clothes_url,
                    "garment_des": "any clothing"
                }
            )

            st.image(output, caption="👗 합성된 이미지", use_column_width=True)
            st.success("완료! 아래 이미지를 확인하세요.")
        except Exception as e:
            st.error(f"AI 처리 중 오류 발생: {e}")
else:
    st.warning("고객 전신 사진과 옷 이미지를 모두 업로드해주세요.")
