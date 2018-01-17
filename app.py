from flask import Flask
from redis import Redis, RedisError
import os
import socket

import requests
import json
import wikipedia

# get a coordinate to search
send_url = 'http://freegeoip.net/json'
r = requests.get(send_url)
j = json.loads(r.text)
lat = j['latitude']
lon = j['longitude']

def print_wiki(result):
    page = wikipedia.page(result)
    page_summary = wikipedia.summary(result)
    
    html = "<h2>{title}:</h2>" \
           "<b>Summary:</b> {summary}<br/>" \

    out = html.format(title=page.title,
                      summary=page_summary)
    
    return(out)

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    city_results = wikipedia.geosearch(latitude=lat,
                                         longitude=lon,
                                         title=None,
                                         results=10,
                                         radius=10000,
                                         feature_type='city')
    
    city_wiki = map(print_wiki, city_results)
    
    city_out = ""
    for i in city_wiki:
        city_out += str(i) + " "
    
    # event_results = wikipedia.geosearch(latitude=lat,
    #                                      longitude=lon,
    #                                      title=None,
    #                                      results=30,
    #                                      radius=10000,
    #                                      feature_type='event')
    #
    # if len(event_results) > 0:
    #     try:
    #         event_wiki = map(print_wiki, event_results)
        
    # else:
    #     event_wiki = None
    event_wiki = None
    
    return city_out

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
