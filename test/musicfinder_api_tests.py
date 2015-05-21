import unittest, copy
import json

import flask

import resources as resources
import database

db_path ='db/db_test.db'
db = database.MusicDatabase(db_path)
initial_artitsts = 20
initial_users = 3
resources.app.config['TESTING'] = True
resources.app.config['DATABASE'] = db
class ResourcesAPITestCase(unittest.TestCase):
   
    def setUp(self):
        db.load_init_values()
        self.client = resources.app.test_client()

    def tearDown(self):
        db.clean()

class ArtistsTestCase (ResourcesAPITestCase):
   
    url = '/musicfinder/api/artists/'
    
    @classmethod
    def setUpClass(cls):
        print 'Testing AtistsTestCase'
    
    def test_url(self):
        '''
        Checks that the URL points to the right resource
        '''
        #NOTE: self.shortDescription() shuould work.
        print '('+self.test_url.__name__+')', self.test_url.__doc__, 
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Artists)
    
    def test_get_artists(self):
        '''
        Checks that GET Artists return correct status code and data format
        '''
        print '('+self.test_get_artists.__name__+')', self.test_get_artists.__doc__
        with resources.app.test_client() as client:
            resp = client.get(self.url)
            self.assertEquals(resp.status_code,200)
            data = json.loads(resp.data)
            template = data['collection']['template']
            template_data = template['data']
            # link = data['links']
            self.assertEquals(template_data[0]['name'],'name')
            self.assertEquals(template_data[1]['name'],'country')
            self.assertEquals(template_data[2]['name'],'genre')
            self.assertEquals(template_data[3]['name'],'language')
            self.assertEquals(template_data[4]['name'],'formed_in')
            # self.assertEquals(link[0]['rel'],'related')
            # self.assertEquals(link[0]['href'],resources.api.url_for(resources.Users))
            artists = data['collection']['items']
            self.assertEquals(len(artists),initial_artitsts)
            #Just check one artist the rest are constructed in the same way
            artist0 =artists [0]['data'][0] # collection -> items -> data -> name
            self.assertIn('name',artist0)
            href = data['collection']['href']
            #The collection contains a url to a message
            self.assertIn(resources.api.url_for(resources.Artists),href)

class UsersTestCase (ResourcesAPITestCase):
   
    url = '/musicfinder/api/users/'
    
    @classmethod
    def setUpClass(cls):
        print 'Testing UsersTestCase'
    
    def test_url(self):
        '''
        Checks that the URL points to the right resource
        '''
        #NOTE: self.shortDescription() shuould work.
        print '('+self.test_url.__name__+')', self.test_url.__doc__, 
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Users)
    
    def test_get_users(self):
        '''
        Checks that GET users return correct status code and data format
        '''
        print '('+self.test_get_users.__name__+')', self.test_get_users.__doc__
        #I use this because I need the app context to use the api.url_for
        with resources.app.test_client() as client:
            resp = client.get(self.url)
            self.assertEquals(resp.status_code,200)
            data = json.loads(resp.data)
            link = data['collection']['links']
            self.assertEquals(link[0]['prompt'],'List of all artists in the Finder')
            self.assertEquals(link[0]['rel'],'artists-all')
            self.assertEquals(link[0]['href'],resources.api.url_for(resources.Artists))
            users = data['collection']['items']
            self.assertEquals(len(users),initial_users)
            #Just check one users the rest are constructed in the same way
            users0_data = users[0]['data'][0]
            self.assertIn('nickname',users0_data['name'])
            users0_links = users[0]
            self.assertIn('links',users0_links)
            link0 = users0_links['links'][0]
            for attr in ('prompt','rel','href'):
                self.assertIn(attr,link0)
            #The link contains a url to a user
            self.assertIn(resources.api.url_for(resources.User, nickname=users0_data['value']), link0['href'])

