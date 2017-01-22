#!/usr/bin/env python

import tornado.web

class CreateHightlightVideoHandler(tornado.web.RequestHandler):
    """
    @api {post} /hightlightVideo/ Hightlight Video
    @apiName HighlightVideo
    @apiGroup Analysis
    @apiDescription Calling this route will create a highlight video of dangerous interactions from a specified project. When the video is created, an email will be sent to the project's user. This route requires running object tracking on the video, and then running safety analysis on the results of the object tracking beforehand. (Due to the potentially long duration, it is infeasible to return the results as a response to the HTTP request. In order to check the status of the testing and view results, see the Status group of messages.)

    @apiParam {String} identifier The identifier of the project to create a highlight video for.
    @apiParam {Integer} [ttc_threshold] Threshold for determining whether an interaction is dangerous.
    @apiParam {Integer} [vehicle_only] Flag for specifying only vehicle-vehicle interactions

    @apiSuccess status_code The API will return a status code of 200 upon success.

    @apiError error_message The error message to display.
    """
    def post(self):
        self.finish("Create Highlight Video")
