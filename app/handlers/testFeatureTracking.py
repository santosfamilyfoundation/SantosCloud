#!/usr/bin/env python

import tornado.web
import os
import uuid

class TestFeatureTrackingHandler(tornado.web.RequestHandler):
    def post(self):
        self.finish("Test feature tracking")
