#!/usr/bin/env python

import tornado.web
import os
import uuid

class TestObjectTrackingHandler(tornado.web.RequestHandler):
    def post(self):
        self.finish("Test object tracking")
