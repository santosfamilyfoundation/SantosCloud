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
from handlers.analysis import AnalysisHandler

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/upload", UploadHandler),
            (r"/uploadVideo", UploadVideoHandler),
            (r"/uploadHomography", UploadHomographyHandler),
            (r"/config", ConfigHandler),
            (r"/testConfig", TestConfigHandler),
            (r"/analysis", AnalysisHandler),
            (r"/objectTracking", ObjectTrackingHandler),
            (r"/safetyAnalysis", SafetyAnalysisHandler),
            (r"/highlightVideo", CreateHighlightVideoHandler),
            (r"/makeReport", MakeReportHandler),
            (r"/roadUserCounts", RoadUserCountsHandler),
            (r"/speedCDF", CreateSpeedCDFHandler),
            (r"/retrieveResults", RetrieveResultsHandler)

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
    keys = ['TRAFFICCLOUD_SECRET_KEY', 'TRAFFICCLOUD_EMAIL', 'TRAFFICCLOUD_EMAIL_PASSWORD']
    for key in keys:
        if os.environ.get(key) == None:
            print("Set the "+key+" environment variable")
            return

    if os.environ.get('TRAFFICCLOUD_SECRET_KEY') == "DefaultSecretKey":
        print('WARNING: You are using the default secret key. This is insecure! Please create a secret key and set it on the TRAFFICCLOUD_SECRET_KEY environment variable.')
    if os.environ.get('TRAFFICCLOUD_EMAIL') == '' or os.environ.get('TRAFFICCLOUD_EMAIL_PASSWORD') == '':
        print("WARNING: Running without email capabilities. Users won't be emailed when their processing completes. To fix this, set the TRAFFICCLOUD_EMAIL and TRAFFICCLOUD_EMAIL_PASSWORD environment variables.")

    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    print('Listening on port '+str(options.port))
    ioloop = tornado.ioloop.IOLoop().instance()
    tornado.autoreload.start(ioloop)
    ioloop.start()

if __name__ == "__main__":
    main()
