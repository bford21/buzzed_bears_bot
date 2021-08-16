import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
    t.statuses.update(status=f"""
🐻 🩺 Daily Buzzed Bears Checkup 🩺 🐻 \n
💎 Number of bear holders: {unique_owners}
💰 Floor Price: {floor_price}
📊 Ninety Day Volume {ninety_day_volume} ETH
""")

DRIVER_PATH = './chromedriver'

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get('https://opensea.io/collection/buzzedbears')

text = []
for el in driver.find_elements_by_tag_name('h3'):
    text.append(el.text)

if len(text)==4:
    unique_owners = text[1]
    floor_price = text[2]
    ninety_day_volume = text[3]

    print("Holders", unique_owners)
    print("Floor", floor_price)
    print("90 Day ETH Volume", ninety_day_volume)

    post_tweet(unique_owners, floor_price, ninety_day_volume)
else:
    print("Length of h3 tags array not equal to 4!")

driver.quit()