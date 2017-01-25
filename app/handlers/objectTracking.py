#!/usr/bin/env python

import tornado.web

class ObjectTrackingHandler(tornado.web.RequestHandler):
    """
    @api {post} /objectTracking/ Object Tracking
    @apiName ObjectTracking
    @apiVersion 0.0.0
    @apiGroup Analysis
    @apiDescription Calling this route will perform object tracking on the video. When the analysis is done, an email will be sent to the project's user. (Due to the potentially long run duration, it is infeasible to return the results as a response to the HTTP request. In order to check the status of the testing and view results, see the Status group of messages.)

    @apiParam {String} identifier The identifier of the project on which to run object tracking.

    @apiSuccess status_code The API will return a status code of 200 upon success.

    @apiError error_message The error message to display.
    """
    def post(self):
        self.finish("Object Tracking")
