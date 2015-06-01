import json

from flask import Flask, request, Response, g, jsonify
from flask.ext.restful import Resource, Api, abort
from werkzeug.exceptions import NotFound,  UnsupportedMediaType
import database

DEFAULT_DB_PATH = 'db/musicdb.db'

#Constants for hypermedia formats and profiles
COLLECTIONJSON = "application/vnd.collection+json"
HAL = "application/hal+json"

USER_PROFILE = "https://docs.google.com/document/d/1ZDNCygeY6-LY8egEJrTeRPx0g6Esoa9_swQ8hbAP6Wc/edit?usp=sharing"
SONG_PROFILE = "https://docs.google.com/document/d/1dU1e3h7Mu_QxW5m7zA_9749d_W68M_4iMl8IZ-cjmIw/edit?usp=sharing"
ARTIST_PROFILE = "https://docs.google.com/document/d/1Y1V0KY6KZVVixDQdBLcX9mzffHHAPUVunowNSs6n8XY/edit?usp=sharing"
PLAYLIST_PROFILE = "https://docs.google.com/document/d/1qSKj2f4MgQ1L1qx1qbanf76BIcR03lz5uuJ4npfZS6s/edit?usp=sharing"

ATOM_THREAD_PROFILE = "https://tools.ietf.org/html/rfc4685"


#Define the application and the api
app = Flask(__name__)
app.debug = True
#Set the database API. Change the DATABASE value from app.config to modify the
#database to be used (for instance for testing)
app.config.update({'DATABASE':database.MusicDatabase(DEFAULT_DB_PATH)})
#Start the RESTful API.
api = Api(app)



def create_error_response(status_code, title, message, resource_type=None):
    response = jsonify(title=title, message=message, resource_type=resource_type)
    response.status_code = status_code
    return response

@app.errorhandler(404)
def resource_not_found(error):
    return create_error_response(404, "Resource not found", "This resource url does not exit")

@app.errorhandler(500)
def unknown_error(error):
    return create_error_response(500, "Error", "The system has failed. Please, contact the administrator")

@app.before_request
def set_database():
    '''Stores an instance of the database API before each request in the flas.g
    variable accessible only from the application context'''
    g.db = app.config['DATABASE']

class Artists(Resource):

    def get(self):

        parameters = request.args
        country = parameters.get('country',None)
        language = parameters.get('language', None)
        name = parameters.get('name', None)
        genre = parameters.get('genre', None)

        artist_db = g.db.get_artists(name, genre, country, language)

        envelope = {}
        collection = {}
        envelope["collection"] = collection
        collection['version'] = "1.0"
        collection['href'] = api.url_for(Artists)

        collection['queries'] = [
            {'href':api.url_for(Artists),
             'rel':'search',
             'prompt':"Search artists",
             'data' : [
                {"prompt" : "Search the artists by name",
                 "name" : "name",
                 "value" : "",
                 "required":False},
                {"prompt" : "Search the artist by genre",
                 "name" : "genre",
                 "value" : "",
                 "required":False},
                {"prompt" : "Search the artists by country",
                 "name" : "country",
                 "value" : "",
                 "required":False},
                {"prompt" : "Search the artists by language",
                 "name" : "language",
                 "value" : "",
                 "required":False}

                ]
            }
        ]

        collection['template'] = {
        "data" : [
            {"prompt" : "", "name" : "legalName", "value" : "", "required":True},
            {"prompt" : "", "name" : "foundingLocation", "value" : "", "required":False},
            {"prompt" : "", "name" : "genre", "value" : "", "required":False},
            {"prompt" : "", "name" : "language", "value" : "", "required":False},
            {"prompt" : "", "name" : "foundingDate", "value" : "", "required":False}

        ]
        }
        #Create the items
        items = []
        for a in artist_db:
            _name = a['legalName']
            _country = a['foundingLocation']
            _genre = a['genre']
            _language = a['language']
            _formed_in = a['foundingDate']
            _url = api.url_for(Artist, artist=_name)
            artist = {}
            artist['href'] = _url
            artist['data'] = []

            ss = [('legalName',_name), ('genre', _genre), ('foundingLocation',_country), ('language',_language),
                ('foundingDate', _formed_in)]
            for s in ss:
                value = {'name': s[0], 'value': s[1]}
                artist['data'].append(value)

            artist['links'] = []
            items.append(artist)
        collection['items'] = items
        return envelope

    def post(self):
        input = request.get_json(force=True)
        if not input:
            return create_error_response(415, "Unsupported Media Type",
                                         "Use a JSON compatible format",
                                         "Artists")


        try:
            data = input['template']['data']
            dictionary = {}
            for d in data:
                tt = d['name']
                dictionary[tt] = d['value']
            #CHECK THAT DATA RECEIVED IS CORRECT
            if not dictionary['legalName'] or not dictionary['genre']:
                return create_error_response(400, "Wrong request format",
                                             "Be sure you include artist's name and genre",
                                             "Artists")
        except:
            return create_error_response(400, "Wrong request format",
                                         "Be sure you include artist's name and genre",
                                         "Artists")

        aid = g.db.create_artist(dictionary['legalName'], dictionary['genre'], dictionary.get('foundingLocation', None), dictionary.get('language', None), dictionary.get('foundingDate', None))
        if not aid:
            abort(500)
        url = api.url_for(Artist, artist=dictionary['legalName'])

        #RENDER
        #Return the response
        return Response(status=201, headers={'Location':url})

