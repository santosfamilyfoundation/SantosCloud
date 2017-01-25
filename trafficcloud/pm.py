"""
Project management classes and functions
"""

import os
from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError
import time
import datetime
from shutil import copy
try:
    from PIL import Image
except:
    import Image
import cvutils
import numpy as np

from app_config import get_project_path, get_project_config_path, config_section_exists
from video import get_framerate

import subprocess
import uuid

class ProjectWizard():

    def __init__(self,files):
        self.dict_files = files

        self.identifier = str(uuid.uuid4())
        self.create_project_dir(self.identifier)

    def create_project_dir(self, identifier):
        directory_names = ["homography", ".temp/test/test_object/", ".temp/test/test_feature/", "run", "results"]
        project_path = get_project_path(identifier)

        if not os.path.exists(project_path):
            # Create proj dirs
            for new_dir in directory_names:
                os.makedirs(os.path.join(project_path, new_dir))

            # Write files from client
            for key,value in self.dict_files.iteritems():
                if key[:5] == 'video':
                    self.videopath = os.path.join(project_path, key)
                with open(os.path.join(project_path, key), 'wb') as fh:
                    fh.write(value)


            self._write_to_project_config(identifier)

            default_files_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "default")

            copy(os.path.join(default_files_dir, "tracking.cfg"), os.path.join(project_path, "tracking.cfg"))
            copy(os.path.join(default_files_dir, "classifier.cfg"), os.path.join(project_path, "classifier.cfg"))

            with open(os.path.join(project_path, 'tracking.cfg') ,'r+') as trkcfg:
                old = trkcfg.read()
                trkcfg.seek(0)
                newline = 'classifier-filename = '+os.path.join(project_path, 'classifier.cfg')
                trkcfg.write(newline+old)

            with open(os.path.join(project_path, 'classifier.cfg'),'r+') as newcfg:
                old = newcfg.read()
                newcfg.seek(0)
                nline1 = 'pbv-svm-filename = '+os.path.join(default_files_dir, 'modelPBV.xml') + '\n'
                nline2 = 'bv-svm-filename = '+os.path.join(default_files_dir, 'modelBV.xml') + '\n'
                newcfg.write(nline1+nline2+old)

        else:
            print("Project exists. No new project created.")

    def _write_to_project_config(self, identifier):
        # Copy information given by the project_name.cfg generated client side
        client_config_parser = SafeConfigParser()
        client_config_parser.read(os.path.join(get_project_path(identifier), "project_name.cfg"))
        unitpixelratio = None
        try:
            unitpixelratio = client_config_parser.get("homography", "unitpixelratio")
        except NoSectionError:
            print("NoSectionError: no 'homography' section found in config file. Unit Pixel Ratio will not be copied.")

        ts = time.time()
        vid_ts = datetime.datetime.now()
        #This line needs to be updated to no longer need the ui class. Load video and pull time.
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S %Z')
        video_timestamp = vid_ts.strftime('%d-%m-%Y %H:%M:%S %Z')
        config_parser = SafeConfigParser()
        config_parser.add_section("info")
        config_parser.set("info", "project_name", identifier)
        config_parser.set("info", "creation_date", timestamp)
        config_parser.add_section("video")
        config_parser.set("video", "name", os.path.basename(self.videopath))
        config_parser.set("video", "source", self.videopath)
        config_parser.set("video", "framerate", get_framerate(self.videopath))
        config_parser.set("video", "start", video_timestamp)
        if unitpixelratio:
            config_parser.add_section("homography")
            config_parser.set("homography", "unitpixelratio", unitpixelratio)

        with open(get_project_config_path(identifier), 'wb') as configfile:
            config_parser.write(configfile)

        os.remove(os.path.join(get_project_path(identifier), "project_name.cfg"))
