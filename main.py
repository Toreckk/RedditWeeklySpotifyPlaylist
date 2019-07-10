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
    print('Obtaining new access tokens...')
    auth_params = {
        "client_id" : tokens['SPOTIFY_CLIENT_ID'],
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        #"state":STATE, #OPTIONAL
        "scope":SCOPE, #OPTIONAL
        "show_dialog":SHOW_DIALOG #OPTIONAL
    }
   
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

        if post_request.status_code == 200:
            print ('Tokens obtained succesfully with code: {}'.format(post_request.status_code))
        else:
            post_request.raise_for_status()
            
        resp = json.loads(post_request.text)
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
    payload = {
            "grant_type": "refresh_token",
            "refresh_token": tokens['SPOTIFY_REFRESH_TOKEN']
        }

    post_request = requests.post(URL_TOKEN, data = payload, headers = getSpotifyAuthHeader(), allow_redirects=False, timeout=None)
    
    if post_request.status_code == 200:
        print("Credentials Refreshed correctly!")
        resp = json.loads(post_request.text)
        access_token = resp['access_token']
        tokens['SPOTIFY_ACCESS_TOKEN'] = access_token
        with open('config.json', 'w') as f:
            json.dump(tokens, f, indent=4)
    else:
        post_request.raise_for_status()

'''
1) Gets 50 song titles from reddit
2) Finds their song ID in spotify
3) Returns list of songIDs
'''
def getSongURIs(r):
    print('Obtaining 50 songs from r/{}, this may take some seconds...'.format(tokens['REDDIT_SUBREDDIT']))
    SongIDs = []
    # Title formatting for most songs:
    #   Artist -- Title [Genre](Year)
    #   Artist - Title [Genre](Year)
    # We'll remove everyting from [
    i = 1
    for submission in r.subreddit(tokens['REDDIT_SUBREDDIT']).top(time_filter='week', limit=100):
        title = re.split(r"^([^:(]+?)(\s*[\[\(])", submission.title)

        try: 
            songID = searchSong(title[1])
            SongIDs.append(songID)
            i+=1
        except IndexError:
            pass
        except:
            pass
        if len(SongIDs)>=50:
            print("Succesfully obtained 50 songs")
            return(SongIDs)
            
        


        

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
    
    if len(resp['tracks']['items'])>0:
        return resp['tracks']['items'][0]['uri']
    else:
        raise Exception('No song found with that title')
    
    
    
    
def replacePlaylistTracks(IDList):
    headers = {
        "Authorization": "Bearer {}".format(tokens['SPOTIFY_ACCESS_TOKEN']),
        "Content-Type": "application/json"
    }
    print("Updating playlist...")
    payload = {
        "uris": IDList
    }
    #print(payload)
    url = "https://api.spotify.com/v1/playlists/{}/tracks".format(tokens['SPOTIFY_PLAYLIST_ID'])
    post_request = requests.put(url, json=payload, headers=headers, allow_redirects=False, timeout=None)
    if (post_request.status_code >= 200 and post_request.status_code <300):
        print('Playlist updated successfully!')
    else:
        post_request.raise_for_status()
    



def main():
    # Refresh or create new Spotify Authentication tokens
    usr_auth()

    #Initialize read-only Reddit instance.
    reddit = praw.Reddit(client_id=tokens['REDDIT_CLIENT_ID'],
                        client_secret=tokens['REDDIT_CLIENT_SECRET'],
                        user_agent=tokens['REDDIT_USER_AGENT'])
    #Returns a list of 50 songs ID
    songIDList = getSongURIs(reddit)
    # Replaces old tracks in playlist with new ones
    replacePlaylistTracks(songIDList)
    

if __name__ == "__main__":
    main()

