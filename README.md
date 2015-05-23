Music Finder

The Music Search & Recommendation system offers different functionalities to search among songs and artists and get recommendations based on genre.
The main use of this application, has been thought for private users, who wants to discover new songs and artists, according to their preferences. However this service could be also used with the purpose of advertisement. For example, some other commercial web-app (e.g. music-industry executive companies ), could integrate the service provided by this system, to analyze what people like most, and change their strategies basing on that.

Install

To store data, it has been used sqlite. So the data is contained in files, that can be found in the folder db (Python sqlite3: http://docs.python.org/2/library/sqlite3.html).
The project has mainly been built in python, and for the server-side, it has been used the Flask-RESTful framework ( http://flask-restful.readthedocs.org/en/latest/quickstart.html).


Getting started

To run the project, from the main folder (path/musicfinder/), it's sufficient to run the command "python musicfinder.py" .
Once the server has run, showing the writing "Running on http://localhost:5000", it's possible to interact with the web-page, usign the following URL: "http://localhost:5000/musicfinder_admin/ui.html" .

Testing the code

To test the artists resource use the following command from the main folder: "python -m test.database_api_tests_artists"
To test the songs resource use the following command from the main folder: "python -m test.database_api_tests_songs"
To test the user resource use the following command from the main folder: "python -m test.database_api_tests_user"
To test the user REST-ful API use the following command from the main folder: "python -m test.musicfinder_api_tests"