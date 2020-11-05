import spotipy, os, time, _pickle as cPickle, sqlite3, flask
from flaskapp import app, delete_db

#x = Database(token)
#x.objToDB()
delete_db() #delete the databse on launch
app.run("0.0.0.0", debug=True) #run the existing app defined in flaskapp.py


# classes.py contains all of the backend functions and classes responsible for the creation and insertion of the sample database. 
# It contains the database custom python class as well as the nested table class.

# flaskapp.py contains all of the backend functions and endpoints responsible for the UI and interaction between the python, html and javascript.
# in static there are all of the files not required to be in a top level directory.
# in templates there is all of the required html files for the flask endpoints.
# the .pkl files are all for offline functionality.


#code to gather all tracks, use caches version for reduced requests to spotify api / offline
#moved most of it to classes
#with open("playlists.txt", 'w+') as f:

"""
client_id = os.environ.get("SPOTIPY_CLIENT_ID")
client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
scope = os.environ.get("SPOTIFLASK_SCOPE")
cache = os.environ.get("SPOTIFLASK_CACHE")
redirect_uri = os.environ.get("SPOTIPY_REDIRECT_URI")
username = "Eriall"
#oauth = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
#oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope, username=username)
"""












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