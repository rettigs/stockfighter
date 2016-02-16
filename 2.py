#!/usr/bin/env python

import json
import requests
import sys
import time

venue = "IGWEX"
symbol = "HUN"
quoteurl = "https://api.stockfighter.io/ob/api/venues/{}/stocks/{}/quote".format(venue, symbol)
orderurl = "https://api.stockfighter.io/ob/api/venues/{}/stocks/{}/orders".format(venue, symbol)
headers = {"X-Starfighter-Authorization": sys.argv[1]}
total_shares = 0
target_shares = 100000
order_size = 1000
target_price = 8867
while total_shares < target_shares:
    data = {
        "orderType": "limit",
        "qty": order_size,
        "price": target_price,
        "direction": "buy",
        "account": "KAH40503416"
    }
    r = requests.post(orderurl, data=json.dumps(data), headers=headers)
    j = r.json()
    print "totalFilled: {}".format(j['totalFilled'])
    while j['totalFilled'] < order_size:
        print "Only {}/{} of order {} has been filled; keep waiting".format(j['totalFilled'], order_size, j['id'])
        time.sleep(3)
        j = requests.get("{}/{}".format(orderurl, j['id']), headers=headers).json()
    total_shares += j['totalFilled']
    time.sleep(0.1)
    print "total shares: {}/{}".format(total_shares, target_shares)