class Artist(Resource):

    def get(self, artist):
        artist_db = g.db.get_artist(artist)
        if not artist_db:
            return create_error_response(404, "Unknown artist",
                                         "There is no artist named %s" % artist,
                                         "Artist")
        #FILTER AND GENERATE RESPONSE
        #Create the envelope:
        envelope = {}
        #Now create the links
        links = {}
        envelope["_links"] = links

        #Fill the links
        _curies = [
            {
            "name": "artist",
            "href": ARTIST_PROFILE,
            },
            {
            "name": "atom-thread",
            "href": ATOM_THREAD_PROFILE
            }
        ]
        links['curies'] = _curies
        links['self'] = {'href':api.url_for(Artist, artist=artist),
                         'profile': ARTIST_PROFILE}
        links['collection'] = [{'href': api.url_for(Artists),
                                'profile': ARTIST_PROFILE,
                                'type': COLLECTIONJSON,
                                'rel': "artists-all"},
                               {'href': api.url_for(Songs, artist=artist),
                                'profile': SONG_PROFILE,
                                'type': COLLECTIONJSON,
                                'rel': "songs-all"}
                               ]

        #Fill the template
        envelope['template'] = {
        "data" : [
            {"prompt" : "", "name" : "legalName", "value" : "", "required":True},
            {"prompt" : "", "name" : "genre", "value" : "", "required":False},
            {"prompt" : "", "name" : "foundingLocation", "value" : "", "required":False},
            {"prompt" : "", "name" : "language", "value" : "", "required":False},
            {"prompt" : "", "name" : "foundingDate", "value" : "", "required":False},

            ]
        }

        #Fill the rest of properties
        envelope['legalName'] = artist_db['legalName']
        envelope['genre'] = artist_db['genre']
        envelope['foundingLocation'] = artist_db['foundingLocation']
        envelope['language'] = artist_db['language']
        envelope['foundingDate'] = artist_db['foundingDate']

        #RENDER
        return Response (json.dumps(envelope), 200, mimetype=HAL+";"+ ARTIST_PROFILE)