class ArtistTestCase (ResourcesAPITestCase):
    
    url = '/musicfinder/api/artists/Placebo/'
    url_wrong = '/forum/api/messages/PlaceboXYZ/'
    artist1 = 'Test'
    artist2 = 'Elio'
    url1 = '/musicfinder/api/artists/%s/'% artist1
    url2 = '/musicfinder/api/artists/'
    artist = {"template":{"data":[{"name":"name","value":"Elio"},{"name":"country","value":"England"},{"name":"language","value":"english"},{"name":"genre","value":"rock"},
                {"name":"formed_in","value":1996}]}}
    artist_1_request_wrong = {"template":{"data":[{"name":"language","value":"english"},{"name":"genre","value":"rock"}]}}
 
    @classmethod
    def setUpClass(cls):
        print 'Testing ArtistTestCase'
    
    
    def test_url(self):
        '''
        Checks that the URL points to the right resource
        '''
        #NOTE: self.shortDescription() shuould work.
        print '('+self.test_url.__name__+')', self.test_url.__doc__
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Artist)
    
    def test_wrong_url(self):
        '''
        Checks that GET Artist return correct status code if given a wrong message
        '''
        resp = self.client.get(self.url_wrong)
        self.assertEquals(resp.status_code, 404)
    
    def test_get_message(self):
        '''
        Checks that GET Artist return correct status code and data format
        '''
        print '('+self.test_get_message.__name__+')', self.test_get_message.__doc__
        with resources.app.test_client() as client:
            resp = client.get(self.url)
            self.assertEquals(resp.status_code ,200)
            data = json.loads(resp.data)
            #The data is formed by links and message
            links = data['_links']
            #message = data ['message']

            #Check that the link format is correct
            self.assertEquals(len(links), 3)
            # link0 = links[0]
            # self.assertEquals(link0['title'],'messages')
            # self.assertEquals(link0['rel'],'collection')
            # self.assertEquals(link0['href'], resources.api.url_for(resources.Messages))
            
            #Check that the artist contains all required attributes
            for attribute in ('name', 'language', 'country', 'genre'):
                self.assertIn(attribute, data)

            #Check that the sender format is correct
            # sender = message['sender']
            # for attribute in ('href','rel','title'):
            #     self.assertIn(attribute, sender)
            
            #Check that we provide the correct user
            # self.assertEquals(resources.api.url_for(resources.Artist, nickname=sender['title']), sender['href'])

    def test_add_artist(self):
        '''
        Checks that the artist is added correctly

        '''
        print '('+self.test_add_artist.__name__+')', self.test_add_artist.__doc__
        resp = self.client.post(self.url2, data=json.dumps(self.artist), headers={"Content-Type":"application/json"})
        #print resp.data
        self.assertEquals(resp.status_code, 201)
        self.assertIn('Location', resp.headers)
        resp2 = self.client.get(self.url2)
        self.assertEquals(resp2.status_code, 200)

    def test_add_reply_wrong_artist(self):
        '''
        Try to add an artist sending wrong data
        '''
        print '('+self.test_add_reply_wrong_artist.__name__+')', self.test_add_reply_wrong_artist.__doc__
        resp = self.client.post(self.url2, data=json.dumps(self.artist_1_request_wrong), headers={"Content-Type":"application/json"})
        self.assertEquals(resp.status_code, 400)

    def test_add_reply_unexisting_artist(self):
        '''
        Try to add a reply to an unexisting artist
        '''
        print '('+self.test_add_reply_unexisting_artist.__name__+')', self.test_add_reply_unexisting_artist.__doc__
        resp = self.client.post(self.url_wrong, data=json.dumps(self.artist_1_request_wrong), headers={"Content-Type":"application/json"})
        self.assertEquals(resp.status_code, 404)


class UserTestCase (ResourcesAPITestCase):
    user1 = 'Test'
    user2 = 'Clayton'
    url1 = '/musicfinder/api/users/%s/'% user1
    url2 = '/musicfinder/api/users/%s/'% user2
    url_wrong = '/musicfinder/api/users/unknown/'

    @classmethod
    def setUpClass(cls):
        print 'Testing UserTestCase'

    def setUp(self):
        super(UserTestCase,self).setUp()
        self.url = '/musicfinder/api/users/'
        self.user = {"template":{"data":[{"name":"nickname","value":"Clayton"},{"name":"password","value":"frank"},{"name":"age","value":30},{"name":"country","value":"England"},
                {"name":"gender","value":"Male"}]}}

    def test_url(self):
        '''
        Checks that the URL points to the right resource
        '''
        #NOTE: self.shortDescription() shuould work.
        print '('+self.test_url.__name__+')', self.test_url.__doc__
        with resources.app.test_request_context(self.url1):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.User)
    
    def test_wrong_url(self):
        '''
        Checks that GET User return correct status code if given a wrong message
        '''
        print '('+self.test_wrong_url.__name__+')', self.test_wrong_url.__doc__
        resp = self.client.get(self.url_wrong)
        self.assertEquals(resp.status_code, 404)

    def test_get_format(self):
        '''
        Checks that the format of user is correct

        '''
        print '('+self.test_get_format.__name__+')', self.test_get_format.__doc__
        resp = self.client.get(self.url2)
        data = json.loads(resp.data)
        self.assertIn('_links', data)
        self.assertIn('nickname', data)
        self.assertIn('country', data)
        self.assertIn('gender', data)
        self.assertIn('age', data)
        #Check that user has public_profile, restricted_profile, history
        for attribute in ('curies', 'self', 'collection'):
            self.assertIn(attribute, data['_links'])

    def test_add_user(self):
        '''
        Checks that the user is added correctly

        '''
        print '('+self.test_add_user.__name__+')', self.test_add_user.__doc__
        resp = self.client.put(self.url2, data=json.dumps(self.user), headers={"Content-Type":"application/json"})
        #print resp.data
        self.assertEquals(resp.status_code, 204) 
        #self.assertIn('Location', resp.headers)
        resp2 = self.client.get(self.url2)
        self.assertEquals(resp2.status_code, 200)    

    
    # def test_add_user_missing_mandatory(self):
    #     '''
    #     Test that it returns error when is missing a mandatory data 
    #     '''
    #     print '('+self.test_add_user_missing_mandatory.__name__+')', self.test_add_user_missing_mandatory.__doc__
    #     mandatory = ['nickname', 'age', 'country', 'gender']
    #     #Iterate through all the attributes from the list, remove one of them in 
    #     #each iteration. Be sure that always return status code 400
    #     for attribute in mandatory:
	   #      for i in [2]:
	   #          user = copy.deepcopy(self.user)
	   #          del user['template']['data'][i]
	   #          print "*********************************************"
	   #          print user
	   #          resp = self.client.put(self.url2, data=json.dumps(user), headers={"Content-Type":"application/json"})
	   #          self.assertEquals(resp.status_code, 400)
      
    # def test_add_existing_user(self):
    #     '''
    #     Testign that trying to add an existing user will fail

    #     '''
    #     print '('+self.test_add_existing_user.__name__+')', self.test_add_existing_user.__doc__
    #     resp = self.client.put(self.url2, data=json.dumps(self.user), headers={"Content-Type":"application/json"})
    #     self.assertEquals(resp.status_code, 409)

