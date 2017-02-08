#!/usr/bin/env python

import tornado.web

from traffic_cloud_utils.pm import default_config_dict
from baseHandler import BaseHandler

class DefaultConfigHandler(BaseHandler):
    """
    @api {post} /defaultConfig/ Default Configuration
    @apiName Default Configuration
    @apiVersion 0.1.0
    @apiGroup Configuration
    @apiDescription Calling this route will return the default values for the configuration files used by the server. This is useful if you want to display the values of the configuration parameters to the user, without hardcoding the values and potentially being incorrect if default values on the server change.

    @apiSuccess {Integer} max_features_per_frame This is the maximum number of features to track per frame. 
    @apiSuccess {Integer} num_displacement_frames This parameter determines how long features will be tracked. 
    @apiSuccess {Number} min_feature_displacement This is the displacement needed to track a feature. 
    @apiSuccess {Integer} max_iterations_to_persist This is the maximum number of iterations that an unmoving feature should persist. 
    @apiSuccess {Integer} min_feature_frames This is the minimum number of frames that a feature must persist in order to be considered a feature. 
    @apiSuccess {Number} max_connection_distance This is the maximum distance that two features can be apart and still be considered part of the same object. 
    @apiSuccess {Number} max_segmentation_distance This is the maximum distance that two features that are moving relative to each other can be apart and still be considered part of the same object. 

    @apiError error_message The error message to display.
    """
    def post(self):
        self.finish(default_config_dict())



