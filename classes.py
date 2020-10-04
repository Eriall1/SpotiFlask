import spotipy, _pickle as cpickle, time
import sqlite3, sys, random
sys.stdout = open("console.log", 'w+', encoding="UTF-8")
from requests.exceptions import SSLError
class Database:
    def __init__(self, token, sp=None, db="spotiFlaskDB.db"):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        self.token = token
        if sp:
            self.sp = sp
        else:
            self.sp = spotipy.Spotify(self.token)
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
        self.me = self.sp.me()

    class Table:
        def __init__(self, name, args):
            print(f"TABLE DATA {name}:")
            self.name = name
            self.args = ', '.join(args)
            self.argKey = [i.split(' ')[0] for i in self.args.split(', ') if i.split(' ')[0] != "FOREIGN" and not i.split(' ')[0].startswith("CHECK")]
            print(self.name)
            print(self.args)
            print(self.argKey)
            print()
        def createQ(self):
            return f"CREATE TABLE {self.name} ({self.args})"
        def insertQ(self, values):
            strarg = []
            for i in values:
                if type(i) != str:
                    strarg.append(i)
                else:
                    strarg.append('"'+i.replace('"', "'")+'"')
            else:
                strarg = ', '.join(str(i) for i in strarg)
                query = f"INSERT INTO {self.name} ({', '.join(self.argKey)}) VALUES ({strarg})"
                print(query)
                return query
        def dropQ(self):
            return f"DROP TABLE IF EXISTS {self.name}"

    def getSongs(self):
        songOBJ = self._spotifyScrape()
        if songOBJ == False:
            print(f"REQUEST ERROR")
            print("FALLING BACK ONTO SAVED FILE")
            songOBJ = self._inbuiltScrape()
            self.saveSongs(songOBJ)
        else:
            self.saveSongs(songOBJ)
        return songOBJ

    def saveSongs(self, trackObj, path="trackOBJ.pkl"):
        with open(path, "bw+") as f:
            cpickle.dump(trackObj, f)
        return True

    def objToDB(self, pathToOBJ=None, pathToDB="spotiFlaskDB.db"):
        tableDict = {"User": ["Username CHAR(25) PRIMARY KEY", 
                                "UserToken VARCHAR(250)", 
                                "isPremium BOOL", 
                                "displayName VARCHAR(30) NOT NULL"],

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
                                "FOREIGN KEY(artistID) REFERENCES TrackArtists(songID)", 
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
                    
                    "AlbumArtists":["songID CHAR(22) NOT NULL",
                                "albumID CHAR(22) NOT NULL",
                                "FOREIGN KEY(songID) REFERENCES Tracks(songID)",
                                "FOREIGN KEY(albumID) REFERENCES Albums(albumID)"]
                    }

        Table = self.Table
        print("DROPPING TABLES")
        for i in tableDict.keys():
            print(f"DROPPING {i} TABLE")
            self.cursor.execute(f'''DROP TABLE IF EXISTS {i}''')
        print()
        print(f"CREATING TABLES:")
        
        tables = [Table(i, tableDict[i]) for i in tableDict.keys()]
        print(*[i.name for i in tables])
        userT, playlistsT, tracksT, albumsT, artistsT, trackAlbumT, trackArtistsT, trackPlaylistsT, albumArtistsT = tables

        for i in tables:
            print(f'CREATING {i.name}')
            self.cursor.execute(i.createQ())

        print()
        print("OBTAINING DATA:")

        if type(pathToOBJ) == str:
            with open(pathToOBJ, 'br') as f:
                songsDict = cpickle.load(f)
        elif pathToOBJ == None:
            songsDict = self.getSongs()

        print()
        print("MISC:")
        print(self.me)
        print(*[i for i in songsDict[0]['track'].keys()])
        print(songsDict[0]['track']['artists'])
        print(songsDict[0]['track']['track'])

        self.cursor.execute(userT.insertQ([self.me['id'], self.token, self.me['product'], self.me['display_name']]))

        for i in songsDict:
            ctrack = i['track']
            keys = []
            if ctrack['id']:
                print(f"INSERT TRACK/ALBUM ({ctrack['id']}/{ctrack['album']['id']}) INTO TrackAlbum TABLE")
                self.cursor.execute(trackAlbumT.insertQ([ctrack['id'], ctrack['album']['id']]))
                if not ctrack['id'] in keys:
                    print(f"INSERT TRACK {ctrack['id']} INTO Track TABLE")
                    iquery = tracksT.insertQ([ctrack['id'], ctrack['duration_ms'], ctrack['name'], ctrack['popularity'], random.choice(self.genres), ctrack['album']['id'], ctrack['id']])
                    if iquery:
                        self.cursor.execute(iquery)


            else:
                print(f"COULD NOT FIND VALID ID FOR {ctrack['name']}, POSSIBLY A LOCAL TRACK ({ctrack['is_local']})")
        #print(songsDict[0]['track']['album'])
        #print(*[(i, songsDict[0]['track'][i]) for i in songsDict[0]['track'].keys()], end="\n\n")
        self.conn.commit()
        self.cursor.close()
        return songsDict
                
    def _spotifyScrape(self):
        try:
            userPublic = self.sp.user_playlists("9ntbx2jbwq9s7fqew766eawob") # my spotify account
            userPublic['items'].extend(self.sp.user_playlists("9ntbx2jbwq9s7fqew766eawob", offset=50)['items']) # my playlists
            #get current saved (liked) tracks
            userTracks = self.sp.current_user_saved_tracks(limit=50)
            userTracks['items'].extend(self.sp.current_user_saved_tracks(limit=50, offset=50)['items'])
            userTracks['items'].extend(self.sp.current_user_saved_tracks(limit=50, offset=100)['items'])
            print(len(userTracks['items']))
            print(len(userPublic['items']))
            print(userPublic[0].keys())
            userPublicIds = [i['id'] for i in userPublic['items']]
            allTracks = []
            print(len(allTracks))
            for i in userPublicIds:
                tracks0 = self.sp.playlist_tracks(i, fields="total")
                total = tracks0['total']
                offsetf = None if total%100 == 0 else total%100
                for j in range(total//100):
                    allTracks.extend(self.sp.playlist_tracks(i, offset=j*100)['items'])
                if offsetf:
                    allTracks.extend(self.sp.playlist_tracks(i, offset=total-offsetf)['items'])
                print(i, total)
                print(total//100, offsetf)
                #time.sleep(2)
            print(len(allTracks))
            return allTracks
        except:
            return False
    
    def _inbuiltScrape(self, pathToOBJ="alltracks.pkl"):
        with open(pathToOBJ, 'br') as f:
            trackOBJ = cpickle.load(f)
        return trackOBJ
    
    def _insert(self, args):
        self.cursor.execute()