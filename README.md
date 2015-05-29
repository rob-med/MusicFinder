Music Finder

The Music Search & Recommendation system offers different functionalities to search among songs and artists and get recommendations based on genre.
The main use of this application, has been thought for private users, who wants to discover new songs and artists, according to their preferences. However this service could be also used with the purpose of advertisement. For example, some other commercial web-app (e.g. music-industry executive companies ), could integrate the service provided by this system, to analyze what people like most, and change their strategies basing on that.

Install

To store data, it has been used sqlite. So the data is contained in files, that can be found in the folder db (Python sqlite3: http://docs.python.org/2/library/sqlite3.html).
The project has mainly been built in python, and for the server-side, it has been used the Flask-RESTful framework ( http://flask-restful.readthedocs.org/en/latest/quickstart.html).


Getting started

To run the project (both client and server), from the main folder (path/musicfinder/), it's sufficient to run the command "python musicfinder.py" .
Once the server has run, it will show the log message "Running on http://localhost:5000", and it'll be possible to interact with the web-page, using the following URL: "http://localhost:5000/musicfinder_admin/ui.html" .

Testing the code

To test the database API for the artists resource use the following command from the main folder: "python -m test.database_api_tests_artists"
To test the database API for the songs resource use the following command from the main folder: "python -m test.database_api_tests_songs"
To test the database API for the user's resource use the following command from the main folder: "python -m test.database_api_tests_user"
To test the user REST-ful API use the following command from the main folder: "python -m test.musicfinder_api_tests"

External dependencies

The GUI uses the library JQuery (v 1.11.2), and it's contained in the folder "musicfinder/musicfinder_admin/static/"
The GUI uses the framework Bootstrap (v 3.3.4) and it's contained in the folder "musicfinder/musicfinder_admin/static/bootstrap" (the folder contains the css, fonts and javascript functions in the relative sub-folders)
It has been used the library "unittest" of Python for testing (http://docs.python.org/2/library/unittest.html).

RESTful API

ENTRYPOINT = /musicfinder/api/
Artists = /musicfinder/api/artists/
Artist = /musicfinder/api/artists/<artist>/
Songs = /musicfinder/api/artists/<artist>/songs/
Song = /musicfinder/api/artists/<artist>/songs/<title>
Users = /musicfinder/api/users/
User = /musicfinder/api/users/<nickname>/
User_playlists = /musicfinder/api/users/<nickname>/playlists/
Playlist = /musicfinder/api/users/<nickname>/playlists/<title>/
Playlist_songs = /musicfinder/api/users/<nickname>/playlists/<title>/songs/