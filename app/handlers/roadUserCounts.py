#!/usr/bin/env python

import os
import tornado.web
import tornado.escape

from traffic_cloud_utils.plotting.visualization import road_user_counts, road_user_icon_counts, object_counts_over_time
from traffic_cloud_utils.app_config import get_project_path, get_project_video_path
from traffic_cloud_utils.video import get_framerate, get_number_of_frames
from baseHandler import BaseHandler

class RoadUserCountsHandler(BaseHandler):
    """
    @api {post} /roadUserCounts/ Road User Counts
    @apiName RoadUserCounts
    @apiVersion 0.2.0
    @apiGroup Results
    @apiDescription Calling this route will create road user counts visualizations from a specified project. When the image is created, an email will be sent to the project's user. This route requires running object tracking on the video, and then running safety analysis on the results of the object tracking beforehand. (Due to the potentially long duration, it is infeasible to return the results as a response to the HTTP request. In order to check the status of the testing and view results, see the Status group of messages.)

    @apiParam {String} identifier The identifier of the project to create road user counts for.

    @apiSuccess status_code The API will return a status code of 200 upon success.

    @apiError error_message The error message to display.
    """
    def post(self):
        identifier = self.find_argument('identifier')
        status_code, reason = RoadUserCountsHandler.handler(identifier)
        print status_code
        print reason
        if status_code == 200:
            self.finish("Visualize Road User Counts")
        else:
            self.error_message = reason
            raise tornado.web.HTTPError(status_code=status_code)

    @staticmethod
    def handler(identifier):
        project_dir = get_project_path(identifier)
        if not os.path.exists(project_dir):
            return (500, 'Project directory does not exist. Check your identifier?')

        db = os.path.join(project_dir, 'run', 'results.sqlite')
        if not os.path.exists(db):
            return (500, 'Database file does not exist. Trajectory analysis needs to be called first ')

        final_images = os.path.join(project_dir, 'final_images')
        if not os.path.exists(final_images):
            os.mkdir(final_images)

        # Aggregate Road User Counts
        try:
            counts = road_user_counts(db)
        except Exception as err_msg:
            return (500, str(err_msg))

        try:
            road_user_icon_counts('Road User Counts',
                car=counts['car'],
                bike=counts['bicycle'],
                pedestrian=counts['pedestrian'],
                save_path=os.path.join(final_images, 'road_user_icon_counts.jpg'))
        except Exception as err_msg:
            return (500, str(err_msg))

        # Road User Counts over time
        try:
            video_path = get_project_video_path(identifier)
            fps = float(get_framerate(video_path))

        except Exception as err_msg:
            return (500, str(err_msg))

        # 60 seconds/min * 60 min/hour
        longer_than_an_hour = get_number_of_frames(video_path)/fps > 60*60
        try:
            if longer_than_an_hour:
                for user_type in [1, 2, 4]: # car, ped, bike
                    object_counts_over_time(db, user_type, int(fps*60*15), '# of 15 min blocks', final_images)
        except Exception as err_msg:
            return (500, str(err_msg))

        return (200, "Success")
