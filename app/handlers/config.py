#!/usr/bin/env python

import tornado.web

class ConfigHandler(tornado.web.RequestHandler):
    """
    @api {post} /config/ Configure Files
    @apiName Configure Files
    @apiGroup Configuration
    @apiDescription Calling this route will modify a specified configuration file using specified key:value pairs. Provides a way to modify configuration files by changing variables rather than uploading complete files.

    @apiParam {String} identifier The identifier of the project whose configuration files are to be modified.
    @apiParam {String} filename The name of the configuration file to be modified
    @apiParam {Dictionary} config_data A dictionary of key:value pairs containing the configuration variables to be modified.

    @apiSuccess status_code The API will return a status code of 200 upon success.

    @apiError error_message The error message to display.
    """
    def post(self):
        self.finish("Config")
