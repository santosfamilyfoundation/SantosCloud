
###This will hold all api calls for TrafficInTheCloud

import os
import shutil
from app_config import get_project_path, get_project_video_path, update_config_without_sections, get_config_without_sections
import pm
import subprocess
import video, feat_config

from plotting.make_object_trajectories import main as db_make_objtraj

def saveFiles(diction, *args):
    return pm.ProjectWizard(diction).identifier

def runConfigTestFeature(identifier, config, frames, ret_type, ret_args, *args):
    tracking_path = os.path.join(get_project_path(identifier), ".temp", "test", "test_feature", "feature_tracking.cfg")
    db_path = os.path.join(get_project_path(identifier), ".temp", "test", "test_feature", "test1.sqlite")
    if os.path.exists(db_path):
        os.remove(db_path)

    images_folder = "feature_images"
    video.delete_images(images_folder)

    # Get the frame information for the test
    configuration = get_config_without_sections(tracking_path)
    frame1 = int(configuration["frame1"])
    nframes = int(configuration["nframes"])
    fps = float(configuration["video-fps"])

    subprocess.call(["feature-based-tracking", tracking_path, "--tf", "--database-filename", db_path])
    subprocess.call(["display-trajectories.py", "-i", get_project_video_path(identifier), "-d", db_path, "-o", get_project_path(identifier) + "/homography/homography.txt", "-t", "feature", "--save-images", "-f", str(frame1), "--last-frame", str(frame1+nframes)])

    video.move_images_to_project_dir_folder(images_folder)

def runTrajectoryAnalysis(identifier):#, config, ret_type, ret_args, *args):
    """
    Runs TrafficIntelligence trackers and support scripts.
    """
    project_path = get_project_path(identifier)

    # create test folder
    if not os.path.exists(project_path + "/run"):
        os.mkdir(project_path + "/run")

    tracking_path = os.path.join(project_path, "run", "run_tracking.cfg")

    # removes object tracking.cfg
    if os.path.exists(tracking_path):
        os.remove(tracking_path)

    # creates new config file
    shutil.copyfile(os.path.join(project_path, ".temp/test/test_object/object_tracking.cfg"), tracking_path)

    update_dict = {'frame1': 0, 
        'nframes': 0, 
        'database-filename': 'results.sqlite', 
        'classifier-filename': os.path.join(project_path, "classifier.cfg"),
        'video-filename': get_project_video_path(identifier),
        'homography-filename': os.path.join(project_path, "homography", "homography.txt")}
    update_config_without_sections(tracking_path, update_dict)

    db_path = os.path.join(project_path, "run", "results.sqlite")

    if os.path.exists(db_path):  # If results database already exists,
        os.remove(db_path)  # then remove it--it'll be recreated.
    subprocess.call(["feature-based-tracking", tracking_path, "--tf", "--database-filename", db_path])
    subprocess.call(["feature-based-tracking", tracking_path, "--gf", "--database-filename", db_path])

    subprocess.call(["classify-objects.py", "--cfg", tracking_path, "-d", db_path])  # Classify road users

    db_make_objtraj(db_path)  # Make our object_trajectories db table

    video.create_tracking_video(project_path, get_project_video_path(identifier))

def createVideos(identifier):
    """
    Runs TrafficIntelligence trackers and support scripts.
    """
    video.create_tracking_video(get_project_path(identifier), get_project_video_path(identifier))


def runSafetyAnalysis(identifier, prediction_method=None):
    project_path = get_project_path(identifier)
    config_path = os.path.join(project_path, "run", "run_tracking.cfg")
    db_path = os.path.join(project_path, "run", "results.sqlite")
    update_dict = {
        'video-filename': get_project_video_path(identifier), # use absolute path to video on server
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