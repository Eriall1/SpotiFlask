import spotipy, os, time
from spotipy.oauth2 import SpotifyOAuth
from spotipy import util
from dotenv import load_dotenv

def loadEnvVariables():
    load_dotenv()

    scope = os.environ.get("SPOTIFLASK_SCOPE")
    cache = os.environ.get("SPOTIFLASK_CACHE")
    username = "test user"
    token = util.prompt_for_user_token(username=username, cache_path=cache, scope=scope)
    sp = spotipy.Spotify(token)
    return sp

def gatherTracks(userID="9ntbx2jbwq9s7fqew766eawob"):
    #with open("playlists.txt", 'w+') as f:
    #code to gather all tracks, use caches version for reduced requests to spotify api
    sp = loadEnvVariables()
    userPublic = sp.user_playlists(userID)
    userPublic['items'].extend(sp.user_playlists(userID, offset=50)['items'])
    userTracks = sp.current_user_saved_tracks(limit=50)
    userTracks['items'].extend(sp.current_user_saved_tracks(limit=50, offset=50)['items'])
    userTracks['items'].extend(sp.current_user_saved_tracks(limit=50, offset=100)['items'])
    print(len(userTracks['items']))
    print(len(userPublic['items']))
    userPublicIds = [i['id'] for i in userPublic['items']]
    allTracks = []
    print(len(allTracks))
    for i in userPublicIds:
        tracks0 = sp.playlist_tracks(i, fields="total")
        total = tracks0['total']
        offsetf = None if total%100 == 0 else total%100
        for j in range(total//100):
            allTracks.extend(sp.playlist_tracks(i, offset=j*100)['items'])
        if offsetf:
            allTracks.extend(sp.playlist_tracks(i, offset=total-offsetf)['items'])
        print(i, total)
        print(total//100, offsetf)
        time.sleep(2)
    print(len(allTracks))
    with open("alltracks.pkl", "bw+") as f:
        cPickle.dump(allTracks, f)
    return allTracks