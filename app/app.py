#!/usr/bin/env python

import logging
import tornado.auth
import tornado.autoreload
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import os

from tornado.options import define, options

# Import all of our custom routes
from handlers.upload import UploadHandler
from handlers.testConfig import TestConfigHandler
from handlers.trajectoryAnalysis import TrajectoryAnalysisHandler
from handlers.safetyAnalysis import SafetyAnalysisHandler

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/upload", UploadHandler),
            (r"/testConfig", TestConfigHandler),
            (r"/analysis", AnalysisHandler),
        ]
        settings = dict(
            cookie_secret=os.environ.get('TRAFFICCLOUD_SECRET_KEY'),
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

def main():
    keys = ['TRAFFICCLOUD_SECRET_KEY', 'TRAFFICCLOUD_EMAIL', 'TRAFFICCLOUD_PASSWORD']
    for key in keys:
        if os.environ.get(key) == None:
            print("Set the "+key+" environment variable")
            return

    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    print('Listening on port '+str(options.port))
    ioloop = tornado.ioloop.IOLoop().instance()
    tornado.autoreload.start(ioloop)
    ioloop.start()

if __name__ == "__main__":
    main()