class Songs(Resource):

    def get(self, artist):
        songs_db = g.db.get_songs(artist)

        envelope = {}
        collection = {}
        envelope["collection"] = collection
        collection['version'] = "1.0"
        collection['href'] = api.url_for(Songs, artist=artist)
        collection['template'] = {
        "data" : [
            {"prompt" : "", "name" : "name", "value" : "", "required":True},
            {"prompt" : "", "name" : "byArtist", "value" : "", "required":True},
            {"prompt" : "", "name" : "duration", "value" : "", "required":False},
            {"prompt" : "", "name" : "datePublished", "value" : "", "required":False},

            ]
        }
        #Create the items
        items = []
        for a in songs_db:
            _title = a['name']
            _length = a['duration']
            _year = a['datePublished']
            _url = api.url_for(Song, artist=artist, title=_title)
            song = {}
            song['href'] = _url
            song['data'] = []
            ss = [('name',_title), ('byArtist', artist), ('duration',_length), ('datePublished',_year)]
            for s in ss:
                value = {'name': s[0], 'value': s[1]}
                song['data'].append(value)

            song['links'] = []
            items.append(song)
        collection['items'] = items
        return envelope

    def post(self, artist):
        input = request.get_json(force=True)
        if not input:
            return create_error_response(415, "Unsupported Media Type",
                                         "Use a JSON compatible format",
                                         "Songs")

        #It throws a BadRequest exception, and hence a 400 code if the JSON is
        #not wellformed
        try:
            data = input['template']['data']
            title = None
            length = None
            year = None

            dictionary = {}
            for d in data:
                tt = d['name']
                dictionary[tt] = d['value']

            #CHECK THAT DATA RECEIVED IS CORRECT
            if not dictionary.get('name', None):
                return create_error_response(400, "Wrong request format",
                                             "Be sure you include song's title",
                                             "Songs")
        except:
            #This is launched if either title or body does not exist or if
            # the template.data array does not exist.
            return create_error_response(400, "Wrong request format",
                                         "Be sure you include song's title",
                                         "Artists")


        aid = g.db.create_song(dictionary.get('name'), dictionary.get('datePublished', None), dictionary.get('duration', None), artist)
        if not aid:
            abort(500)

        url = api.url_for(Song, artist=artist, title=title)

        #RENDER
        #Return the response
        return Response(status=201, headers={'Location':url})

        return

class Song(Resource):

    def get(self, artist, title):
        song_db = g.db.get_song(artist, title)
        if not song_db:
            return create_error_response(404, "Unknown song",
                                         "There is no song named %s of the artist %s" % (title,artist),
                                         "Song")
        #FILTER AND GENERATE RESPONSE
        #Create the envelope:
        envelope = {}
        #Now create the links
        links = {}
        envelope["_links"] = links

        #Fill the links
        _curies = [
            {
            "name": "song",
            "href": SONG_PROFILE,
            },
            {
            "name": "atom-thread",
            "href": ATOM_THREAD_PROFILE
            }
        ]
        links['curies'] = _curies
        links['self'] = {'href':api.url_for(Song, title=title, artist=artist),
                         'profile': SONG_PROFILE}
        links['collection'] = [{'href':api.url_for(Songs, artist=artist),
                                'profile': SONG_PROFILE,
                                'type':COLLECTIONJSON,
                                'rel': "songs-all"},
                               {'href':api.url_for(Artists),
                                'profile': ARTIST_PROFILE,
                                'type':COLLECTIONJSON,
                                'rel': "artists-all"}
                               ]
        links['artist'] = {'href':api.url_for(Artist, artist=artist),
							   'profile': ARTIST_PROFILE,
							   'type': "" ,
                               'rel': "artist"}


        #Fill the template
        envelope['template'] = {
        "data" : [
            {"prompt" : "", "name" : "name", "value" : "", "required":True},
            {"prompt" : "", "name" : "byArtist", "value" : "", "required":False},
            {"prompt" : "", "name" : "datePublished", "value" : "", "required":False},
            {"prompt" : "", "name" : "duration", "value" : "", "required":False},
            {"prompt" : "", "name" : "sid", "value" : "", "required":False},

            ]
        }

        #Fill the rest of properties
        envelope['name'] = song_db['name']
        envelope['byArtist'] = song_db['byArtist']
        envelope['datePublished'] = song_db['datePublished']
        envelope['duration'] = song_db['duration']
        envelope['sid'] = song_db['sid']


        #RENDER
        return Response (json.dumps(envelope), 200, mimetype=HAL+";"+ SONG_PROFILE)

    def delete(self, artist, title):

        if g.db.delete_song(artist, title):
            return '', 204
        else:

            return create_error_response(404, "Unknown song",
                                         "There is no songs with title %s" % title,
                                         "Song")


