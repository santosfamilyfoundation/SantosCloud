"""
Project management classes and functions
"""

import os
from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError
import time
import datetime
from shutil import copy
import cv2
try:
    from PIL import Image
except:
    import Image
import cvutils
import numpy as np

from app_config import AppConfig as ac
from app_config import check_project_cfg_option, update_project_cfg, check_project_cfg_section

import subprocess
import uuid

class ProjectWizard():

    def __init__(self,files):
        self.dict_files = files

        self.aerial_image_selected = False
        self.video_selected = False

        # self.DEFAULT_PROJECT_DIR = os.path.join(os.getcwd(), os.pardir, "project_dir")
        ac.load_application_config()
        self.DEFAULT_PROJECT_DIR = ac.PROJECT_DIR

        self.uuid = uuid.uuid4()
        self.config_parser = SafeConfigParser()
        self.create_project_dir(self.uuid)

    def create_project_dir(self, uuid):
        self.project_name = str(uuid)
        directory_names = ["homography", ".temp/test/test_object/", ".temp/test/test_feature/", "run", "results"]
        pr_path = os.path.join(self.DEFAULT_PROJECT_DIR, self.project_name)

        if not os.path.exists(pr_path):
            # Create proj dirs
            self.PROJECT_PATH = pr_path
            for new_dir in directory_names:
                os.makedirs(os.path.join(pr_path, new_dir))

            # Write files from client
            for key,value in self.dict_files.iteritems():
                if key[:5] == 'video':
                    self.videopath = os.path.join(pr_path, key)
                with open(os.path.join(pr_path, key), 'wb') as fh:
                    fh.write(value)


            self._write_to_project_config()
            copy(os.path.join(os.path.dirname(os.path.realpath(__file__)), "default/tracking.cfg"), os.path.join(pr_path, "tracking.cfg"))

            copy(os.path.join(os.path.dirname(os.path.realpath(__file__)), "default/classifier.cfg"), os.path.join(pr_path, "classifier.cfg"))
            with open(os.path.join(pr_path, 'tracking.cfg') ,'r+') as trkcfg:
                old = trkcfg.read()
                trkcfg.seek(0)
                newline = 'classifier-filename = ../project_dir/{}/classifier.cfg'.format(self.project_name)
                trkcfg.write(newline+old)
            with open(os.path.join(pr_path, 'classifier.cfg'),'r+') as newcfg:
                old = newcfg.read()
                newcfg.seek(0)
                nline1 = 'pbv-svm-filename = ../project_dir/{}/modelPBV.xml\n'.format(self.project_name)
                nline2 = 'bv-svm-filename = ../project_dir/{}/modelBV.xml\n'.format(self.project_name)
                newcfg.write(nline1+nline2+old)

            svms = ["modelBV.xml", "modelPB.xml", "modelPBV.xml", "modelPV.xml"]
            for svm in svms:
                copy(os.path.join(os.path.dirname(os.path.realpath(__file__)), "default/{}".format(svm)), os.path.join(pr_path, svm))

            self.load_new_project()

        else:
            print("Project exists. No new project created.")

    def _write_to_project_config(self):
        # Copy information given by the project_name.cfg generated client side
        client_config_parser = SafeConfigParser()
        client_config_parser.read(os.path.join(self.PROJECT_PATH, "project_name.cfg"))
        unitpixelratio = None
        try:
            unitpixelratio = client_config_parser.get("homography", "unitpixelratio")
        except NoSectionError:
            print("NoSectionError: no 'homography' section found in config file. Unit Pixel Ratio will not be copied.")

        ts = time.time()
        vid_ts = datetime.datetime.now()
        #This line needs to be updated to no longer need the ui class. Load video and pull time.
        list_o = str(subprocess.check_output(["ffprobe",
         "-v", "error", 
         "-select_streams", "v:0", 
         "-show_entries", "stream=avg_frame_rate", 
         "-of", "default=noprint_wrappers=1:nokey=1", 
         self.videopath]))
        vid_framerate = str(int(list_o.strip().split('/')[0])/int(list_o.strip().split('/')[1]))
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S %Z')
        video_timestamp = vid_ts.strftime('%d-%m-%Y %H:%M:%S %Z')
        self.config_parser.add_section("info")
        self.config_parser.set("info", "project_name", self.project_name)
        self.config_parser.set("info", "creation_date", timestamp)
        self.config_parser.add_section("video")
        self.config_parser.set("video", "name", os.path.basename(self.videopath))
        self.config_parser.set("video", "source", self.videopath)
        self.config_parser.set("video", "framerate", vid_framerate)
        self.config_parser.set("video", "start", video_timestamp)
        if unitpixelratio:
            self.config_parser.add_section("homography")
            self.config_parser.set("homography", "unitpixelratio", unitpixelratio)

        with open(os.path.join(self.PROJECT_PATH, "{}.cfg".format(self.project_name)), 'wb') as configfile:
            self.config_parser.write(configfile)

    def load_new_project(self):
        load_project(self.PROJECT_PATH)


