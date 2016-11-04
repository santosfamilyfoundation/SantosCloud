#!/usr/bin/env python

import tornado.web
import os
import uuid

class SafetyAnalysisHandler(tornado.web.RequestHandler):
    def post(self):
        self.finish("Safety analysis")