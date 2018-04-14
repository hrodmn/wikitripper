import sqlite3
import pandas as pd

import urllib
import gzip

# download the table
urllib.urlretrieve ('https://dumps.wikimedia.org/other/clickstream/2018-02/clickstream-enwiki-2018-02.tsv.gz',
    '/tmp/clickstream-2018-02.tsv.gz')

# column names
dfNames = ['prev', 'curr', 'type', 'n']

# read in the table
df = pd.read_csv('/tmp/clickstream-2018-02.tsv.gz',
                compression='gzip',
                sep='\t',
                names = dfNames,
                encoding = 'utf-8')

# write to mysql database
connection = sqlite3.connect('clickstream.db')
connection.text_factory = str
df.to_sql('feb2018', connection, if_exists = 'replace')

df.iloc[0:2]
