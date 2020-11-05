import sqlite3
from flask import g, Flask, render_template, request, redirect, url_for, jsonify
from classes import logger, Database
import os

app = Flask(__name__)
DATABASE = 'spotiFlaskDB.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE) # connect to databse on request happening
    return db

def delete_db(): #wipe db
    try:
        tableNameList = ["User", "Playlists", "Tracks", "Albums", "Artists", "TrackAlbum", "TrackArtists", "TrackPlaylists", "AlbumArtists"] #list of tables names
        logger.info("DROPPING DATABASE; User Call")
        try:
            for i in tableNameList:
                get_db().execute(f"DROP TABLE {i}") #drop tables
                logger.debug(f"DROPPING {i}; REASON: User Call [Delete Database]")
        except sqlite3.OperationalError as e:
            logger.warning("RuntimeError; "+e.__str__()+"; User calling DeleteDB whilst no tables; Ignore")
    except RuntimeError as e: #except error if its out of request context
        logger.warning("RuntimeError; "+e.__str__()+"; POSSIBLE REASON: FIRST TIME STARTUP")
        logger.warning("Re calling delete_db out of application context")
        db = sqlite3.connect(DATABASE) # connect to db out of reqauest context
        try:
            for i in tableNameList:
                db.execute(f"DROP TABLE {i}")
                logger.debug(f"DROPPING {i}; REASON: User Call [Delete Database]")
            db.commit()
        except sqlite3.OperationalError as e:
            logger.debug(e.__str__())

def query_db(query, args=(), one=False): # query db
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext #idk what this does ngl sir
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/') #redirect function to homepage
def index():
    return redirect(url_for("homepage"))

@app.route('/tables/', methods=["GET"]) #rendering for the tables endpoint
def tables():
    return render_template("tables.html")

@app.route('/homepage/', methods=["GET"]) # rendering for homepage endpoint
def homepage():
    tableNames = get_db().execute("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';").fetchall()
    return render_template("homepage.html", tableNames=tableNames)
    #cur = get_db().cursor()

@app.route('/query/', methods=["GET", "POST"])# rendering for query endpoint
def query():
    tableNames = get_db().execute("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';").fetchall()
    if request.method == "POST":
        queryResults = get_db().execute(request.form['query'].upper())
        qData = request.form['query'].upper().split(' ')
        tableName = qData[qData.index("FROM")+1]
        tableHeadings = get_db().execute(f"PRAGMA table_info('{tableName}')")
        return render_template("query.html", queryResults=queryResults, tableHeadings=tableHeadings, tableNames=tableNames)

    elif request.method == "GET":
        return render_template("query.html", tableNames=tableNames)
    #cur = get_db().cursor()

@app.route('/guide/', methods=["GET"])# rendering for guide endpoint
def guide():
    with open("static/guide.txt") as f:
        Lines = [i.strip() for i in f.readlines()]
        lines = []
    for i in Lines:
        if not i.startswith('<'):
            lines.append("<p>"+i+"</p>")
        else:
            splitup = i.split(' ')
            x = splitup[0]+'>' if splitup[0][-1] != '>' else splitup[0]
            y = x[0]+'/'+x[1::]
            end = x + ' '.join(splitup[1::]) + y
            #print(end)
            lines.append(end)

    return render_template("guide.html", lines=lines)
    #cur = get_db().cursor()

@app.route('/_get_table_values') #backend endpoint for js
def _get_table_values():
    # good for debug, make sure args were sent
    logger.debug(request.args)
    table = request.args['table']
    logger.debug(table)
    queryOut = get_db().execute(f"PRAGMA table_info('{table}')").fetchall()
    logger.debug(queryOut)
    output = {}
    output['variables'] = [i[1] for i in queryOut]
    return jsonify(output)

@app.route('/query_sql') #backend endpoint for js
def query_sql():
    logger.debug(request.args)
    isMulti = request.args['multi'] == "true"
    logger.debug(isMulti)
    if isMulti:
        return multi_request(request)
    tableName = request.args['table']
    searchVar = request.args["variable"]
    search = request.args['query']
    orderVal = request.args['order']
    qVar = request.args['qVar1']
    groupVar = request.args['group']
    if orderVal == "None" and groupVar == "None":
        query = f"SELECT {searchVar} FROM {tableName} WHERE {tableName}.{qVar} LIKE '%{search}%'"
    elif groupVar == "None" and orderVal != "None":
        query = f"SELECT {searchVar} FROM {tableName} WHERE {tableName}.{qVar} LIKE '%{search}%' ORDER BY {tableName}.{orderVal}"
    elif orderVal == "None" and groupVar != "None":
        query = f"SELECT {searchVar} FROM {tableName} WHERE {tableName}.{qVar} LIKE '%{search}%' GROUP BY {tableName}.{groupVar}"
    else:
        query = f"SELECT {searchVar} FROM {tableName} WHERE {tableName}.{qVar} LIKE '%{search}%' GROUP BY {tableName}.{orderVal} ORDER BY {tableName}.{orderVal}"
    logger.debug(query)
    queryOut = get_db().execute(query).fetchall()
    output = {}
    output['results'] = queryOut
    return jsonify(output)

