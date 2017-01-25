#!/usr/bin/env python
import os
import subprocess
import shutil
import smtplib
from email.mime.text import MIMEText

import tornado.web

from app_config import AppConfig as ac
from app_config import update_config_without_sections
import pm
import video



class ObjectTrackingHandler(tornado.web.RequestHandler):
    """
    @api {post} /objectTracking/ Object Tracking
    @apiName ObjectTracking
    @apiVersion 0.0.0
    @apiGroup Analysis
    @apiDescription Calling this route will perform object tracking on the video. When the analysis is done, an email will be sent to the project's user. (Due to the potentially long run duration, it is infeasible to return the results as a response to the HTTP request. In order to check the status of the testing and view results, see the Status group of messages.)

    @apiParam {String} identifier The identifier of the project on which to run object tracking.
    @apiParam {String} email The email address that should be notified when the object tracking is complete.

    @apiSuccess status_code The API will return a status code of 200 upon success.

    @apiError error_message The error message to display.
    """

    def post(self):
        self.objectTrack(self.request.identifier)

        host_email = os.environ.get('SANTOSCLOUD_EMAIL')
        
        msg = MIMEText("Hello,\n\tWe have finished processing your video and identifying all objects.\nThank you for your patience,\nThe Santos Team")
        msg['Subject'] = "Your video has finished processing."
        msg['From'] = "SantosTrafficCloud@gmail.com"
        msg['To'] = self.request.email

        s = smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        s.login(host_email, os.environ.get('SANTOSCLOUD_EMAIL_PASSWORD'))
        s.sendmail(host_email, [self.request.email], msg.as_string())
        s.quit()

        self.finish("Object Tracking")


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

