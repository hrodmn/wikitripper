from wikipedia import *
import requests
import json
import sqlite3
import pandas as pd
import numpy as np

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
            results=10,
            radius=10000,
            table=True
        )
        all_results['curr'] = all_results['title'].str.replace(' ', '_')
        self.results = all_results
    
    def stream_table(self):
        rez = [str(x.encode('ascii', 'ignore')).replace(' ', '_') for x in list(self.results['title'])]
        sql = """select * from feb2018 where curr in ({1})"""
        sql = sql.format('?', ','.join('?' * len(rez)))
        
        self.stream_query = pd.read_sql_query(sql = sql,
                                con = CONNECTION,
                                params = tuple(rez))
    
    def local_stream(self):
        sorted_stream = self.stream_query[['curr', 'n']].groupby(['curr'], as_index=False).sum().sort_values('n', ascending=False)
        stream_table = pd.merge(sorted_stream, self.results, on='curr', how='inner')
        
        # order articles weighted by popularity and distance
        pop_score = np.sqrt(stream_table['n'] / np.mean(stream_table['n']))

        dist_score = stream_table['dist'] / min(stream_table['dist'])
        
        stream_table['weight'] = 1 / pop_score * dist_score
        self.table = stream_table
        self.local_stream = list(stream_table.sort_values(by = 'weight')['title'])
    
    def summarize(self):
        titles = self.local_stream
        summaries = [wikipedia.summary(title) for title in titles]
        distances = self.table['dist']
        
        stacked = zip(titles, zip(distances, summaries))
        
        self.content = json.dumps(stacked)

        
        
