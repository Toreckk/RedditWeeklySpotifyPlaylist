import requests
import json
import base64
import urllib
import praw
import re

# Client Keys
with open('./config.json') as f:
    tokens = json.loads(f.read())

#Spotify Base URLs
URL_AUTH = "https://accounts.spotify.com/authorize"
URL_TOKEN = "https://accounts.spotify.com/api/token"
BASE_URL = "https://api.spotify.com/v1"

REDIRECT_URI = "http://localhost:8888/callback"
STATE = ""
SCOPE = "user-library-read playlist-modify-private playlist-modify-public"
SHOW_DIALOG = str(False).lower()

#Authorization header for Spotify API requests
def getSpotifyAuthHeader():
    auth_str = bytes('{}:{}'.format(tokens['SPOTIFY_CLIENT_ID'], tokens['SPOTIFY_CLIENT_SECRET']), 'utf-8')
    b64_auth_str = base64.b64encode(auth_str).decode('utf-8')

    headers = {
        "Authorization": "Basic {}".format(b64_auth_str),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    return headers
#Gets the Spotify code to obtain your access and refresh tokens


# if the config.json doesn't have it
def req_auth_app():
    auth_params = {
        "client_id" : tokens['SPOTIFY_CLIENT_ID'],
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


# If there is no refresh token we obtain a new refresh token and access token
# Else we refresh the access token with the refresh token
def usr_auth():
    if(len(tokens['SPOTIFY_REFRESH_TOKEN'])<1): # If no previous token exists we obtain 

        auth_code = req_auth_app()

        payload = {
            "grant_type": "authorization_code",
            "code": str(auth_code),
            "redirect_uri": REDIRECT_URI
        }

        
        
        post_request = requests.post(URL_TOKEN, data=payload, headers=getSpotifyAuthHeader(), allow_redirects=False, timeout=None)

        resp = json.loads(post_request.text)
        print(resp)
        access_token = resp['access_token']
        refresh_token = resp['refresh_token']

        tokens['SPOTIFY_ACCESS_TOKEN'] = access_token
        tokens['SPOTIFY_REFRESH_TOKEN'] = refresh_token

        with open('config.json', 'w') as f:
            json.dump(tokens, f, indent=4)
    else:#We have refresh token -> We use it to obtain a new access token
        refresh_credentials()
          
def refresh_credentials():
    print("Refreshing credentials...")
    print("REFRESH TOKEN: "+ tokens['SPOTIFY_REFRESH_TOKEN'])
    payload = {
            "grant_type": "refresh_token",
            "refresh_token": tokens['SPOTIFY_REFRESH_TOKEN']
        }

    post_request = requests.post(URL_TOKEN, data = payload, headers = getSpotifyAuthHeader(), allow_redirects=False, timeout=None)
    print(post_request.text)
    
    if post_request.status_code == 200:
        print("Credentials Refreshed correctly!")
        resp = json.loads(post_request.text)
        access_token = resp['access_token']
        tokens['SPOTIFY_ACCESS_TOKEN'] = access_token
        with open('config.json', 'w') as f:
            json.dump(tokens, f, indent=4)
    else:
        print("Failed to refresh credentials with error code {}".format(post_request.status_code))

'''
1) Gets 50 song titles from reddit
2) Finds their song ID in spotify
3) Returns list of songIDs
'''
def getSongURIs(r):
    SongIDs = []
    # Title formatting for most songs:
    #   Artist -- Title [Genre](Year)
    #   Artist - Title [Genre](Year)
    # We'll remove everyting from [
    i = 1
    for submission in r.subreddit('listentothis').top(time_filter='week', limit=100):
        title = re.split(r"^([^:(]+?)(\s*[\[\(])", submission.title)
        #print(title[1])
        try: 
            songID = searchSong(title[1])
            print("{}. {} ID: {}".format(i, title[1], songID))
            SongIDs.append(songID)
            i+=1
        except IndexError:
            pass
        except:
            print("No song found with title {}".format(title[1]))
        if len(SongIDs)>=50:
            print("----------------")
            print("50 songs reached")
            print("----------------")
            break
        


        

def searchSong(songTitle):
    url = "https://api.spotify.com/v1/search"
    TitleSearch = songTitle.replace(' ', '%20')
    query_params = {
        "q":TitleSearch,
        "type":"",
        "limit":"1",#We only want the first result
    }
    
    search_url = "{}?q={}&type=track&limit=1".format(url,query_params['q'])
    headers = {
        "Authorization": "Bearer {}".format(tokens['SPOTIFY_ACCESS_TOKEN']),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    song = requests.get(search_url, headers = headers, allow_redirects=False, timeout=None)
    resp = json.loads(song.text)
    #print(resp)
    
    if len(resp['tracks']['items'])>0:
        #print("Track ID: "+ resp['tracks']['items'][0]['id'])
        return resp['tracks']['items'][0]['id']
    else:
        #print("Song not found")
        raise Exception('No song found with that title')
    
    
    
    




def main():
    #Initialize Spotify
    usr_auth()

    #Initialize Reddit
    reddit = praw.Reddit(client_id=tokens['REDDIT_CLIENT_ID'],
                        client_secret=tokens['REDDIT_CLIENT_SECRET'],
                        user_agent=tokens['REDDIT_USER_AGENT'])
    getSongURIs(reddit)
    

if __name__ == "__main__":
    main()