class Playlist(Resource):

    def get(self, nickname, title):
        pl_db = g.db.get_playlist(title, nickname)
        if not pl_db:
            return create_error_response(404, "Unknown playlist",
                                         "There is no playlist called %s" % title,
                                         "Playlist")
        #FILTER AND GENERATE RESPONSE
        #Create the envelope:
        envelope = {}
        #Now create the links
        links = {}
        envelope["_links"] = links

        #Fill the links
        _curies = [
            {
            "name": "playlist",
            "href": PLAYLIST_PROFILE,
            },
            {
            "name": "atom-thread",
            "href": ATOM_THREAD_PROFILE
            }
        ]
        links['curies'] = _curies
        links['self'] = {'href':api.url_for(Playlist, nickname=nickname, title=title),
                         'profile': PLAYLIST_PROFILE}
        links['collection'] = {'href':api.url_for(User_playlists, nickname=nickname),
                               'profile': PLAYLIST_PROFILE,
                               'type':COLLECTIONJSON}

        #Fill the template
        envelope['template'] = {
        "data" : [
            {"prompt" : "", "name" : "name", "value" : "", "required":True},
            {"prompt" : "", "name" : "author", "value" : "", "required":True},
            {"prompt" : "", "name" : "created_on", "value" : "", "required":False}
        ]
        }

        #Fill the rest of properties
        envelope['name'] = pl_db['name']
        envelope['author'] = pl_db['author']
        envelope['created_on'] = pl_db['created_on']

        #RENDER
        return Response (json.dumps(envelope), 200, mimetype=HAL+";"+ PLAYLIST_PROFILE)

    def post(self, nickname, title):
        input = request.get_json(force=True)
        if not input:
            return create_error_response(415, "Unsupported Media Type",
                                         "Use a JSON compatible format",
                                         "Playlist")

        #It throws a BadRequest exception, and hence a 400 code if the JSON is
        #not wellformed
        try:
            data = input['template']['data']

            dictionary = {}
            for d in data:
                tt = d['name']
                dictionary[tt] = d['value']



            #CHECK THAT DATA RECEIVED IS CORRECT
            if not dictionary.get("byArtist", "None") or not dictionary.get('name',"None"):
                return create_error_response(400, "Wrong request format",
                                             "Be sure you include song's title and artist",
                                             "Playlist")
        except:
            #This is launched if either title or body does not exist or if
            # the template.data array does not exist.
            return create_error_response(400, "Wrong request format",
                                         "Be sure you include song's title and artist",
                                         "Playlist")
        song = g.db.get_song(dictionary.get("byArtist"),dictionary.get("name"))
        if not song:
            abort(500)

        sid = song['sid']
        print sid

        aid = g.db.append_song_to_playlist(sid, title, nickname)
        if not aid:
            abort(500)

        url = api.url_for(Playlist, nickname=nickname, title=title)

        #RENDER
        #Return the response
        return Response(status=201, headers={'Location':url})



    def delete(self, nickname, title):

        #PERFORM DELETE OPERATIONS
        if g.db.delete_playlist(nickname, title):
            return '', 204
        else:
            return create_error_response(404, "Unknown playlist",
                                         "There is no playlist titled %s" % title,
                                         "Playlist")

    def put(self, nickname, title):

        if not g.db.contains_playlist(nickname, title):
            raise NotFound()

        input = request.get_json(force=True)
        # using JSON
        if not input:
            return create_error_response(415, "Unsupported Media Type",
                                         "Use a JSON compatible format",
                                         "Playlist")

        #It throws a BadRequest exception, and hence a 400 code if the JSON is
        #not wellformed
        try:
            data = input['template']['data']

            dictionary = {}
            for d in data:
                tt = d['name']
                dictionary[tt] = d['value']


            #CHECK THAT DATA RECEIVED IS CORRECT
            if not dictionary.get("name", None) or not dictionary.get("author", None):
             return create_error_response(400, "Wrong request format",
                                         "Be sure you include playlists's title and author",
                                         "Playlist")
        except:
             return create_error_response(400, "Wrong request format",
                                         "Be sure you include playlists's title and author",
                                         "Playlist")
        else:
            if not g.db.modify_playlist(nickname, title, dictionary.get("author"), dictionary.get("name"), dictionary.get("created_on")):
                return NotFound()
            return '', 204