def load_project(folder_path): # main_window):
    path = os.path.join(ac.PROJECT_DIR, os.path.normpath(folder_path))  # Clean path. May not be necessary.
    project_name = os.path.basename(path)
    project_cfg = os.path.join(path, "{}.cfg".format(project_name))
    ac.CURRENT_PROJECT_PATH = path  # Set application-level variables indicating the currently open project
    ac.CURRENT_PROJECT_NAME = project_name
    ac.CURRENT_PROJECT_CONFIG = project_cfg
    config_parser = SafeConfigParser()
    config_parser.read(project_cfg)  # Read project config file.
    print(project_cfg)
    ac.CURRENT_PROJECT_VIDEO_PATH = os.path.join(ac.CURRENT_PROJECT_PATH, config_parser.get("video", "name"))

    # TODO(rlouie): uncomment out these functions as they were originally called in TrafficGUI
    #load_homography(main_window)
    #load_results(main_window)


def load_homography(main_window):
    """
    Loads homography information into the specified main window.
    """
    path = ac.CURRENT_PROJECT_PATH
    aerial_path = os.path.join(path, "homography", "aerial.png")
    camera_path = os.path.join(path, "homography", "camera.png")
    # TODO: Handle if above two paths do not exist
    load_from = 'image_pts'  # "image_pts" or "pt_corrs"
    gui = main_window.ui
    # Load images
    gui.homography_aerialview.load_image_from_path(aerial_path)
    gui.homography_cameraview.load_image_from_path(camera_path)

    goodness_path = os.path.join(path, "homography", "homography_goodness_aerial.png")
    image_pts_path = os.path.join(path, "homography", "image-points.txt")
    pt_corrs_path = os.path.join(path, "homography", "point-correspondences.txt")
    homo_path = os.path.join(path, "homography", "homography.txt")

    if load_from is "image_pts":
        corr_path = image_pts_path
    else:
        corr_path = pt_corrs_path

    # Has a homography been previously computed?
    if check_project_cfg_section("homography"):  # If we can load homography unit-pix ratio load it
        # load unit-pixel ratio
        upr_exists, upr = check_project_cfg_option("homography", "unitpixelratio")
        if upr_exists:
            gui.unit_px_input.setText(upr)
    if os.path.exists(corr_path):  # If points have been previously selected
        worldPts, videoPts = cvutils.loadPointCorrespondences(corr_path)
        main_window.homography = np.loadtxt(homo_path)
        if load_from is "image_pts":
            for point in worldPts:
                main_window.ui.homography_aerialview.scene().add_point(point)
        elif load_from is "pt_corrs":
            for point in worldPts:
                main_window.ui.homography_aerialview.scene().add_point(point/float(upr))
        else:
            print("ERR: Invalid point source {} specified. Points not loaded".format(load_from))
        for point in videoPts:
            main_window.ui.homography_cameraview.scene().add_point(point)
        gui.homography_results.load_image_from_path(goodness_path)
    else:
        print ("{} does not exist. No points loaded.".format(corr_path))

def load_results(main_window):
    if os.path.exists(os.path.join(ac.CURRENT_PROJECT_PATH, "homography", "homography.txt")):
        if os.path.exists(os.path.join(ac.CURRENT_PROJECT_PATH, "run", "results.sqlite")):
            plot_results(main_window)