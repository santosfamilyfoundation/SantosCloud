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
        upload_dir = os.path.join(os.getcwd(), 'uploads')
        if not os.path.exists(upload_dir):
            os.mkdir(upload_dir)
        fh = open(os.path.join(upload_dir, cname), 'wb')
        fh.write(fileinfo['body'])
        self.finish(cname + " is uploaded!! Check uploads folder")


    def get(self):
        self.render("upload.html")
