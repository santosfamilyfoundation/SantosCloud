#!/usr/bin/env python

import tornado.web
import os
import uuid
from trafficcloud import api

class UploadHandler(tornado.web.RequestHandler):
    
    @staticmethod
    def parse_request(files):
        name_body_dict = {}
        for k, v in files.iteritems():
            fileinfo = v[0]
            name_body_dict[k] = fileinfo['body']
        return name_body_dict

    """
    @api {post} /upload/ Upload Video
    @apiName UploadVideo
    @apiGroup Upload

    @apiParam {File} id Users unique ID.

    @apiSuccess {String} firstname Firstname of the User.
    @apiSuccess {String} lastname  Lastname of the User.
    """
    def post(self):
        name_body_dict = self.parse_request(self.request.files)
        project_identifier = api.saveFiles(name_body_dict)

        api.runTrajectoryAnalysis(project_identifier)

        self.finish("Upload successful for project directory {}".format(project_identifier))

    def get(self):
        self.render("upload.html")