@app.route('/DBFunc')#backend endpoint for js DB functions
def DBFunc():
    x = Database()
    function = request.args['function']
    print(function)
    if function == "init":
        get_db()
    elif function == "fill":
        x.objToDB()
    elif function == "drop":
        delete_db()
    return jsonify(True)

def multi_request(request): #backend endpoint for js
    logger.info(f"Multi Request Received; {request.__str__()}")
    qVar1 = request.args['qVar1']
    qVar2 = request.args['qVar2']
    table1 = request.args['table1']
    table2 = request.args['table2']
    logger.debug(", ".join([qVar1, qVar2, table1, table2]))
    searchVar = f'{table1}.{qVar1}, {table2}.{qVar2}'
    tableName = f"{table1} INNER JOIN {table2}"
    baseQ = f"SELECT * FROM {tableName} ON {table1}.{qVar1} == {table2}.{qVar2}"
    query = baseQ
        
    logger.info(query)
    queryOut = get_db().execute(query).fetchall()
    
    output = {}
    output['results'] = queryOut
    return jsonify(output)

@app.route("/fetchValue") #backend endpoint for js
def fetchValues():
     # good for debug, make sure args were sent
    table = request.args['table']
    logger.debug(table)
    queryOut = []
    queryOut.extend(get_db().execute(f"PRAGMA table_info('{table}')").fetchall())
    logger.debug(queryOut)
    output = {}
    output['variables'] = [i[1] for i in queryOut]
    return jsonify(output)

@app.route('/multiHeader') #backend endpoint for js
def multiHeader():
    t1 = request.args['table1']
    t2 = request.args['table2']
    queryOut = []
    queryOut.extend(f"{t1}.{i[1]}" for i in get_db().execute(f"PRAGMA table_info('{t1}')").fetchall())
    queryOut.extend(f"{t2}.{i[1]}" for i in get_db().execute(f"PRAGMA table_info('{t2}')").fetchall())
    output = {}
    output['headers'] = queryOut
    return jsonify(output)

@app.route('/genReport') #backend endpoint for report generation
def genReport():
    headers = ['Max Song Duration (ms)', "Average Song Duration (ms)", "Minimum Song Duration (ms)", "Sum of All Song Durations (ms)", "Number of Songs", "Number of Artists", "Number of Albums", "Average Songs in Albums", "Number of Playlists", "Average Songs of Playlists"]
    queries = ["SELECT MAX(Tracks.duration) FROM Tracks", "SELECT AVG(Tracks.duration) FROM Tracks", "SELECT MIN(Tracks.duration) FROM Tracks", "SELECT SUM(Tracks.duration) FROM Tracks", "SELECT COUNT(Tracks.songID) FROM Tracks", "SELECT COUNT(Artists.artistID) FROM Artists", "SELECT COUNT(Albums.albumID) FROM Albums", "SELECT AVG(Albums.albumSongs) FROM Albums", "SELECT COUNT(Playlists.playlistID) FROM Playlists", "SELECT AVG(Playlists.songCount) FROM Playlists"]
    data = [get_db().execute(i).fetchall()[0][0] for i in queries]
    print(data)
    output = {"headers":headers, "data":data}
    return jsonify(output)

@app.route('/insertUser') #backend endpoint for js
def insertUser():
    userID = request.args['id']
    token = request.args['token']
    premium = request.args.get('isPremium', default=None)
    name = request.args['displayName']
    print(userID, token, premium, name)
    if premium is None:
        premium = False
    else:
        premium = True
    try:
        get_db().execute(f'INSERT INTO User (Username, UserToken, isPremium, displayName) VALUES ("{userID}", "{token}", {premium}, "{name}")')
        get_db().commit()
    except sqlite3.OperationalError as e:
        print(e)
        logger.debug(e.__str__())
    return redirect(url_for("tables"))