import requests
import json
import base64
import urllib

# Client Keys
with open('./config.json') as f:
    tokens = json.loads(f.read())

CLIENT_ID = tokens['SPOTIFY_CLIENT_ID']
CLIENT_SECRET = tokens['SPOTIFY_CLIENT_SECRET']
ACCESS_TOKEN = tokens['SPOTIFY_ACCESS_TOKEN']
REFRESH_TOKEN = tokens['SPOTIFY_REFRESH_TOKEN']

print('Client ID: {}'.format(CLIENT_ID))
print('Client Secret: {}'.format(CLIENT_SECRET))

#Spotify Base URLs
URL_AUTH = "https://accounts.spotify.com/authorize"
URL_TOKEN = "https://accounts.spotify.com/api/token"
BASE_URL = "https://api.spotify.com/v1"

#Request based on Client Credentials Flow from https://developer.spotify.com/web-api/authorization-guide/

#1. Have your application request authorization; the user logs in and authorizes access

# playlist-modify-public = 	Write access to a user's public playlists.
# playlist-modify-private = Write access to a user's private playlists.
REDIRECT_URI = "http://localhost:8888/callback"
STATE = ""
SCOPE = "playlist-modify-public"
SHOW_DIALOG = str(False).lower()

def req_auth_app():
    auth_params = {
        "client_id" : CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        #"state":STATE, #OPTIONAL
        "scope":SCOPE, #OPTIONAL
        "show_dialog":SHOW_DIALOG #OPTIONAL
    }
    # example GET request 
    # GET https://accounts.spotify.com/authorize?client_id=5fe01282e44241328a84e7c5cc169165&response_type=code&redirect_uri=https%3A%2F%2Fexample.com%2Fcallback&scope=user-read-private%20user-read-email&state=34fFs29kd09
    args = '&'.join('{}={}'.format(param, urllib.parse.quote(auth_params[param])) for param in auth_params)
    auth_url = "{}/?{}".format(URL_AUTH,args)
    print('Auth URL: {}'.format(auth_url))
    print('-------------------------------------')
    var = input("Please access the url above in your browser give permissions and paste the resulting URL: ")
    print('-------------------------------------')
    parsed = urllib.parse.urlparse(var)
    code = urllib.parse.parse_qs(parsed.query)['code'][0]
    print('-------------------------------------')
    return code



#2. Have your application request refresh and access tokens; Spotify returns access and refresh tokens
def usr_auth():
    if(len(ACCESS_TOKEN)<1): # If no previous token exists

        auth_code = req_auth_app()

        payload = {
            "grant_type": "authorization_code",
            "code": str(auth_code),
            "redirect_uri": REDIRECT_URI
        }

        auth_str = bytes('{}:{}'.format(CLIENT_ID, CLIENT_SECRET), 'utf-8')
        b64_auth_str = base64.b64encode(auth_str).decode('utf-8')

        headers = {
            "Authorization": "Basic {}".format(b64_auth_str),
            'Content-Type': 'application/x-www-form-urlencoded'
            }
        
        post_request = requests.post(URL_TOKEN, data=payload, headers=headers, allow_redirects=False, timeout=None)

        resp = json.loads(post_request.text)

        access_token = resp['access_token']
        refresh_token = resp['refresh_token']

        tokens['SPOTIFY_ACCESS_TOKEN'] = access_token
        tokens['SPOTIFY_REFRESH_TOKEN'] = refresh_token

        with open('config.json', 'w') as f:
            json.dump(tokens, f, indent=4)

        




#3. Use the access token to access the Spotify Web API; Spotify returns requested data
usr_auth()
