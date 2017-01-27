#!/usr/bin/env python
import os
import subprocess
import shutil
import smtplib
from email.mime.text import MIMEText

import tornado.web

from app_config import get_project_path, get_project_video_path, update_config_without_sections, get_config_without_sections
import pm
import video
from traffic_cloud_utils.emailHelper import EmailHelper

class TestConfigHandler(tornado.web.RequestHandler):
    """
    @api {post} /testConfig/ Test Configuration
    @apiName TestConfig
    @apiVersion 0.0.0
    @apiGroup Configuration
    @apiDescription Calling this route will test the video's configuration. When testing is done, an email will be sent to the project's user. This test consists of running object tracking on a small subset of the video, and producing a video showing the results of the tracking. (Due to the potentially long duration of testing, it is infeasible to return the results as a response to the HTTP request. In order to check the status of the testing and view results, see the Status group of messages.)

    @apiParam {String} test_flag Flag to determine whether feature tracking or object tracking will be tested.
    @apiParam {String} identifier The identifier of the project to test configuration of.
    @apiParam {String} email The email address that should be notified when the object tracking is complete.
    @apiParam {Integer} [frame_start] The frame number to start the configuration test at. If no frame_start is provided, the configuration test will start at the beginning of the video.
    @apiParam {Integer} [num_frames] The number of frames to analyze. To keep configuration testing short, this parameter must be less than 200. If no num_frames is provided, a default value of 100 will be used.

    @apiSuccess status_code The API will return a status code of 200 upon success.

    @apiError error_message The error message to display.
    """
    def post(self):

        identifier = self.request.body_arguments["identifier"]
        test_flag = self.request.body_arguments["test_flag"]

        try:
            frame_start = int(self.request.body_arguments["frame_start"])
            num_frames = int(self.request.body_arguments["num_frames"])
        except Exception as e:
            frame_start = 0
            num_frames = 120
            print e

        if test_flag == "feature":
            runConfigTestFeature(identifier, frame_start, num_frames)
        if test_flag == "object":
            runConfigTestObject(identifier, frame_start, num_frames)

        message = "Hello,\n\tWe have finished processing your video and identifying all objects.\nThank you for your patience,\nThe Santos Team"
        subject = "Your video has finished processing."

        EmailHelper.send_email(self.request.body_arguments["email"], subject, message)
        self.finish("Test feature tracking")

    def runConfigTestFeature(self, identifier, frame_start, num_frames):
        pm.load_project(ac.CURRENT_PROJECT_PATH)

        tracking_path = os.path.join(ac.CURRENT_PROJECT_PATH, ".temp", "test", "test_feature", "feature_tracking.cfg")
        db_path = os.path.join(ac.CURRENT_PROJECT_PATH, ".temp", "test", "test_feature", "test1.sqlite")
        if os.path.exists(db_path):
            os.remove(db_path)

        images_folder = "feature_images"
        video.delete_images(images_folder)

        subprocess.call(["feature-based-tracking", tracking_path, "--tf", "--database-filename", db_path])
        subprocess.call(["display-trajectories.py", "-i", ac.CURRENT_PROJECT_VIDEO_PATH, "-d", db_path, "-o", ac.CURRENT_PROJECT_PATH + "/homography/homography.txt", "-t", "feature", "--save-images", "-f", str(frame_start), "--last-frame", str(frame_start+num_frames)])

        video.move_images_to_project_dir_folder(images_folder)

    def runConfigTestObject(self, identifier, frame_start, num_frames):
        pm.load_project(ac.CURRENT_PROJECT_PATH)

        tracking_path = os.path.join(ac.CURRENT_PROJECT_PATH, ".temp", "test", "test_object", "object_tracking.cfg")
        obj_db_path = os.path.join(ac.CURRENT_PROJECT_PATH,".temp", "test", "test_object", "test1.sqlite")
        feat_db_path = os.path.join(ac.CURRENT_PROJECT_PATH, ".temp", "test", "test_feature", "test1.sqlite")
        if os.path.exists(obj_db_path):
            os.remove(obj_db_path)
        shutil.copyfile(feat_db_path, obj_db_path)

        images_folder = "object_images"
        video.delete_images(images_folder)

        subprocess.call(["feature-based-tracking",tracking_path,"--gf","--database-filename",obj_db_path])
        subprocess.call(["classify-objects.py", "--cfg", tracking_path, "-d", obj_db_path])  # Classify road users
        subprocess.call(["display-trajectories.py", "-i", ac.CURRENT_PROJECT_VIDEO_PATH,"-d", obj_db_path, "-o", ac.CURRENT_PROJECT_PATH + "/homography/homography.txt", "-t", "object", "--save-images", "-f", str(frame_start), "--last-frame", str(frame_start+num_frames)])
        
        video.move_images_to_project_dir_folder(images_folder)

