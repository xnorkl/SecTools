import requests
import re
import sys
from pprint import pprint

'''Simple CLI tool for securityheaders.com'''
# TODO:Rework formatting and Regex. Regex should output matches to a dictionary."

# Rudimentary Argument Parsing
pre = str('https://securityheaders.com/?q=')
arg = str(sys.argv[1])
suf = str('&followRedirects=on')

# Payload
r = requests.get(pre + arg + suf)

# Regex
rx_grade = re.findall(r"(?<=grade )\w+", r.text)
html_tags = re.compile(r"<(?!meta)[^>]*>")      # Negative Look-Around for Non Meta tags
meta_tags = re.compile(r"<meta\s\w+\-?\w+=(.*)\scontent=(.*)\s/>")      # Capture meta content
multi_space = re.compile(r"\s\s+")      # Simple multi-space regex

# Removing regex matches
clean = html_tags.sub(" ", r.text)
clean = meta_tags.sub("\\1\\t\\2", clean)
clean = multi_space.sub("\n", clean)

for e in clean.split('\n')[29:-10]:
    print(e)
