#!/usr/bin/env python

import tornado.web
import os
import uuid

class TrajectoryAnalysisHandler(tornado.web.RequestHandler):
    def post(self):
        self.finish("Trajectory analysis")
