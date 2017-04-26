#!/usr/bin/env python

import os
import tornado.web
from baseHandler import BaseHandler
from traffic_cloud_utils.app_config import get_project_path, get_project_video_path
from traffic_cloud_utils.video import save_video_frame
from traffic_cloud_utils.plotting.visualization import road_user_traj, turn_icon_counts
from traffic_cloud_utils.turning_counts import trajectory_headings, get_objects_with_trajectory

from traffic_cloud_utils.statusHelper import StatusHelper, Status
import json
import traceback

class TurningCountsHandler(BaseHandler):
    """
    @api {get} /speedDistribution/ Speed Distribution
    @apiName SpeedDistribution
    @apiVersion 0.1.0
    @apiGroup Results
    @apiDescription Calling this route will create a graph of the speed distribution from a specified project. The image will then be sent back in the response body. This route requires running object tracking on the video, and then running safety analysis on the results of the object tracking beforehand.
    @apiParam {String} identifier The identifier of the project to create a speed distribution for.
    @apiParam {Integer} [speed_limit] speed limit of the intersection. Defaults to 25 mph.
    @apiParam {Boolean} [vehicle_only] Flag for specifying only vehicle speeds. Takes True, False, 1 (true), or 0 (false). Defaults to True.

    @apiSuccess {File} image_jpg The API will return the created graph upon success.

    @apiError error_message The error message to display.
    """
    def prepare(self):
        self.identifier = self.find_argument('identifier', str)
        self.project_exists(self.identifier)

        status_dict = StatusHelper.get_status(self.identifier)
        if status_dict[Status.Type.SAFETY_ANALYSIS] != Status.Flag.COMPLETE:
            status_code = 412
            self.error_message = "Safety analysis did not complete successfully, try re-running it."

    def get(self):
        status_code, reason = TurningCountsHandler.handler(self.identifier)
        if status_code == 200:
            image_path = os.path.join(\
                                    get_project_path(self.identifier),\
                                    'final_images',\
                                    'turningCounts.jpg')
            self.set_header('Content-Disposition',\
                            'attachment; filename=turningCounts.jpg')
            self.set_header('Content-Type', 'application/octet-stream')
            self.set_header('Content-Description', 'File Transfer')
            self.write_file_stream(image_path)
            self.finish("Create Turning Counts")
        else:
            self.error_message = reason
            raise tornado.web.HTTPError(status_code=status_code)

    @staticmethod
    def handler(identifier, save_turns=False):
        project_dir = get_project_path(identifier)

        if not os.path.exists(project_dir):
            return (500, 'Project directory does not exist. Check your identifier?')

        db = os.path.join(project_dir, 'run', 'results.sqlite')
        if not os.path.exists(db):
            return (500, 'Database file does not exist. Trajectory analysis needs to be called first ')

        homography = os.path.join(project_dir, 'homography', 'homography.txt')

        # Save a frame in order to overlay trajectories
        video_path = get_project_video_path(identifier)
        if not os.path.exists(video_path):
            return (500, 'Source video file does not exist.  Was the video uploaded?')
        image_path = os.path.join(project_dir, '.temp', 'frame.png')
        save_video_frame(video_path, image_path)

        final_images = os.path.join(project_dir, 'final_images')
        if not os.path.exists(final_images):
            os.mkdir(final_images)

        if save_turns:
            turn_images = os.path.join(final_images, 'turns')
            if not os.path.exists(turn_images):
                os.mkdir(turn_images)

        obj_to_heading = trajectory_headings(db, homography)

        out = {}

        for turn in ['left', 'straight', 'right']:
            objs = get_objects_with_trajectory(obj_to_heading, turn=turn)
            if save_turns:
                save_path = os.path.join(turn_images, 'turn_'+turn+'.png')
                road_user_traj(db, homography, image_path, save_path, objs_to_plot=objs, plot_cars=True)

            for direction in ['right', 'down', 'left', 'up']:
                if direction not in out:
                    out[direction] = {}

                objs = get_objects_with_trajectory(obj_to_heading, turn=turn, initial_heading=direction)
                if save_turns:
                    save_path = os.path.join(turn_images, 'turn_'+turn+'_direction_'+direction+'.png')
                    road_user_traj(db, homography, image_path, save_path, objs_to_plot=objs, plot_cars=True)

                out[direction][turn] = len(objs)

        save_path = os.path.join(final_images, 'turningCounts.jpg')
        turn_icon_counts(out, save_path)

        return (200, "Success")

