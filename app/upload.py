#!/usr/bin/env python

import tornado.web
import os
import uuid

class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        fileinfo = self.request.files['filearg'][0]
        print 'hi'
        print "fileinfo is", fileinfo.keys()
        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[-1]
        cname = str(uuid.uuid4()) + extn
        if not os.exists(os.path.join(os.getcwd(), '/uploads')):
            os.mkdirs(os.path.join(os.getcwd(), '/uploads'))
        fh = open('uploads/' + cname, 'w')
        fh.write(fileinfo['body'])
        self.finish(cname + " is uploaded!! Check uploads folder")


    def get(self):
        self.render("upload.html")