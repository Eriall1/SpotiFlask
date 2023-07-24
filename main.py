import spotipy, os, time, _pickle as cPickle, sqlite3, flask
from flaskapp import app, delete_db


delete_db() #delete the databse on launch
app.run("0.0.0.0", debug=True) #run the existing app defined in flaskapp.py

"""
classes.py contains all of the backend functions and classes responsible for the creation and insertion of the sample database. 
It contains the database custom python class as well as the nested table class.

flaskapp.py contains all of the backend functions and endpoints responsible for the UI and interaction between the python, html and javascript.
in static there are all of the files not required to be in a top level directory.
in templates there is all of the required html files for the flask endpoints.
the .pkl files are all for offline functionality.


code to gather all tracks, use caches version for reduced requests to spotify api / offline
moved most of it to classes """
