#!/usr/bin/env python
import os
import subprocess
import shutil

import tornado.web

from traffic_cloud_utils.app_config import get_project_path, get_project_video_path, update_config_without_sections, get_config_without_sections
from traffic_cloud_utils.emailHelper import EmailHelper
from objectTracking import ObjectTrackingHandler
from safetyAnalysis import SafetyAnalysisHandler

class AnalysisHandler(tornado.web.RequestHandler):
    """
    @api {post} /analysis/ Analysis
    @apiName Analysis
    @apiVersion 0.1.0
    @apiGroup Analysis
    @apiDescription Calling this route will perform analysis on the video. When the analysis is done, an email will be sent to the project's user. This test consists of running object tracking on the video, and then running safety analysis on the results of the object tracking. When the analysis is complete, the system will produce a safety report for the intersection. (Due to the potentially long duration of testing, it is infeasible to return the results as a response to the HTTP request. In order to check the status of the testing and view results, see the Status group of messages.)

    @apiParam {String} identifier The identifier of the project to test configuration of.
    @apiParam {String} email The email address that should be notified when the analysis is complete.

    @apiSuccess status_code The API will return a status code of 200 upon success.

    @apiError error_message The error message to display.
    """
    def post(self):
        identifier = self.get_body_argument("identifier")
        email = self.get_body_argument("email")
        status_code, reason = AnalysisHandler.handler(identifier, email)

        if status_code == 200:
            self.finish("Analysis")
        else:
            raise tornado.web.HTTPError(reason=reason, status_code=status_code)

    @staticmethod
    def handler(identifier, email):
        project_path = get_project_path(identifier)
        if not os.path.exists(project_path):
           return (500, 'Project directory does not exist. Check your identifier?')

        status_code, reason = ObjectTrackingHandler.handler(identifier, email, AnalysisHandler.object_tracking_callback)
        return (status_code, reason)

    @staticmethod
    def object_tracking_callback(status_code, response_message, email):
        if status_code == 200:
            message = "Hello,\n\tWe have finished processing your video and identifying all objects.\nWe will perform safety analysis now.\nThank you for your patience,\nThe Santos Team"
            subject = "Your video has finished processing."

            EmailHelper.send_email(email, subject, message)

            status_code, reason = SafetyAnalysisHandler.handler(identifier, email, AnalysisHandler.safety_analysis_callback)

        print (status_code, response_message)

    @staticmethod
    def safety_analysis_callback(status_code, response_message, email):
        if status_code == 200:
            subject = "Your video has finished processing."
            message = "Hello,\n\tWe have finished looking through your data and identifying any dangerous interactions.\nThank you for your patience,\nThe Santos Team"

            EmailHelper.send_email(email, subject, message)

        print(status_code, response_message)

