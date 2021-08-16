
import requests
import os
import time
import sys
import calendar
import json
from twitter import *
from dotenv import load_dotenv

bears_contract_address="0x4923017F3B7fAC4e096b46e401c0662F0B7E393f"
last_polled=0

# Load env vars from .env
load_dotenv()
auth_token = os.getenv('auth_token')
auth_secret = os.getenv('auth_secret')
consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')

def get_recent_sales(occured_after=None):
    url = "https://collections.rarity.tools/static/collections.json"
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        response_json = response.json()

        for collection in response_json['collections']:
            if collection['id'] == "buzzedbears":
                one_day_volume = collection['id']['stats']['one_day_volume']
                ...
                ...
                ...
                
                break
           
    else:
        print("Non 200 response from Opensea api: ", response.status_code)

# def post_tweet(token_id, amount, currency, usd_amount, opensea_link):
#     t = Twitter(auth=OAuth(auth_token, auth_secret, consumer_key, consumer_secret))
#     t.statuses.update(status=f"Buzzed Bear #{token_id} just sold for {amount} {currency} (${usd_amount} USD) {opensea_link}")

try:
    while True:
        if last_polled==0:
            last_polled=calendar.timegm(time.gmtime())
        
        get_recent_sales(last_polled)
        
        # set last polled time
        last_polled = calendar.timegm(time.gmtime())
        print("last polled: ", last_polled)

        # sleep for 15 minutes before polling again
        time.sleep(900)
except KeyboardInterrupt:
    print("Quitting the program.")
except:
    print("Unexpected error: ", sys.exc_info()[0])
    raise       