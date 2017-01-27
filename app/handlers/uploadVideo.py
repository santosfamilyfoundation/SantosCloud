#!/usr/bin/env python

import tornado.web
from tornado.web import stream_request_body
from tornado.httputil import parse_multipart_form_data
import trafficcloud.api as api

from pprint import pprint
from uuid import uuid4
import os


@stream_request_body
class UploadVideoHandler(tornado.web.RequestHandler):
    """
    @api {post} /uploadVideo/ Upload Video
    @apiName UploadVideo
    @apiVersion 0.0.0
    @apiGroup Upload
    @apiDescription This route will upload a video to a project (and create a new project if an old one is not specified)

    
    @apiParam {File} video The video file to analyze. This can have any file extension.
    @apiParam {String} [identifier] The identifier of the project to update the video of. If no identifier is provided, a new project will be created, and the identifier will be returned in the response.

    @apiSuccess {String} project_identifier The project identifier. This will be used to reference the project in all other requests.

    @apiError error_message The error message to display.
    """
    def initialize(self):
        self.file_name  = str(uuid4().int)
        self.file_path = os.path.realpath(os.path.join('..','.temp',self.file_name))
        print 'Upload Video Initialized @{}'.format(self.file_path)

    def post(self):
        if 'multipart/form-data; boundary=' in self.request.headers['Content-Type']:
            boundary = self.request.headers['Content-Type'][30:]
        else:
            self.finish('Incorrect File Format: Must be of type multipart/form-data')

        files = {}
        arguments = {}
        with open(self.file_path, 'rb') as f:
            try:
                content = f.read()
                parse_multipart_form_data(boundary,content,arguments,files)
            except MemoryError as err:
                raise tornado.web.HTTPError(reason = 'Memory Error: File too large',\
                        status_code = 507)
        if 'identifier' in arguments:
            identifier = arguments['identifier']
        video = files['video'][0]
        vdict = {video['filename']:video['body']}
        project_identifier = api.saveFiles(vdict)
        #TO-DO: Hookup identifier
        #TO-DO: Error checking for correct arguments
        self.finish("Upload Video Finished")

    def prepare(self):
        open(self.file_path, 'wb').close()
        print 'Upload Video Prepared'

    def data_received(self, data):
        with open(self.file_path, 'ab') as f:
            f.write(data)

    def on_finish(self):
        os.remove(self.file_path)