class Playlist_songs(Resource):

    def get(self, title, nickname):

        songs = g.db.get_songs_in_playlist(title, nickname)

        envelope = {}
        collection = {}
        envelope["collection"] = collection
        collection['version'] = "1.0"
        collection['href'] = api.url_for(Playlist_songs, nickname=nickname, title=title)
        collection['template'] = {
        "data" : [
            {"prompt" : "", "name" : "name", "value" : "", "required":True},
            {"prompt" : "", "name" : "byArtist", "value" : "", "required":True},
            {"prompt" : "", "name" : "duration", "value" : "", "required":False},
            {"prompt" : "", "name" : "datePublished", "value" : "", "required":False},

            ]
        }
        #Create the items
        items = []
        for a in songs:
            _artist = a['byArtist']
            _title = a['name']
            _length = a['duration']
            _year = a['datePublished']
            _url = api.url_for(Song, artist=a['byArtist'], title=_title)
            song = {}
            song['href'] = _url
            song['data'] = []

            ss = [('name',_title), ('byArtist', _artist), ('duration',_length), ('datePublished',_year)]
            for s in ss:
                value = {'name': s[0], 'value': s[1]}
                song['data'].append(value)

            song['links'] = []
            items.append(song)
        collection['items'] = items

        return envelope

class Users(Resource):

    def get(self):
        users_db = g.db.get_users()

        #FILTER AND GENERATE THE RESPONSE
        #Create the envelope
        envelope = {}
        collection = {}
        envelope["collection"] = collection
        collection['version'] = "1.0"
        collection['href'] = api.url_for(Users)
        collection['links'] = [{'prompt':'List of all artists in the Finder',
                                'rel':'artists-all',
                                'href': api.url_for(Artists)}
                               ]
        collection['template'] = {
        "data" : [
            {"prompt" : "Insert nickname", "name" : "nickname",
             "value" : "", "required":True},
            {"prompt" : "Insert password", "name" : "password",
             "object" : {}, "required":False},
            {"prompt" : "Insert user gender", "name" : "gender",
             "value" : "", "required":False},
            {"prompt" : "Insert user country", "name" : "nationality",
             "value" : "", "required":False},
            {"prompt" : "Insert user age", "name" : "age",
             "value" : "", "required":False}

        ]
        }
        #Create the items
        items = []
        for user in users_db:
            print user
            _nickname = user['nickname']
            _gender = user['gender']
            _country = user['nationality']
            _age = user['age']

            _url = api.url_for(User, nickname=_nickname)
            _playlist_url = api.url_for(User_playlists, nickname=_nickname)
            user = {}
            user['href'] = _url
            user['read-only'] = True
            user['data'] = []

            ss = [('nickname',_nickname), ('gender', _gender), ('nationality',_country), ('age',_age)]
            for s in ss:
                value = {'name': s[0], 'value': s[1]}
                user['data'].append(value)

            user['links'] = [{
                             'href':_playlist_url,
                             'rel':"playlists",
                             'name':"playlists",
                             'prompt':"Playlists of user"
                             }]
            items.append(user)
        collection['items'] = items
        #RENDER
        return envelope

    def post(self):
        input = request.get_json(force=True)
        if not input:
            return create_error_response(415, "Unsupported Media Type",
                                         "Use a JSON compatible format",
                                         "Users")

        try:
            data = input['template']['data']

            dictionary = {}
            for d in data:
                tt = d['name']
                dictionary[tt] = d['value']


            #CHECK THAT DATA RECEIVED IS CORRECT
            if not dictionary.get("nickname", None) or not dictionary.get("password", None):
                return create_error_response(400, "Wrong request format",
                                             "Be sure you include user's nickname and password",
                                             "Users")
        except:
            return create_error_response(400, "Wrong request format",
                                         "Be sure you include user's nickname and password",
                                         "Users")

        #aid = g.db.create_user(nickname, password, age=None, country=None, gender=None)
        aid = g.db.create_user(dictionary.get("nickname"), dictionary.get("password"), dictionary.get("age", None), dictionary.get("nationality", None), dictionary.get("gender", None))
        if not aid:
            abort(500)

        url = api.url_for(User, nickname=dictionary.get("nickname"))


        #RENDER
        #Return the response
        return Response(status=201, headers={'Location':url})


