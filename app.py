import os
import replicate

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
replicate.Client(api_token=REPLICATE_API_TOKEN)
