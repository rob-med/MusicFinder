from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware
from resources import app as musicfinder
from musicfinder_admin.application import app as musicfinder_admin

application = DispatcherMiddleware(musicfinder, {
     '/musicfinder_admin': musicfinder_admin
})
if __name__ == '__main__':
    run_simple('localhost', 5000, application,
               use_reloader=True, use_debugger=True, use_evalex=True)