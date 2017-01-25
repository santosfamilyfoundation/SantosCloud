#!/usr/bin/env python
import os
import subprocess
import shutil

import tornado.web

from app_config import AppConfig as ac
from app_config import update_config_without_sections
import pm
import video

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
        identifier = self.request.identifier

        self.objectTrack(identifier)
        self.safetyAnalysis(identifier)

        self.finish("Analysis")

    def safetyAnalysis(self, identifier, prediction_method=None):

        ac.load_application_config()
        pm.load_project(identifier)

        config_path = os.path.join(ac.CURRENT_PROJECT_PATH, "run", "run_tracking.cfg")
        db_path = os.path.join(ac.CURRENT_PROJECT_PATH, "run", "results.sqlite")
        update_dict = {
            'video-filename': ac.CURRENT_PROJECT_VIDEO_PATH, # use absolute path to video on server
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
        ac.load_application_config()
        pm.load_project(identifier)

        # create test folder
        if not os.path.exists(ac.CURRENT_PROJECT_PATH + "/run"):
            os.mkdir(ac.CURRENT_PROJECT_PATH + "/run")

        tracking_path = os.path.join(ac.CURRENT_PROJECT_PATH, "run", "run_tracking.cfg")

        # removes object tracking.cfg
        if os.path.exists(tracking_path):
            os.remove(tracking_path)

        # creates new config file
        shutil.copyfile(ac.CURRENT_PROJECT_PATH + "/.temp/test/test_object/object_tracking.cfg", tracking_path)

        update_dict = {'frame1': 0, 
            'nframes': 0, 
            'database-filename': 'results.sqlite', 
            'classifier-filename': os.path.join(ac.CURRENT_PROJECT_PATH, "classifier.cfg"),
            'video-filename': ac.CURRENT_PROJECT_VIDEO_PATH,
            'homography-filename': os.path.join(ac.CURRENT_PROJECT_PATH, "homography", "homography.txt")}
        update_config_without_sections(tracking_path, update_dict)

        db_path = os.path.join(ac.CURRENT_PROJECT_PATH, "run", "results.sqlite")

        if os.path.exists(db_path):  # If results database already exists,
            os.remove(db_path)  # then remove it--it'll be recreated.
        subprocess.call(["feature-based-tracking", tracking_path, "--tf", "--database-filename", db_path])
        subprocess.call(["feature-based-tracking", tracking_path, "--gf", "--database-filename", db_path])

        subprocess.call(["classify-objects.py", "--cfg", tracking_path, "-d", db_path])  # Classify road users

        db_make_objtraj(db_path)  # Make our object_trajectories db table

        video.create_tracking_video(ac.CURRENT_PROJECT_PATH, ac.CURRENT_PROJECT_VIDEO_PATH)
