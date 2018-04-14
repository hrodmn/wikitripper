from wikipedia import *
import requests
import json
import sqlite3
import pandas as pd


CONNECTION = sqlite3.connect('clickstream.db')

class wikitrip:
    def __init__(self, lon, lat):
        self.lon = lon
        self.lat = lat
    
    def search(self):
        all_results = wikipedia.geosearch(
            latitude=self.lat,
            longitude=self.lon,
            title=None,
            results=100,
            radius=10000,
            table=True
        )
        all_results['curr'] = all_results['title'].str.replace(' ', '_')
        self.results = all_results
    
    def clickstream(self):
        rez = [str(x.encode('ascii', 'ignore')).replace(' ', '_') for x in list(self.results['title'])]
        sql = """select * from feb2018 where curr in ({1})"""
        sql = sql.format('?', ','.join('?' * len(rez)))
        
        clickstream_results = pd.read_sql_query(sql = sql,
                                con = CONNECTION,
                                params = tuple(rez))

        sorted_results = clickstream_results[['curr', 'n']].groupby(['curr'], as_index=False).sum().sort_values('n', ascending=False)
        self.stream = pd.merge(sorted_results, self.results, on='curr', how='inner')
