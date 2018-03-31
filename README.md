# wikitripper
A package that will query Wikipedia for nearby content and tell you stories about things in your area!

## Setup
Start by creating a python virtual environment, then activate the virtualenv:
```bash
cd ~/workspace/wikitripper
mkvirtualenv wikitripper
workon wikitripper
```

Install local version of Wikipedia package. This is a fork of the Wikipedia package from https://github.com/goldsmith/Wikipedia

```bash
cd ~/workspace
git clone https://github.com/hrodmn/Wikipedia.git
pip install -e ~/workspace/Wikipedia
```

Install a jupyter kernel for wikitripper:
```bash
pip install ipykernel
python -m ipykernel install --user \
 --name wikitripper \
 --display-name "Python (wikitripper)"
```

# Query by location
The first step in the wikitripper process will be to query for Wikipedia content in the area surrounding a location. We can do this by setting up a query using the Wikipedia package:
```python
import wikipedia
import requests
import json

send_url = 'http://freegeoip.net/json'
r = requests.get(send_url)
j = json.loads(r.text)
latitude = j['latitude']
longitude = j['longitude']

allResults = wikipedia.geosearch(latitude=lat,
                                     longitude=lon,
                                     title=None,
                                     results=100,
                                     radius=10000)

```

We may also want to query by content type (e.g. city, county, landmark, etc.):

```python
city_results = wikipedia.geosearch(latitude=lat,
                                     longitude=lon,
                                     title=None,
                                     results=500,
                                     radius=10000,
                                     feature_type='city')

landmark_results = wikipedia.geosearch(latitude=lat,
                                     longitude=lon,
                                     title=None,
                                     results=500,
                                     radius=10000,
                                     feature_type='landmark')
```
