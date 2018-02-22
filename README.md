# Music Finder

This Music Search & Recommendation system offers different functionalities to search among songs and artists and get recommendations based on genre.
This application is mainly aimed for private users, who wish to discover new songs and artists, according to their preferences. However this service could be also used with the purpose of advertisement. For example, some external commercial web-app (e.g. music-industry executive companies) could integrate the service provided by this system, to analyze what people like most, and change their strategies accordingly.

## Installation

SQLite is used to store data. The data can be found in the folder db (Python sqlite3: http://docs.python.org/2/library/sqlite3.html).
The project has been built using Python; the backend relies on the Flask-RESTful framework ( http://flask-restful.readthedocs.org/en/latest/quickstart.html).


## Getting started

To run the project (both client and server), from the main folder (path/musicfinder/), it's sufficient to run the command:

> python musicfinder.py

Once the server has started, the log message "Running on http://localhost:5000" will appear, and it will be possible to interact with the web-page at the following URL: "http://localhost:5000/musicfinder_admin/ui.html" .

## Testing the code

To test the database API for the artists resource use the following command from the main folder

> python -m test.database_api_tests_artists

To test the database API for the songs resource use the following command from the main folder: 

> python -m test.database_api_tests_songs

To test the database API for the user's resource use the following command from the main folder: 

> python -m test.database_api_tests_user

To test the user REST-ful API use the following command from the main folder: 

> python -m test.musicfinder_api_tests

## External dependencies

The GUI uses the library JQuery (v 1.11.2), that can be found in the folder "musicfinder/musicfinder_admin/static/".
The GUI uses the framework Bootstrap (v 3.3.4) located in the folder "musicfinder/musicfinder_admin/static/bootstrap" (the folder contains the css, fonts and javascript functions in the relative sub-folders).
[_unittest_](http://docs.python.org/2/library/unittest.html) was used for testing .

## RESTful API endpoints

- **ENTRYPOINT** = /musicfinder/api/

- **Artists** = /musicfinder/api/artists/

- **Artist** = /musicfinder/api/artists/<artist>/

- **Songs** = /musicfinder/api/artists/<artist>/songs/

- **Song** = /musicfinder/api/artists/<artist>/songs/<title>

- **Users** = /musicfinder/api/users/

- **User** = /musicfinder/api/users/<nickname>/

- **User_playlists** = /musicfinder/api/users/<nickname>/playlists/

- **Playlist** = /musicfinder/api/users/<nickname>/playlists/<title>/

- **Playlist_songs** = /musicfinder/api/users/<nickname>/playlists/<title>/songs/
