#!/usr/bin/env python
import os
import subprocess
import shutil

import tornado.web

from traffic_cloud_utils.app_config import get_project_path, get_project_video_path, update_config_without_sections, get_config_without_sections
import pm
import video
from traffic_cloud_utils.emailHelper import EmailHelper

class AnalysisHandler(tornado.web.RequestHandler):
    """
    @api {post} /analysis/ Analysis
    @apiName Analysis
    @apiVersion 0.0.0
    @apiGroup Analysis
    @apiDescription Calling this route will perform analysis on the video. When the analysis is done, an email will be sent to the project's user. This test consists of running object tracking on the video, and then running safety analysis on the results of the object tracking. When the analysis is complete, the system will produce a safety report for the intersection. (Due to the potentially long duration of testing, it is infeasible to return the results as a response to the HTTP request. In order to check the status of the testing and view results, see the Status group of messages.)

    @apiParam {String} identifier The identifier of the project to test configuration of.
    @apiParam {String} email The email address that should be notified when the analysis is complete.

    @apiSuccess status_code The API will return a status code of 200 upon success.

    @apiError error_message The error message to display.
    """
    def post(self):
        identifier = self.request.body_arguments["identifier"]

        self.objectTrack(identifier)
        self.safetyAnalysis(identifier)

        message = "Hello,\n\tWe have finished processing your video and identifying any dangerous interactions.\nThank you for your patience,\nThe Santos Team"
        subject = "Your video has finished processing."

        EmailHelper.send_email(self.request.body_arguments["email"], subject, message)

        self.finish("Analysis")

    def safetyAnalysis(self, identifier, prediction_method=None):

        project_path = get_project_path(identifier)

        config_path = os.path.join(project_path, "run", "run_tracking.cfg")
        db_path = os.path.join(project_path, "run", "results.sqlite")
        update_dict = {
            'video-filename': get_project_video_path(identifier), # use absolute path to video on server
            'database-filename': db_path # use absolute path to database
        }
        update_config_without_sections(config_path, update_dict)

        if prediction_method is None:
            prediction_method = 'cv' # default to the least resource intensive method

        # Predict Interactions between road users and compute safety metrics describing them
        subprocess.call(["safety-analysis.py", "--cfg", config_path, "--prediction-method", prediction_method])


    def objectTrack(self, identifier):
        """
        Runs TrafficIntelligence trackers and support scripts.
        """
        project_path = get_project_path(identifier)

        # create test folder
        if not os.path.exists(os.path.join(project_path, "run")):
            os.mkdir(os.path.join(project_path, "run"))

        tracking_path = os.path.join(project_path, "run", "run_tracking.cfg")

        # removes object tracking.cfg
        if os.path.exists(tracking_path):
            os.remove(tracking_path)

        # creates new config file
        prev_tracking_path = os.path.join(project_path, ".temp", "test", "test_object", "object_tracking.cfg")
        shutil.copyfile(prev_tracking_path, tracking_path)

        update_dict = {'frame1': 0, 
            'nframes': 0, 
            'database-filename': 'results.sqlite', 
            'classifier-filename': os.path.join(project_path, "classifier.cfg"),
            'video-filename': get_project_video_path(identifier),
            'homography-filename': os.path.join(project_path, "homography", "homography.txt")}
        update_config_without_sections(tracking_path, update_dict)

        db_path = os.path.join(project_path, "run", "results.sqlite")

        if os.path.exists(db_path):  # If results database already exists,
            os.remove(db_path)  # then remove it--it'll be recreated.
        subprocess.call(["feature-based-tracking", tracking_path, "--tf", "--database-filename", db_path])
        subprocess.call(["feature-based-tracking", tracking_path, "--gf", "--database-filename", db_path])

        subprocess.call(["classify-objects.py", "--cfg", tracking_path, "-d", db_path])  # Classify road users

        db_make_objtraj(db_path)  # Make our object_trajectories db table

        video.create_tracking_video(project_path, get_project_video_path(identifier))

        