class User(Resource):

    def get(self, nickname):
        user_db = g.db.get_user(nickname, request.args.get('password'))
        if not user_db:
            return create_error_response(404, "Unknown user",
                                         "There is no user named %s" % nickname,
                                         "User")
        #FILTER AND GENERATE RESPONSE
        #Create the envelope:
        envelope = {}
        #Now create the links
        links = {}
        envelope["_links"] = links

        #Fill the links
        _curies = [
            {
            "name": "user",
            "href": USER_PROFILE,
            },
            {
            "name": "atom-thread",
            "href": ATOM_THREAD_PROFILE
            }
        ]
        links['curies'] = _curies
        links['self'] = {'href':api.url_for(User, nickname=nickname),
                         'profile': USER_PROFILE}
        links['collection'] = [{'href':api.url_for(Users),
                               'profile': USER_PROFILE,
                               'type':COLLECTIONJSON,
                               'rel': "users-all"},
                               {'href':api.url_for(User_playlists, nickname=nickname),
                               'profile': PLAYLIST_PROFILE,
                               'type':COLLECTIONJSON,
                               'rel': "playlists-all"}
                               ]

        #Fill the template
        envelope['template'] = {
        "data" : [
            {"prompt" : "", "name" : "nickname", "value" : "", "required":True},
            {"prompt" : "", "name" : "gender", "value" : "", "required":False},
            {"prompt" : "", "name" : "nationality", "value" : "", "required":False},
            {"prompt" : "", "name" : "age", "value" : "", "required":False}
        ]
        }

        #Fill the rest of properties
        envelope['nickname'] = user_db['nickname']
        envelope['gender'] = user_db['gender']
        envelope['nationality'] = user_db['nationality']
        envelope['age'] = user_db['age']

        #RENDER
        return Response (json.dumps(envelope), 200, mimetype=HAL+";"+ USER_PROFILE)

    def delete(self, nickname):
        if g.db.delete_user(nickname):
            return '', 204
        else:
            #Send error message
            return create_error_response(404, "Unknown user",
                                         "There is no user with nickname %s" % nickname,
                                         "User")

    def put(self, nickname):

        input = request.get_json(force=True)
        if not input:
            return create_error_response(415, "Unsupported Media Type",
                                         "Use a JSON compatible format",
                                         "User")


        #It throws a BadRequest exception, and hence a 400 code if the JSON is
        #not wellformed
        try:
            data = input['template']['data']
            dictionary = {}
            for d in data:
                tt = d['name']
                dictionary[tt] = d['value']

        except:
             return create_error_response(400, "Wrong request format",
                                         "Be sure you include playlists's title and author",
                                         "Playlist")
        else:
            if not g.db.modify_user(nickname, dictionary.get("age", None), dictionary.get("nationality", None), dictionary.get("gender", None)):
                return NotFound()
            return '', 204

