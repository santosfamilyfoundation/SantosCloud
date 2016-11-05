
###This will hold all api calls for TrafficInTheCloud

import os
import shutil
from app_config import AppConfig as ac
import pm
import subprocess
import video, feat_config

from plotting.make_object_trajectories import main as db_make_objtraj

def saveFiles(diction, *args):
    pm.ProjectWizard(diction)


def runConfigTestFeature(uuid, config, frames, ret_type, ret_args, *args):
    ac.load_application_config()
    pm.load_project(ac.CURRENT_PROJECT_PATH)

    tracking_path = os.path.join(ac.CURRENT_PROJECT_PATH, ".temp", "test", "test_feature", "feature_tracking.cfg")
    db_path = os.path.join(ac.CURRENT_PROJECT_PATH, ".temp", "test", "test_feature", "test1.sqlite")
    if os.path.exists(db_path):
        os.remove(db_path)

    images_folder = "feature_images"
    video.delete_images(images_folder)

    # Get the frame information for the test
    configuration = feat_config.getConfig_features()
    frame1 = int(configuration["frame1"])
    nframes = int(configuration["nframes"])
    fps = float(configuration["video-fps"])

    subprocess.call(["feature-based-tracking", tracking_path, "--tf", "--database-filename", db_path])
    subprocess.call(["display-trajectories.py", "-i", ac.CURRENT_PROJECT_VIDEO_PATH, "-d", db_path, "-o", ac.CURRENT_PROJECT_PATH + "/homography/homography.txt", "-t", "feature", "--save-images", "-f", str(frame1), "--last-frame", str(frame1+nframes)])

    video.move_images_to_project_dir_folder(images_folder)

    self.feature_tracking_video_player.loadFrames(os.path.join(ac.CURRENT_PROJECT_PATH, images_folder), fps)

def runTrajectoryAnalysis(uuid):#, config, ret_type, ret_args, *args):
    """
    Runs TrafficIntelligence trackers and support scripts.
    """
    ac.load_application_config()
    pm.load_project(uuid)

    # create test folder
    if not os.path.exists(ac.CURRENT_PROJECT_PATH + "/run"):
        os.mkdir(ac.CURRENT_PROJECT_PATH + "/run")

    # removes object tracking.cfg
    if os.path.exists(ac.CURRENT_PROJECT_PATH + "/run/run_tracking.cfg"):
        os.remove(ac.CURRENT_PROJECT_PATH + "/run/run_tracking.cfg")

    # creates new config file
    shutil.copyfile(ac.CURRENT_PROJECT_PATH + "/.temp/test/test_object/object_tracking.cfg", ac.CURRENT_PROJECT_PATH + "/run/run_tracking.cfg")

    path1 = ac.CURRENT_PROJECT_PATH + "/run/run_tracking.cfg"

    f = open(path1, 'r')
    lines = f.readlines()
    f.close()
    with open(path1, "w") as wf:
        for line in lines:
            line_param = line.split('=')[0].strip()
            if "frame1" == line_param:  # Replace parameter "frame1"
                wf.write("frame1 = 0\n")
            elif "nframes" == line_param:  # Remove parameter "nframes"
                wf.write("nframes = 0\n")
            elif "database-filename" == line_param:
                wf.write("database-filename = results.sqlite\n")
            else:
                wf.write(line)

    db_path = os.path.join(ac.CURRENT_PROJECT_PATH, "run", "results.sqlite")
    tracking_path = os.path.join(ac.CURRENT_PROJECT_PATH, "run", "run_tracking.cfg")

    if os.path.exists(db_path):  # If results database already exists,
        os.remove(db_path)  # then remove it--it'll be recreated.
    subprocess.call(["feature-based-tracking", tracking_path, "--tf", "--database-filename", db_path])
    subprocess.call(["feature-based-tracking", tracking_path, "--gf", "--database-filename", db_path])

    subprocess.call(["classify-objects.py", "--cfg", tracking_path, "-d", db_path])  # Classify road users

    db_make_objtraj(db_path)  # Make our object_trajectories db table

    video.create_video()



def runSafetyAnalysis(uuid, prediction, db, ret_type, ret_args):
    pass

def runVisualization(uuid, db, ret_form, ret_type, ret_args, *args):
    pass

def getDB(uuid):
    pass

def getStatus(uuid):
    pass

def generateDefaultConfig():
    pass

if __name__ == "__main__":
	pass