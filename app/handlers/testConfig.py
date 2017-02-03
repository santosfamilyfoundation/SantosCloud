#!/usr/bin/env python
import os
import subprocess
import shutil

import tornado.web
import threading

from traffic_cloud_utils.app_config import get_project_path, get_project_video_path, update_config_without_sections, get_config_without_sections
from traffic_cloud_utils.emailHelper import EmailHelper
from traffic_cloud_utils.app_config import update_config_without_sections
from traffic_cloud_utils import video

class TestConfigHandler(tornado.web.RequestHandler):
    """
    @api {post} /testConfig/ Test Configuration
    @apiName TestConfig
    @apiVersion 0.1.0
    @apiGroup Configuration
    @apiDescription Calling this route will test the video's configuration. This test consists of running object tracking on a small subset of the video, and producing a video showing the results of the tracking. (Due to the potentially long duration of testing, it is infeasible to return the results as a response to the HTTP request. In order to check the status of the testing and view results, see the Status group of messages.)

    @apiParam {String} test_flag Flag to determine whether feature tracking or object tracking will be tested.
    @apiParam {String} identifier The identifier of the project to test configuration of.
    @apiParam {Integer} [frame_start] The frame number to start the configuration test at. If no frame_start is provided, the configuration test will start at the beginning of the video.
    @apiParam {Integer} [num_frames] The number of frames to analyze. To keep configuration testing short, this parameter must be less than 200. If no num_frames is provided, a default value of 100 will be used.

    @apiSuccess status_code The API will return a status code of 200 upon success.

    @apiError error_message The error message to display.
    """
    def post(self):

        identifier = self.get_body_argument("identifier")
        test_flag = self.get_body_argument("test_flag")
        print test_flag

        frame_start = int(self.get_body_argument("frame_start", default = 0))
        num_frames = int(self.get_body_argument("num_frames", default = 120))

        status_code, response_message = TestConfigHandler.handler(identifier, frame_start, num_frames, test_flag)

        if status_code == 200:
            self.finish("Testing tracking")
        else:
            raise tornado.web.HTTPError(reason=reason, status_code=status_code)

    @staticmethod
    def handler(identifier, frame_start, num_frames, test_flag):
        project_path = get_project_path(identifier)
        if not os.path.exists(project_path):
           return (500, 'Project directory does not exist. Check your identifier?')

        if test_flag == "feature":
            print "running feature"
            TestConfigFeatureThread(identifier, frame_start, num_frames, TestConfigHandler.test_feature_callback).start()
        elif test_flag == "object":
            print "running object"
            TestConfigObjectThread(identifier, frame_start, num_frames, TestConfigHandler.test_feature_callback).start()

        return (200, "Success")


    @staticmethod
    def test_feature_callback(status_code, response_message, identifier):
        print(status_code, response_message)

    @staticmethod
    def test_object_callback(status_code, response_message, identifier):
        print(status_code, response_message)


class TestConfigFeatureThread(threading.Thread):
    def __init__(self, identifier, frame_start, num_frames, callback):
        threading.Thread.__init__(self)
        self.identifier = identifier
        self.frame_start = frame_start
        self.num_frames = num_frames
        self.callback = callback

    def run(self):
        project_path = get_project_path(self.identifier)
        tracking_path = os.path.join(project_path, "tracking.cfg")
        db_path = os.path.join(project_path, ".temp", "test", "test_feature", "test1.sqlite")
        if os.path.exists(db_path):
            os.remove(db_path)

        testing_dict = {'frame1': self.frame_start, 'nframes': self.num_frames}
        update_config_without_sections(tracking_path, testing_dict)

        images_folder = os.path.join(get_project_path(self.identifier), "feature_images")
        video.delete_files(images_folder)

        try:
            subprocess.call(["feature-based-tracking", tracking_path, "--tf", "--database-filename", db_path])
            subprocess.call(["display-trajectories.py", "-i", get_project_video_path(self.identifier), "-d", db_path, "-o", project_path + "/homography/homography.txt", "-t", "feature", "--save-images", "-f", str(self.frame_start), "--last-frame", str(self.frame_start+self.num_frames)])
        except Exception as err_msg:
            return self.callback(500, err_msg, self.identifier)

        videos_folder = os.path.join(get_project_path(self.identifier), "feature_images")
        video_filename = "feature_video.mp4"
        temp_image_prefix = 'image-'
        video.move_files_to_folder(os.getcwd(),images_folder,temp_image_prefix, '.png')
        video.renumber_frames(images_folder, 0, temp_image_prefix, "png")
        video.convert_frames_to_video(get_project_video_path(self.identifier), images_folder, videos_folder, temp_image_prefix, video_filename, 1.0)

        self.callback(200, "Test config done", self.identifier)

class TestConfigObjectThread(threading.Thread):
    def __init__(self, identifier, frame_start, num_frames, callback):
        threading.Thread.__init__(self)
        self.identifier = identifier
        self.frame_start = frame_start
        self.num_frames = num_frames
        self.callback = callback

    def run(self):
        project_path = get_project_path(self.identifier)
        tracking_path = os.path.join(project_path, "tracking.cfg")
        obj_db_path = os.path.join(project_path,".temp", "test", "test_object", "test1.sqlite")
        feat_db_path = os.path.join(project_path, ".temp", "test", "test_feature", "test1.sqlite")
        if os.path.exists(obj_db_path):
            os.remove(obj_db_path)
        shutil.copyfile(feat_db_path, obj_db_path)

        testing_dict = {'frame1': self.frame_start, 'nframes': self.num_frames}
        update_config_without_sections(tracking_path, testing_dict)

        images_folder = "object_images"
        video.delete_files(images_folder)

        try:
            subprocess.call(["feature-based-tracking",tracking_path,"--gf","--database-filename",obj_db_path])
            subprocess.call(["classify-objects.py", "--cfg", tracking_path, "-d", obj_db_path])  # Classify road users
            subprocess.call(["display-trajectories.py", "-i", get_project_video_path(self.identifier),"-d", obj_db_path, "-o", project_path + "/homography/homography.txt", "-t", "object", "--save-images", "-f", str(self.frame_start), "--last-frame", str(self.frame_start+self.num_frames)])
        except Exception as err_msg:
            self.callback(500, err_msg, self.identifier)

        video.move_files_to_folder(os.getcwd(),images_folder,'image-', '.png')

        self.callback(200, "Test config done", self.identifier)



