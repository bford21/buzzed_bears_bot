import requests
import time
import os
from bs4 import BeautifulSoup
from twitter import *
from dotenv import load_dotenv


# Load env vars from .env
load_dotenv()
auth_token = os.getenv('auth_token')
auth_secret = os.getenv('auth_secret')
consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')

def post_tweet(unique_owners, floor_price, ninety_day_volume):
    t = Twitter(auth=OAuth(auth_token, auth_secret, consumer_key, consumer_secret))
    # TODO Figure out handling of newline characters
    # t.statuses.update(status=f"Daily Buzzed Bears Checkup 🩺 \n\")

url = 'https://opensea.io/collection/buzzedbears'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
h3_tags = soup.find_all('h3')
text=[]
for item in h3_tags:
    text.append(item.text.strip())

# Soft check here on number of h3 tags on page. If opensea changes site html we wont post
# Probably need a better safety net here
if len(text)==4:
    unique_owners = text[1]
    floor_price = text[2]
    ninety_day_volume = text[3]

    print("Holders", unique_owners)
    print("Floor", floor_price)
    print("90 Day ETH Volume", ninety_day_volume)

