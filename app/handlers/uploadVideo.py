#!/usr/bin/env python

import tornado.web

class UploadVideoHandler(tornado.web.RequestHandler):
    """
    @api {post} /uploadVideo/ Upload Video
    @apiName UploadVideo
    @apiGroup Upload
    @apiDescription This route will upload a video to a project (and create a new project if an old one is not specified)

    
    @apiParam {File} video The video file to analyze. This can have any file extension.
    @apiParam {String} [identifier] The identifier of the project to update the video of. If no identifier is provided, a new project will be created, and the identifier will be returned in the response.

    @apiSuccess {String} project_identifier The project identifier. This will be used to reference the project in all other requests.

    @apiError error_message The error message to display.
    """
    def post(self):
        self.finish("Upload Video")
