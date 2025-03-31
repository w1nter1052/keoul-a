human_url = "https://replicate.delivery/mgxm/9d067505-728f-4cf5-987c-4e10be1c0036/human.jpg"
garment_url = "https://replicate.delivery/mgxm/427b9a2a-44ff-4b4c-9b1e-7ce8b0a80449/garment.jpg"

output = replicate.run(
    "cuuupid/idm-vton:latest",
    input={
        "human_img": human_url,
        "garment_img": garment_url,
        "garment_type": "upper_body"
    }
)
