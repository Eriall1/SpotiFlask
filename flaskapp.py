import sqlite3
from flask import g, Flask, render_template, request, redirect, url_for, jsonify
from classes import logger, Database
import os

app = Flask(__name__)
DATABASE = 'spotiFlaskDB.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def delete_db():
    try:
        tableNameList = ["User", "Playlists", "Tracks", "Albums", "Artists", "TrackAlbum", "TrackArtists", "TrackPlaylists", "AlbumArtists"]
        logger.info("DROPPING DATABASE; User Call")
        try:
            for i in tableNameList:
                get_db().execute(f"DROP TABLE {i}")
                logger.debug(f"DROPPING {i}; REASON: User Call [Delete Database]")
        except sqlite3.OperationalError as e:
            logger.warning("RuntimeError; "+e.__str__()+"; User calling DeleteDB whilst no tables; Ignore")
    except RuntimeError as e:
        logger.warning("RuntimeError; "+e.__str__()+"; POSSIBLE REASON: FIRST TIME STARTUP")

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return redirect(url_for("homepage"))

@app.route('/tables/', methods=["GET"])
def tables():
    cur = get_db().cursor()
    return render_template("tables.html")

@app.route('/homepage/', methods=["GET"])
def homepage():
    tableNames = get_db().execute("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';").fetchall()
    return render_template("homepage.html", tableNames=tableNames)
    #cur = get_db().cursor()

@app.route('/query/', methods=["GET", "POST"])
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

@app.route('/guide/', methods=["GET"])
def guide():
    with open("guide.txt") as f:
        Lines = [i.strip() for i in f.readlines()]
        lines = []
    for i in Lines:
        if not i.startswith('<'):
            lines.append("<p>"+i+"</p>")
        else:
            lines.append(i)

    return render_template("guide.html", lines=lines)
    #cur = get_db().cursor()

@app.route('/_get_table_values')
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

@app.route('/query_sql')
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
        query = f"SELECT {searchVar} FROM {tableName} WHERE {tableName}.{qVar} LIKE '%{search}%' ORDER BY {tableName}.{orderVal} GROUP BY {tableName}.{orderVal}"
    queryOut = get_db().execute(query).fetchall()
    output = {}
    output['results'] = queryOut
    return jsonify(output)
@app.route('/DBFunc')
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

def multi_request(request):
    logger.info(f"Multi Request Received; {request.__str__()}")
    tableNames = request.args.getlist("table[]")
    searchVar = ", ".join(request.args.getlist("variable[]"))
    tableName = tableNames[0] + "".join([f" INNER JOIN {i}" for i in tableNames[1::]])
    print(tableName)
    qVar1 = request.args['qVar1']
    qVar2 = request.args['qVar2']
    table1 = request.args['table1']
    table2 = request.args['table2']
    orderTable = request.args['orderTable']
    groupTable = request.args['groupTable']
    groupVar = request.args['group']
    orderVal = request.args['order']

    if "*" in searchVar.split(', '):
        searchVar = "*"
    baseQ = f"SELECT {searchVar} FROM {tableName} WHERE {table1}.{qVar1} == {table2}.{qVar2}"
    if orderVal == "None" and groupVar == "None":
        query = baseQ
    elif groupVar == "None" and orderVal != "None":
        query = baseQ+f" ORDER BY {orderTable}.{orderVal}"
    elif orderVal == "None" and groupVar != "None":
        query = baseQ+f" GROUP BY {groupTable}.{groupVar}"
    else:
        query = baseQ+f" ORDER BY {orderTable}.{orderVal} GROUP BY {groupTable}.{orderVal}"
    queryOut = get_db().execute(query).fetchall()
    logger.info(query)
    
    output = {}
    output['results'] = queryOut
    return jsonify(output)

@app.route("/fetchValue")
def fetchValues(tableName):
     # good for debug, make sure args were sent
    table = request.args['table']
    logger.debug(table)
    queryOut = []
    queryOut.extend(get_db().execute(f"PRAGMA table_info('{table}')").fetchall())
    logger.debug(queryOut)
    output = {}
    output['variables'] = [i[1] for i in queryOut]
    return jsonify(output)
