
###This will hold all api calls for TrafficInTheCloud

import os
import shutil
from app_config import AppConfig as ac
from app_config import update_config_without_sections
import pm
import subprocess
import video, feat_config

from plotting.make_object_trajectories import main as db_make_objtraj

def saveFiles(diction, *args):
    return pm.ProjectWizard(diction).identifier

def runConfigTestFeature(identifier, config, frames, ret_type, ret_args, *args):
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

def runTrajectoryAnalysis(identifier):#, config, ret_type, ret_args, *args):
    """
    Runs TrafficIntelligence trackers and support scripts.
    """
    ac.load_application_config()
    pm.load_project(identifier)

    # create test folder
    if not os.path.exists(ac.CURRENT_PROJECT_PATH + "/run"):
        os.mkdir(ac.CURRENT_PROJECT_PATH + "/run")

    tracking_path = os.path.join(ac.CURRENT_PROJECT_PATH, "run", "run_tracking.cfg")

    # removes object tracking.cfg
    if os.path.exists(tracking_path):
        os.remove(tracking_path)

    # creates new config file
    shutil.copyfile(ac.CURRENT_PROJECT_PATH + "/.temp/test/test_object/object_tracking.cfg", tracking_path)

    update_dict = {'frame1': 0, 
        'nframes': 0, 
        'database-filename': 'results.sqlite', 
        'classifier-filename': os.path.join(ac.CURRENT_PROJECT_PATH, "classifier.cfg"),
        'video-filename': ac.CURRENT_PROJECT_VIDEO_PATH,
        'homography-filename': os.path.join(ac.CURRENT_PROJECT_PATH, "homography", "homography.txt")}
    update_config_without_sections(tracking_path, update_dict)

    db_path = os.path.join(ac.CURRENT_PROJECT_PATH, "run", "results.sqlite")

    if os.path.exists(db_path):  # If results database already exists,
        os.remove(db_path)  # then remove it--it'll be recreated.
    subprocess.call(["feature-based-tracking", tracking_path, "--tf", "--database-filename", db_path])
    subprocess.call(["feature-based-tracking", tracking_path, "--gf", "--database-filename", db_path])

    subprocess.call(["classify-objects.py", "--cfg", tracking_path, "-d", db_path])  # Classify road users

    db_make_objtraj(db_path)  # Make our object_trajectories db table

    video.create_tracking_video(ac.CURRENT_PROJECT_PATH, ac.CURRENT_PROJECT_VIDEO_PATH)

def createVideos(identifier):
    """
    Runs TrafficIntelligence trackers and support scripts.
    """
    ac.load_application_config()
    pm.load_project(identifier)

    video.create_tracking_video(ac.CURRENT_PROJECT_PATH, ac.CURRENT_PROJECT_VIDEO_PATH)


def runSafetyAnalysis(identifier, prediction_method=None):

    ac.load_application_config()
    pm.load_project(identifier)

    config_path = os.path.join(ac.CURRENT_PROJECT_PATH, "run", "run_tracking.cfg")
    db_path = os.path.join(ac.CURRENT_PROJECT_PATH, "run", "results.sqlite")
    update_dict = {
        'video-filename': ac.CURRENT_PROJECT_VIDEO_PATH, # use absolute path to video on server
        'database-filename': db_path # use absolute path to database
    }
    update_config_without_sections(config_path, update_dict)

    if prediction_method is None:
        prediction_method = 'cv' # default to the least resource intensive method

    # Predict Interactions between road users and compute safety metrics describing them
    subprocess.call(["safety-analysis.py", "--cfg", config_path, "--prediction-method", prediction_method])


def runVisualization(identifier, db, ret_form, ret_type, ret_args, *args):
    pass

def getDB(identifier):
    pass

def getStatus(identifier):
    pass

def generateDefaultConfig():
    pass

if __name__ == "__main__":
    pass