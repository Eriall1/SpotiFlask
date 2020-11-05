# import all needed modules
import spotipy, _pickle as cpickle, time, os
import sqlite3, sys, random, logging
from requests.exceptions import SSLError
from dotenv import load_dotenv
from spotipy import util
from binascii import unhexlify


# setup logging
logger = logging.getLogger('log')
hdlr = logging.FileHandler(filename='console.log', encoding="UTF-8", mode='w+')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
class Database(object): #main class
    def __init__(self, token=None, db="spotiFlaskDB.db"):
        self.conn = sqlite3.connect(db)
        self.token = token
        self.init()

    def init(self): #init function
        load_dotenv()
        self.cursor = self.conn.cursor()
        scope = os.environ.get("SPOTIFLASK_SCOPE")
        cache = os.environ.get("SPOTIFLASK_CACHE")
        username = "Eriall"
        
        if self.token is None: #if token not provided
            self.token = util.prompt_for_user_token(username=username, scope=scope) #fetch one
        # genre list 
        self.genres = [
            "acoustic",
            "afrobeat",
            "alt-rock",
            "alternative",
            "ambient",
            "anime",
            "black-metal",
            "bluegrass",
            "blues",
            "bossanova",
            "brazil",
            "breakbeat",
            "british",
            "cantopop",
            "chicago-house",
            "children",
            "chill",
            "classical",
            "club",
            "comedy",
            "country",
            "dance",
            "dancehall",
            "death-metal",
            "deep-house",
            "detroit-techno",
            "disco",
            "disney",
            "drum-and-bass",
            "dub",
            "dubstep",
            "edm",
            "electro",
            "electronic",
            "emo",
            "folk",
            "forro",
            "french",
            "funk",
            "garage",
            "german",
            "gospel",
            "goth",
            "grindcore",
            "groove",
            "grunge",
            "guitar",
            "happy",
            "hard-rock",
            "hardcore",
            "hardstyle",
            "heavy-metal",
            "hip-hop",
            "holidays",
            "honky-tonk",
            "house",
            "idm",
            "indian",
            "indie",
            "indie-pop",
            "industrial",
            "iranian",
            "j-dance",
            "j-idol",
            "j-pop",
            "j-rock",
            "jazz",
            "k-pop",
            "kids",
            "latin",
            "latino",
            "malay",
            "mandopop",
            "metal",
            "metal-misc",
            "metalcore",
            "minimal-techno",
            "movies",
            "mpb",
            "new-age",
            "new-release",
            "opera",
            "pagode",
            "party",
            "philippines-opm",
            "piano",
            "pop",
            "pop-film",
            "post-dubstep",
            "power-pop",
            "progressive-house",
            "psych-rock",
            "punk",
            "punk-rock",
            "r-n-b",
            "rainy-day",
            "reggae",
            "reggaeton",
            "road-trip",
            "rock",
            "rock-n-roll",
            "rockabilly",
            "romance",
            "sad",
            "salsa",
            "samba",
            "sertanejo",
            "show-tunes",
            "singer-songwriter",
            "ska",
            "sleep",
            "songwriter",
            "soul",
            "soundtracks",
            "spanish",
            "study",
            "summer",
            "swedish",
            "synth-pop",
            "tango",
            "techno",
            "trance",
            "trip-hop",
            "turkish",
            "work-out",
            "world-music"
            ]
        self.isOnline = bool
        self.sp = spotipy.Spotify(self.token) #spotify object for online fetching
        #cant be bothered checking how online code works when not logged into spotify so just disabling code
        '''
        try:
            self.me = self.sp.me()
            self.isOnline = True
        except:
            self.me = cpickle.load(open("meOBJ.pkl", 'br'))
            self.isOnline = False
        '''
        #hard set the isOnline to be False, meaning the app will use offline stored data
        self.isOnline = False
        
        if not self.isOnline:
            self.playlists = cpickle.load(open("playlistsOBJ.pkl", "br"))
            self.playlistTrackIds = cpickle.load(open("playlistTrackIdsOBJ.pkl", "br"))
            self.me = cpickle.load(open("meOBJ.pkl", 'br'))

        cpickle.dump(self.me, open("meOBJ.pkl", 'bw+')) #only matters when online

    class Table(object): #object to help generate tables / insert data
        def __init__(self, name, args): #init the table
            self.name = name
            self.args = ', '.join(args)
            self.argKey = [i.split(' ')[0] for i in self.args.split(', ') if i.split(' ')[0] != "FOREIGN" and not i.split(' ')[0].startswith("CHECK")]
            logger.debug(f"TABLE DATA {name}:\n")
            logger.debug(self.name)
            logger.debug(self.args)
            logger.debug(self.argKey)

        def createQ(self): #generates create query
            return f"CREATE TABLE {self.name} ({self.args})"

        def insertQ(self, values): #generates an insert query
            strarg = []
            for i in values:
                if type(i) != str:
                    strarg.append(i)
                else:
                    strarg.append('"'+i.replace('"', "'")+'"')
            else:
                strarg = ', '.join(str(i) for i in strarg)
                query = f"INSERT INTO {self.name} ({', '.join(self.argKey)}) VALUES ({strarg})" #insert generation
                logger.debug(query)
                return query

        def dropQ(self): #generates a drop query
            return f"DROP TABLE IF EXISTS {self.name}"

    def getSongs(self): #wrapper function for offline capabilities
        if self.isOnline:
            songOBJ = self._spotifyScrape()
        else:
            logger.warn(f"REQUEST ERROR")
            logger.warn("FALLING BACK ONTO SAVED FILE")
            songOBJ = self._inbuiltScrape()
        logger.info("SAVING SONG OBJ TO BUILTIN FILE TO SUPPORT OFFLINE MODE")
        self.saveSongs(songOBJ)
        return songOBJ

    def saveSongs(self, trackObj, path="trackOBJ.pkl"): #saves for offline capability
        with open(path, "bw+") as f:
            cpickle.dump(trackObj, f)
        return True

    def objToDB(self, pathToOBJ=None, pathToDB="spotiFlaskDB.db"): #Main function responsible for 
        startTime = time.time()
        #setup all of the tables and their various data in a dictionary
        tableDict = {"User": ["Username VARCHAR(25) PRIMARY KEY", 
                                "UserToken VARCHAR(250)", 
                                "isPremium BOOL", 
                                "displayName VARCHAR(30)"],

                    "Playlists": ["playlistID CHAR(22) PRIMARY KEY", 
                                "songCount INT NOT NULL", 
                                "userID VARCHAR(22) NOT NULL", 
                                "playlistName VARCHAR(100) NOT NULL"],

                    "Tracks": ["songID CHAR(22) PRIMARY KEY", 
                                "duration INT NOT NULL", 
                                "songName VARCHAR(200) NOT NULL", 
                                "popularity INT NOT NULL", 
                                "genre VARCHAR(20)", 
                                "albumID CHAR(22) NOT NULL", 
                                "artistID CHAR(22) NOT NULL",
                                "FOREIGN KEY(albumID) REFERENCES Albums(albumID)", 
                                "FOREIGN KEY(artistID) REFERENCES TrackArtists(artistID)", 
                                "CHECK(popularity >= 0 AND popularity <= 100)"],
                                
                    "Albums":["albumID CHAR(22) PRIMARY KEY", 
                                "albumName VARCHAR(200) NOT NULL", 
                                "albumSongs INT"],

                    "Artists":["artistID CHAR(22) PRIMARY KEY", 
                                "artistName VARCHAR(100) NOT NULL"],

                    "TrackAlbum":["songID CHAR(22) NOT NULL",
                                "albumID CHAR(22) NOT NULL",
                                "FOREIGN KEY(songID) REFERENCES Tracks(songID)",
                                "FOREIGN KEY(albumID) REFERENCES Albums(albumID)"],

                    "TrackArtists":["songID CHAR(22) NOT NULL",
                                "artistID CHAR(22) NOT NULL",
                                "FOREIGN KEY(songID) REFERENCES Tracks(songID)",
                                "FOREIGN KEY(artistID) REFERENCES Artists(artistID)"],
                                
                    "TrackPlaylists":["songID CHAR(22) NOT NULL",
                                "playlistID CHAR(22) NOT NULL",
                                "FOREIGN KEY(songID) REFERENCES Tracks(songID)",
                                "FOREIGN KEY(playlistID) REFERENCES Playlists(playlistID)"],
                    
                    "AlbumArtists":["albumID CHAR(22) NOT NULL",
                                "artistID CHAR(22) NOT NULL",
                                "FOREIGN KEY(albumID) REFERENCES Albums(albumID)",
                                "FOREIGN KEY(artistID) REFERENCES Artists(artistID)"]
                    }

        Table = self.Table # reference table object so i dont have to call self. everytime
        logger.info("DROPPING TABLES")
        for i in tableDict.keys():
            logger.debug(f"DROPPING {i} TABLE")
            self.cursor.execute(f'''DROP TABLE IF EXISTS {i}''')
        logger.info(f"CREATING TABLES")
        
        tables = [Table(i, tableDict[i]) for i in tableDict.keys()]
        logger.debug(', '.join(['"'+i.name+'"' for i in tables]))
        userT, playlistsT, tracksT, albumsT, artistsT, trackAlbumT, trackArtistsT, trackPlaylistsT, albumArtistsT = tables

        for i in tables:
            logger.debug(f'CREATING {i.name}')
            self.cursor.execute(i.createQ())

        logger.info("OBTAINING DATA")

        if type(pathToOBJ) == str:
            with open(pathToOBJ, 'br') as f:
                songsDict = cpickle.load(f)
        elif pathToOBJ == None:
            songsDict = self.getSongs()

        logger.info("MISC")
        logger.debug(self.me)
        logger.debug(songsDict[0]['track'].keys())
        logger.debug(songsDict[0]['track']['artists'])
        logger.debug(songsDict[0]['track']['track'])
        logger.debug(songsDict[0]['track']['album'].keys())
        logger.debug(songsDict[0]['track']['album']['artists'][0].keys())


        #user data entry
        self.cursor.execute(userT.insertQ([self.me['id'], self.token, True if self.me['product'] == 'premium' else False, self.me['display_name']]))

        #table keys for unique constraints
        trackKeys = []
        albumKeys = []
        artistKeys = []

        for i in songsDict: #for each track
            ctrack = i['track'] #base track data
            x = unhexlify(b'6e696767').decode() in ctrack['name'].lower()
            logger.debug(x)
            if ctrack['id'] and not x: #removes local tracks as they have no id
                calbum = ctrack['album'] #album data from track
                logger.debug(f"INSERT TRACK/ALBUM ({ctrack['id']}/{ctrack['album']['id']}) INTO TrackAlbum TABLE")
                self.cursor.execute(trackAlbumT.insertQ([ctrack['id'], calbum['id']])) #insert track / album ids into table medium

                for i in ctrack['artists']: #for each artist in track data
                    logger.debug(f"INSERT TRACK/ARTIST ({ctrack['id']}/{i['id']}) INTO TrackAlbum TABLE")
                    self.cursor.execute(trackArtistsT.insertQ([ctrack['id'], i['id']])) #insert track / artist ids into table medium
                    if not i['id'] in artistKeys:
                        self.cursor.execute(artistsT.insertQ([i['id'], i['name']])) #also insert artist into artist table while we here
                        artistKeys.append(i['id'])


                if not calbum['id'] in albumKeys: #check unique album
                    logger.debug(f"INSERT ALBUM ({calbum['id']}) INTO Album TABLE")
                    self.cursor.execute(albumsT.insertQ([calbum['id'], calbum['name'], calbum['total_tracks']]))

                    for i in calbum['artists']:
                        logger.debug(f"INSERT ALBUM/ARTIST ({calbum['id']}/{i['id']}) INTO TrackAlbum TABLE")
                        self.cursor.execute(albumArtistsT.insertQ([calbum['id'], i['id']]))
                    albumKeys.append(calbum['id'])
                

                if not ctrack['id'] in trackKeys:
                    #logger.debug(f"INSERT TRACK {ctrack['id']} INTO Track TABLE")
                    iquery = tracksT.insertQ([ctrack['id'], ctrack['duration_ms'], ctrack['name'], ctrack['popularity'], random.choice(self.genres), ctrack['album']['id'], ctrack['id']])
                    if iquery:
                        self.cursor.execute(iquery)
                    trackKeys.append(ctrack['id'])
            else:
                logger.debug(f"COULD NOT FIND VALID ID FOR {ctrack['name']}, POSSIBLY A LOCAL TRACK ({ctrack['is_local']})")
        #print(songsDict[0]['track']['album'])
        #print(*[(i, songsDict[0]['track'][i]) for i in songsDict[0]['track'].keys()], end="\n\n")

        if self.playlists:
            logger.debug(", ".join([i for i in self.playlists['items'][0].keys()]))
            logger.debug(self.playlists['items'][0]['tracks'])
            for i in self.playlists['items']:
                self.cursor.execute(playlistsT.insertQ([i['id'], i['tracks']['total'], i['owner']['id'], i['name']]))
        
        for i in self.playlistTrackIds:
            if i[0]:
                self.cursor.execute(trackPlaylistsT.insertQ([i[0], i[1]]))

        

        self.conn.commit() #commit all changes to the db record
        self.cursor.close() #close the connection to the db
        stopTime = time.time()
        runningTime = str(stopTime-startTime)
        print(f"SCRIPT RAN FOR {runningTime}")
        return songsDict
                
    def _spotifyScrape(self):
        logger.info("SCRAPING SPOTIFY ID 9ntbx2jbwq9s7fqew766eawob")
        userPublic = self.sp.user_playlists("9ntbx2jbwq9s7fqew766eawob") # my spotify account
        userPublic['items'].extend(self.sp.user_playlists("9ntbx2jbwq9s7fqew766eawob", offset=50)['items']) # my playlists
        
        self.playlists = userPublic #set obj variable for use in obj to db function later
        cpickle.dump(userPublic, open("playlistsOBJ.pkl", "bw+")) #dump playlist obj

            #get current saved (liked) tracks
        userTracks = self.sp.current_user_saved_tracks(limit=50)
        userTracks['items'].extend(self.sp.current_user_saved_tracks(limit=50, offset=50)['items'])
        userTracks['items'].extend(self.sp.current_user_saved_tracks(limit=50, offset=100)['items'])
        logger.debug(len(userTracks['items']))
        logger.debug(len(userPublic['items']))
        logger.debug(userPublic.keys())
        userPublicIds = [i['id'] for i in userPublic['items']]
        allTracks = []
        playlistTrackIds = []
        logger.debug(str(len(allTracks)))
        for i in userPublicIds:
            ctracks = []
            tracks0 = self.sp.playlist_tracks(i, fields="total")
            total = tracks0['total']
            offsetf = None if total%100 == 0 else total%100
            for j in range(total//100):
                x = self.sp.playlist_tracks(i, offset=j*100)['items']
                allTracks.extend(x)
                ctracks.extend(x)
            if offsetf:
                x = self.sp.playlist_tracks(i, offset=total-offsetf)['items']
                allTracks.extend(x)
                ctracks.extend(x)
            logger.debug(f"{str(i)} {str(total)}")
            logger.debug(f'{str(total//100)} {str(offsetf)}')
            for j in ctracks:
                playlistTrackIds.append((j['track']['id'], i))
            #time.sleep(2)

        self.playlistTrackIds = playlistTrackIds
        cpickle.dump(playlistTrackIds, open("playlistTrackIdsOBJ.pkl", "bw+")) #dump playlist ids

        logger.debug(str(len(allTracks)))
        return allTracks
    
    def _inbuiltScrape(self, pathToOBJ="alltracks.pkl"): # offline capability
        with open(pathToOBJ, 'br') as f:
            trackOBJ = cpickle.load(f)
        return trackOBJ
    
    def _insert(self, args): #lol
        self.cursor.execute()



"""
        try:
            logger.info("SCRAPING SPOTIFY ID 9ntbx2jbwq9s7fqew766eawob")
            userPublic = self.sp.user_playlists("9ntbx2jbwq9s7fqew766eawob") # my spotify account
            userPublic['items'].extend(self.sp.user_playlists("9ntbx2jbwq9s7fqew766eawob", offset=50)['items']) # my playlists
            
            self.playlists = userPublic #set obj variable for use in obj to db function later

            #get current saved (liked) tracks
            userTracks = self.sp.current_user_saved_tracks(limit=50)
            userTracks['items'].extend(self.sp.current_user_saved_tracks(limit=50, offset=50)['items'])
            userTracks['items'].extend(self.sp.current_user_saved_tracks(limit=50, offset=100)['items'])
            logger.debug(len(userTracks['items']))
            logger.debug(len(userPublic['items']))
            logger.debug(userPublic[0].keys())
            userPublicIds = [i['id'] for i in userPublic['items']]
            allTracks = []
            logger.debug(len(allTracks))
            for i in userPublicIds:
                tracks0 = self.sp.playlist_tracks(i, fields="total")
                total = tracks0['total']
                offsetf = None if total%100 == 0 else total%100
                for j in range(total//100):
                    allTracks.extend(self.sp.playlist_tracks(i, offset=j*100)['items'])
                if offsetf:
                    allTracks.extend(self.sp.playlist_tracks(i, offset=total-offsetf)['items'])
                logger.debug(i, total)
                logger.debug(total//100, offsetf)
                #time.sleep(2)
            logger.debug(len(allTracks))
            return allTracks
        except:
            self.playlists = False
            return False
"""