import requests
import os

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
headers = {
    "Authorization": f"Token {REPLICATE_API_TOKEN}"
}

person_url = "https://i.imgur.com/9d067505.jpg"
garment_url = "https://i.imgur.com/427b9a2.jpg"

url = "https://api.replicate.com/v1/predictions"
data = {
    "version": "cuuupid/idm-vton:latest",
    "input": {
        "human_img": person_url,
        "garment_img": garment_url,
        "garment_type": "upper_body"
    }
}

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.status_code, response.text)
