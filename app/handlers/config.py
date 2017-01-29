#!/usr/bin/env python

import tornado.web

from trafficcloud.pm import default_config_dict, update_project_config

class ConfigHandler(tornado.web.RequestHandler):
    """
    @api {post} /config/ Configure Project
    @apiName Configure Project
    @apiVersion 0.0.0
    @apiGroup Configuration
    @apiDescription Calling this route will modify a specified configuration file using values of the provided arguments.

    @apiParam {String} identifier The identifier of the project whose configuration files are to be modified.
    @apiParam {Integer} [max_features_per_frame] This is the maximum number of features to track per frame. If not provided, a value of 1000 will be used. The recommended value for this is 1000 or greater.
    @apiParam {Integer} [num_displacement_frames] This parameter determines how long features will be tracked. If not provided, a value of 10 will be used. The recommended value for this is 2-15.
    @apiParam {Number} [min_feature_displacement] This is the displacement needed to track a feature. If not provided, a value of 0.0001 will be used. The recommended value for this is 0.0001-0.1.
    @apiParam {Integer} [max_iterations_to_persist] This is the maximum number of iterations that an unmoving feature should persist. If not provided, a value of 200 will be used. The recommended value for this is 10-1000.
    @apiParam {Integer} [min_feature_frames] This is the minimum number of frames that a feature must persist in order to be considered a feature. If not provided, a value of 15 will be used. The recommended value for this is 10-25.
    @apiParam {Number} [max_connection_distance] This is the maximum distance that two features can be apart and still be considered part of the same object. If not provided, a value of 1 will be used.
    @apiParam {Number} [max_segmentation_distance] This is the maximum distance that two features that are moving relative to each other can be apart and still be considered part of the same object. If not provided, a value of .7 will be used.


    @apiSuccess status_code The API will return a status code of 200 upon success.

    @apiError error_message The error message to display.
    """
    def post(self):
        identifier = self.get_body_argument("identifier")

        config_keys = default_config_dict().keys()
        config_dict = {}

        for key in config_keys:
            arg = self.get_body_argument(key, default=None)
            if arg != None:
                config_dict[key] = arg

        self.handler(identifier, config_dict)

        self.finish("Config")

    @staticmethod
    def handler(identifier, config_dict):
        update_project_config(identifier, config_dict)





