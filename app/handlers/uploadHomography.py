#!/usr/bin/env python

import tornado.web
import os
from trafficcloud.app_config import get_project_path

class UploadHomographyHandler(tornado.web.RequestHandler):
    """
    @api {post} /uploadHomography/ Upload Homography
    @apiName UploadHomography
    @apiVersion 0.1.0
    @apiGroup Upload
    @apiDescription Use this route to upload homography files for a project.

    @apiParam {String} identifier The identifier of the project to upload files to.
    @apiParam {File} aerial An aerial photo of the intersection.
    @apiParam {File} camera A screenshot of the intersection from the video.
    @apiParam {File} homography The homography text file to use.

    @apiSuccess status_code The API will return a status code of 200 upon success.

    @apiError error_message The error message to display.
    """
    def initialize(self):
        self.identifier = None
        self.files = {}

    def post(self):
        self.files = self.request.files
        self.identifier = self.get_body_argument('identifier')
        self.write_homography_files()
        self.finish("Upload Homography")
        
    def write_homography_files(self):
        project_dir = get_project_path(self.identifier)
        for key,value in self.files.iteritems():
            with open(os.path.join(project_dir,'homography',value[0]['filename']), 'wb') as f:
                f.write(value[0]['body'])
