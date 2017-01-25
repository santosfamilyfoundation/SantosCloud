#!/usr/bin/env python

import tornado.web

class UploadHomographyHandler(tornado.web.RequestHandler):
    """
    @api {post} /uploadHomography/ Upload Homography
    @apiName UploadHomography
    @apiVersion 0.0.0
    @apiGroup Upload
    @apiDescription Use this route to upload homography files for a project.

    @apiParam {String} identifier The identifier of the project to upload files to.
    @apiParam {File} homography/aerialpng An aerial photo of the intersection.
    @apiParam {File} homography/camerapng A screenshot of the intersection from the video.
    @apiParam {File} homography/homographytxt The homography text file to use.

    @apiSuccess status_code The API will return a status code of 200 upon success.

    @apiError error_message The error message to display.
    """
    def post(self):
        self.finish("Upload Homography")
