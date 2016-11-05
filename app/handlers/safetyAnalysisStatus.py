#!/usr/bin/env python

import tornado.web
import os
import uuid

class SafetyAnalysisStatusHandler(tornado.web.RequestHandler):
    def post(self):
        self.finish("Not quite there yet")
