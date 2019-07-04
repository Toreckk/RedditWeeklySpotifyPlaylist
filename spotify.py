import requests
import json
import base64

# Client Keys
with open('./config.json') as f:
    tokens = json.loads(f.read())

CLIENT_ID = tokens['CLIENT_ID']
CLIENT_SECRET = tokens['CLIENT_SECRET']

print('Client ID: {}'.format(CLIENT_ID))
print('Client Secret: {}'.format(CLIENT_SECRET))

#Spotify Base URLs
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"
