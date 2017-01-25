 #!/usr/bin/env python

import tornado.web

class SafetyAnalysisHandler(tornado.web.RequestHandler):
    """
    @api {post} /safetyAnalysis/ Safety Analysis
    @apiName SafetyAnalysis
    @apiVersion 0.0.0
    @apiGroup Analysis
    @apiDescription Calling this route will perform safety analysis on a project that object tracking has already been run on. When the analysis is done, an email will be sent to the project's user. (Due to the potentially long run duration, it is infeasible to return the results as a response to the HTTP request. In order to check the status of the testing and view results, see the Status group of messages.)

    @apiParam {String} identifier The identifier of the project on which to run safety analysis.
    @apiParam {String} email The email address that should be notified when the safety analysis is complete

    @apiSuccess status_code The API will return a status code of 200 upon success.

    @apiError error_message The error message to display. (Will return unique error message if object tracking has NOT been run on specified project)
    """
    def post(self):
        self.finish("Safety Analysis")