class User_playlists(Resource):

    def get(self, nickname):
        pl_db = g.db.get_playlists(nickname)

        envelope = {}
        collection = {}
        envelope["collection"] = collection
        collection['version'] = "1.0"
        collection['href'] = api.url_for(User_playlists, nickname=nickname)
        collection['template'] = {
        "data" : [
            {"prompt" : "", "name" : "name", "value" : "", "required":True},
            {"prompt" : "", "name" : "author", "value" : "", "required":True},
            {"prompt" : "", "name" : "created_on", "value" : "", "required":False}
        ]
        }
        #Create the items
        items = []
        for a in pl_db:
            _title = a['name']
            _user = a['author']
            _created_on = a['created_on']
            _url = api.url_for(Playlist, nickname=_user, title=_title)
            pl = {}
            pl['href'] = _url
            pl['data'] = []

            ss = [('name',_title), ('author', _user), ('created_on',_created_on)]
            for s in ss:
                value = {'name': s[0], 'value': s[1]}
                pl['data'].append(value)

            pl['links'] = []
            items.append(pl)

        collection['items'] = items
        return envelope

    def post(self, nickname):

        #creates a playlist for the user
        input = request.get_json(force=True)
        if not input:
            return create_error_response(415, "Unsupported Media Type",
                                         "Use a JSON compatible format",
                                         "User")


        try:
            data = input['template']['data']
            name = None
            for d in data:
                #This code has a bad performance. We write it like this for
                #simplicity. Another alternative should be used instead.
                if d['name'] == 'name':
                    name = d['value']
                #CHECK THAT DATA RECEIVED IS CORRECT
                if not name or not nickname:
                    return create_error_response(400, "Wrong request format",
                                                 "Be sure you include playlist's title and owner",
                                                 "User")
        except:
            #This is launched if either title or body does not exist or if
            # the template.data array does not exist.
            return create_error_response(400, "Wrong request format",
                                         "Be sure you include playlist's title and owner",
                                         "User")

        plid = g.db.create_playlist(name, nickname)
        if not plid:
            abort(500)

        url = api.url_for(Playlist, nickname=nickname, title=name)

        #RENDER
        #Return the response
        return Response(status=201, headers={'Location':url})





api.add_resource(Artists, '/musicfinder/api/artists/',
                 endpoint='artists')
api.add_resource(Artist, '/musicfinder/api/artists/<artist>/',
                 endpoint='artist')
api.add_resource(Songs, '/musicfinder/api/artists/<artist>/songs/',
                 endpoint='songs')
api.add_resource(Song, '/musicfinder/api/artists/<artist>/songs/<title>',
                 endpoint='song')
api.add_resource(Users, '/musicfinder/api/users/',
                 endpoint='users')
api.add_resource(User, '/musicfinder/api/users/<nickname>/',
                 endpoint='user')
api.add_resource(User_playlists, '/musicfinder/api/users/<nickname>/playlists/',
                 endpoint='playlists')
api.add_resource(Playlist, '/musicfinder/api/users/<nickname>/playlists/<title>/',
                 endpoint='playlist')
api.add_resource(Playlist_songs, '/musicfinder/api/users/<nickname>/playlists/<title>/songs/',
                 endpoint='playlist_songs')

#Start the application
#DATABASE SHOULD HAVE BEEN POPULATED PREVIOUSLY
if __name__ == '__main__':
    app.run(debug=True)
				 

