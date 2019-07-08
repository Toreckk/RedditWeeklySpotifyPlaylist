import requests
import json
import base64
import urllib

with open('./config.json') as f:
    tokens = json.loads(f.read())
