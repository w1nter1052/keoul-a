import replicate
import os

# Replicate API 키 세팅
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
replicate = replicate.Client(api_token=REPLICATE_API_TOKEN)

# 테스트용 이미지 URL
human_url = "https://replicate.delivery/mgxm/9d067505-728f-4cf5-987c-4e10be1c0036/human.jpg"
garment_url = "https://replicate.delivery/mgxm/427b9a2a-44ff-4b4c-9b1e-7ce8b0a80449/garment.jpg"

# 실행
output = replicate.run(
    "cuuupid/idm-vton:latest",
    input={
        "human_img": human_url,
        "garment_img": garment_url,
        "garment_type": "upper_body"
    }
)

print("결과 이미지:", output)