class PlaylistTestCase (ResourcesAPITestCase):
   
    url = '/musicfinder/api/users/Robi/playlists/Posted/'
    links_number = 3
    template_data_number = 3
#     url_nickname = 'AxelW'
#     url2 = '/forum/api/users/Mystery/history/'
#     messages2_number = 2
#     url3 = '/forum/api/users/AxelW/history/?length=1'
#     messages3_number = 1

#     url4 =  '/forum/api/users/AxelW/history/?after=1362317481'
#     messages4_number = 1
#     url5 =  '/forum/api/users/AxelW/history/?before=1362317481'
#     messages5_number = 1
#     url6 = '/forum/api/users/AxelW/history/?before=1362317481&after=1362217481'
  

 
    
    @classmethod
    def setUpClass(cls):
        print 'Testing PlaylistTestCase'
    
    def test_url(self):
        '''
        Checks that the URL points to the right resource
        '''
        #NOTE: self.shortDescription() shuould work.
        print '('+self.test_url.__name__+')', self.test_url.__doc__, 
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Playlist)
    
    def test_get_playlist_number_values(self):
        '''
        Checks that GET playlist return correct status code and number of values
        '''
        print '('+self.test_get_playlist_number_values.__name__+')', self.test_get_playlist_number_values.__doc__
        with resources.app.test_client() as client:
            resp = client.get(self.url)
            self.assertEquals(resp.status_code,200)
            data = json.loads(resp.data)
            self.assertIn('created_on',data)
            self.assertIn('_links',data)
            self.assertIn('name',data)
            self.assertIn('template',data)
            self.assertIn('user',data)
            links = data['_links']
            template_data = data['template']['data']
            self.assertEquals(len(links),self.links_number)
            self.assertEquals(len(template_data),self.template_data_number)

            
    
#     def test_get_history_timestamp_values(self):
#         '''
#         Checks that GET history return correct status code and format
#         '''
#         print '('+self.test_get_history_timestamp_values.__name__+')', self.test_get_history_timestamp_values.__doc__
#         #I use this because I need the app context to use the api.url_for
#         with resources.app.test_client() as client:
#             resp = client.get(self.url4)
#             self.assertEquals(resp.status_code,200)
#             data = json.loads(resp.data)
#             self.assertIn('messages',data)
#             messages = data['messages']
#             self.assertEquals(len(messages),self.messages4_number)

#             resp = client.get(self.url5)
#             self.assertEquals(resp.status_code,200)
#             data = json.loads(resp.data)
#             self.assertIn('messages',data)
#             messages = data['messages']
#             self.assertEquals(len(messages),self.messages5_number)

#             resp = client.get(self.url6)
#             self.assertEquals(resp.status_code,404)

    
#     def test_get_history(self):
#         '''
#         Checks that GET history return correct status code and number of values
#         '''
#         print '('+self.test_get_history.__name__+')', self.test_get_history.__doc__
#         #I use this because I need the app context to use the api.url_for
#         with resources.app.test_client() as client:
#             resp = client.get(self.url)
#             self.assertEquals(resp.status_code,200)
#             data = json.loads(resp.data)
#             link = data['links']
#             self.assertEquals(link[0]['title'],'user')
#             self.assertEquals(link[0]['rel'],'parent')
#             self.assertEquals(link[0]['href'],resources.api.url_for(resources.User,nickname=self.url_nickname))
#             self.assertEquals(link[1]['title'],'public profile')
#             self.assertEquals(link[1]['rel'],'related')
#             self.assertEquals(link[1]['href'],resources.api.url_for(resources.User_public,nickname=self.url_nickname))
#             self.assertEquals(link[2]['title'],'users')
#             self.assertEquals(link[2]['rel'],'collection')
#             self.assertEquals(link[2]['href'],resources.api.url_for(resources.Users))
#             messages = data['messages']
            
#             #Just check one message the rest are constructed in the same way
#             message0 = messages [0]
#             link0 = message0['link']
#             self.assertIn('title',link0)
#             self.assertIn('href',link0)
#             self.assertIn('rel',link0)

if __name__ == '__main__':
    print 'Start running tests'
    unittest.main()