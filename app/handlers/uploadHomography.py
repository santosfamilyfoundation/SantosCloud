#!/usr/bin/env python

import tornado.web
from tornado.escape import json_decode
import os
from traffic_cloud_utils.app_config import get_project_path
import numpy as np
import cv2

class UploadHomographyHandler(tornado.web.RequestHandler):
    """
    @api {post} /uploadHomography/ Upload Homography
    @apiName UploadHomography
    @apiVersion 0.1.0
    @apiGroup Upload
    @apiDescription Use this route to upload homography files for a project.

    @apiParam {String} identifier The identifier of the project to upload files to.
    @apiParam {File} aerial An aerial photo of the intersection.
    @apiParam {File} camera A screenshot of the intersection from the video.
    @apiParam {File} homography The homography text file to use.

    @apiSuccess status_code The API will return a status code of 200 upon success.

    @apiError error_message The error message to display.
    """
    def initialize(self):
        self.identifier = None
        self.files = {}

    def post(self):
        self.files = self.request.files
        self.identifier = self.get_body_argument('identifier')
        self.up_ratio = float(self.get_body_argument('unit_pixel_ratio'))
        self.write_homography_files()
        self.finish("Upload Homography")
        
    def write_homography_files(self):
        project_dir = get_project_path(self.identifier)
        num_points = int(self.get_body_argument('num_points')) 
        points = [ (self.get_body_arguments('p'+str(i))[0],\
                    self.get_body_arguments('p'+str(i))[1]) for i in xrange(num_points)]

        homography = self.handler(self.up_ratio, points)
        np.savetxt(os.path.join(project_dir,'homography','homography.txt'),homography)

        for key,value in self.files.iteritems():
            with open(os.path.join(project_dir,'homography',value[0]['filename']), 'wb') as f:
                f.write(value[0]['body'])

    @staticmethod
    def handler(up_ratio, pts):
        aerial, camera=  zip(*pts)

        unscaled_world = []
        for i in aerial:
            h,t = i.split(', ')
            unscaled_world.append((float(h[1:]),float(t[:-2])))

        scaled_video = []
        for i in camera:
            h,t = i.split(', ')
            scaled_video.append((float(h[1:]),float(t[:-2])))

        homography, mask = cv2.findHomography(up_ratio*np.array(unscaled_world), np.array(scaled_video))
        return homography
