#!/usr/bin/env python

import tornado.web

class TestConfigHandler(tornado.web.RequestHandler):
    """
    @api {post} /testConfig/ Test Configuration
    @apiName TestConfig
    @apiGroup Configuration
    @apiDescription Calling this route will test the video's configuration. When testing is done, an email will be sent to the project's user. This test consists of running object tracking on a small subset of the video, and producing a video showing the results of the tracking. (Due to the potentially long duration of testing, it is infeasible to return the results as a response to the HTTP request. In order to check the status of the testing and view results, see the Status group of messages.)

    @apiParam {String} test_flag Flag to determine whether feature tracking or object tracking will be tested.
    @apiParam {String} identifier The identifier of the project to test configuration of.
    @apiParam {Integer} [frame_start] The frame number to start the configuration test at. If no frame_start is provided, the configuration test will start at the beginning of the video.
    @apiParam {Integer} [num_frames] The number of frames to analyze. To keep configuration testing short, this parameter must be less than 200. If no num_frames is provided, a default value of 100 will be used.

    @apiSuccess status_code The API will return a status code of 200 upon success.

    @apiError error_message The error message to display.
    """
    def post(self):
        self.finish("Test feature tracking")