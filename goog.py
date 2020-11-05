import requests
import sys
import json

# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

# API Key. Switch to dot env...
KEY="CHANGEME"

# Query
query = sys.argv[1]
mquery = query.replace(' ', '+')
URL = f"https://api.goog.io/v1/search/q={mquery}&num=100"

headers = {
    "user-agent": USER_AGENT,
    "apikey": KEY }

resp = requests.get(URL, headers=headers)
ansr = json.loads(resp.content)

for item in ansr['results']:
    print(item.get('link'))
