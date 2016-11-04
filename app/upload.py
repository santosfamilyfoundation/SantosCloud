#!/usr/bin/env python

import tornado.web

class UploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")