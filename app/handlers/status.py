#!/usr/bin/env python

import tornado.escape
import tornado.web
from traffic_cloud_utils.statusHelper import StatusHelper

class StatusHandler(tornado.web.RequestHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        status_dict = StatusHelper.get_status(data['project_id'])
        if status_dict != None:
        	self.write({'status': status_dict})
        else:
        	# TODO: Error
        	pass
