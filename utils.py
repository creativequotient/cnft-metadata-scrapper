from redis import Redis
import requests
import dotenv
import os

dotenv.load_dotenv('.env')

redis = Redis(
    host=os.getenv('UPSTASH_HOST'),
    port=os.getenv('UPSTASH_PORT'),
    password=os.getenv('UPSTASH_PASSWORD'),
    ssl=True
)
