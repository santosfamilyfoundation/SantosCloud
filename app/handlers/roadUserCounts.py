#!/usr/bin/env python

import tornado.web

class RoadUserCountsHandler(tornado.web.RequestHandler):
    """
    @api {post} /roadUserCounts/ Road User Counts
    @apiName RoadUserCounts
    @apiVersion 0.0.0
    @apiGroup Analysis
    @apiDescription Calling this route will create a road user counts image from a specified project. When the image is created, an email will be sent to the project's user. This route requires running object tracking on the video, and then running safety analysis on the results of the object tracking beforehand. (Due to the potentially long duration, it is infeasible to return the results as a response to the HTTP request. In order to check the status of the testing and view results, see the Status group of messages.)

    @apiParam {String} identifier The identifier of the project to create road user counts for.

    @apiSuccess status_code The API will return a status code of 200 upon success.

    @apiError error_message The error message to display.
    """
    def post(self):
        self.finish("Visualize Road User Counts")
