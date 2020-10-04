import spotipy, os, time
from spotipy.oauth2 import SpotifyOAuth
from spotipy import util
import sqlite3
from classes import Database

# Set up connection to database and open a cursor
db = sqlite3.connect("spotiFlaskDB.db")
cursor = db.cursor()



# Save changes to the database and close the cursor
db.commit()
db.close()

from dotenv import load_dotenv
import pandas as pd

load_dotenv()
scope = os.environ.get("SPOTIFLASK_SCOPE")
cache = os.environ.get("SPOTIFLASK_CACHE")
username = "test user"

import _pickle as cPickle

token = util.prompt_for_user_token(username=username, cache_path=cache, scope=scope)

sp = spotipy.Spotify(token)

x = Database(token, sp)
x.objToDB()

#with open("playlists.txt", 'w+') as f:
#code to gather all tracks, use caches version for reduced requests to spotify api




















"""
with open("allTracks.pkl", "br") as f:
    allTracks = cPickle.load(f)
print(len(allTracks))
idNum = 0
trackInfo = {}
print(allTracks[0]['track'].keys())
highestPop = 0
popTrack = None
for i in allTracks:
    track = i['track']
    trackInfo[idNum] = {'trackID':track['id'],
                        'trackName':track['name'], 
                        'artists':', '.join(track['artists'][j]['name'] for j in range(len(track['artists']))).split(', '), 
                        'duration':track['duration_ms'],
                        'popularity':track['popularity'],
                        }
    
    if int(trackInfo[idNum]['popularity']) < 50 and int(trackInfo[idNum]['popularity']) > 40:
        print(trackInfo[idNum])
    if int(trackInfo[idNum]['popularity']) > highestPop:
        popTrack = trackInfo[idNum]
        highestPop = int(trackInfo[idNum]['popularity'])
    
    '''
    if "FINNEAS" in trackInfo[idNum]['artists']:
        print(trackInfo[idNum])
    '''
    '''
    if "slow" in trackInfo[idNum]['trackName'].lower():
        print(trackInfo[idNum])
    '''
    #print(idNum, i['track']['name'], "|||", ', '.join(i['track']['artists'][j]['name'] for j in range(len(i['track']['artists']))))
    idNum += 1
#print("\n\n\n")
#print(popTrack)
"""