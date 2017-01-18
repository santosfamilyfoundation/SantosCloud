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
    @apiDescription This route will analyze the provided video, and return the project identifier.

    @apiParam {String} email The email to notify when analysis is done.
    @apiParam {File} homography/aerialpng An aerial photo of the intersection.
    @apiParam {File} homography/camerapng A screenshot of the intersection from the video.
    @apiParam {File} homography/homographytxt The homography text file to use.
    @apiParam {File} project_namecfg The project name configuration file.
    @apiParam {File} trackingcfg The tracking configuration file.
    @apiParam {File} temp/test/test_object/object_trackingcfg The object tracking configuration file.
    @apiParam {File} temp/test/test_feature/feature_trackingcfg The feature tracking configuration file.
    @apiParam {File} video The video file to analyze. This can have any file extension.

    @apiSuccess {String} project_identifier The project identifier. This will be used to reference the project in all other requests.
    """
    def post(self):
        name_body_dict = self.parse_request(self.request.files)
        project_identifier = api.saveFiles(name_body_dict)

        api.runTrajectoryAnalysis(project_identifier)

        d = {'project_identifier': project_identifier}
        self.write(d)

    def get(self):
        self.render("upload.html")
