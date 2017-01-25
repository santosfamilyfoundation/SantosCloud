#!/usr/bin/env python

import tornado.web
from tornado.web import stream_request_body

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
    def initialize():
        self.file_name = 'video.avi'
        self.num_chunks = 0;
        print 'Upload Video Initialized'

    def post(self):
        print 'Filename: {}'.format(self.file_name)
        self.finish("Upload Video Finished")

    def prepare():
        open(self.file_name, 'w').close()
        print 'Upload Video Prepared'

    def data_received(self, data):
        with open(self.file_name, 'wb') as f:
            print('Writing to "{0}"...'.format(self.file_name))
                    f.write(data)
                    self.num_chunks += 1