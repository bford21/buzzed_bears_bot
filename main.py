
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
    url = "https://api.opensea.io/api/v1/events"
    querystring = {"asset_contract_address":bears_contract_address,"event_type":"successful","only_opensea":"false","offset":"0","limit":"100","occurred_after":occured_after}
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.status_code == 200:
        response_json = response.json()

        for new_sale in response_json['asset_events']:
            if new_sale['asset'] is not None:
                token_id = new_sale['asset']['token_id']
                opensea_link = new_sale['asset']['permalink']
                currency = new_sale['payment_token']['symbol']
                decimals = new_sale['payment_token']['decimals']
                usd_price = float(new_sale['payment_token']['usd_price'])
                amount = float(new_sale['total_price']) / 10**decimals
                usd_amount = round(usd_price * amount, 2)
                print(f"Buzzed Bear #{token_id} just sold for {amount} {currency} (${usd_amount} USD) {opensea_link}")
                post_tweet(token_id, amount, currency, usd_amount, opensea_link)
            else:
                print("Error asset is None", new_sale)
    else:
        print("Non 200 response from Opensea api: ", response.status_code)

def post_tweet(token_id, amount, currency, usd_amount, opensea_link):
    t = Twitter(auth=OAuth(auth_token, auth_secret, consumer_key, consumer_secret))
    t.statuses.update(status=f"Buzzed Bear #{token_id} just sold for {amount} {currency} (${usd_amount} USD) {opensea_link}")

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