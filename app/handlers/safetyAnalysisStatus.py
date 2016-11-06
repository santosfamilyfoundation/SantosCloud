#!/usr/bin/env python

import tornado.escape
import tornado.web
from utils.statusHelper import sharedStatusHelper

class SafetyAnalysisStatusHandler(tornado.web.RequestHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        self.finish(sharedStatusHelper.get_status(data['videoId']))
