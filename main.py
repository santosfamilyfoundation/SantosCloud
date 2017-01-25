
from trafficcloud import api
from trafficcloud.app_config import AppConfig as ac
import sys

if __name__ == "__main__":
    ac.load_application_config()
    if len(sys.argv) <= 1:
        print('Please pass the name of the folder in project_dir that you would like to run analysis on.')
    else:
        project = sys.argv[1]
        project_identifier = project.strip('/').split('/')[-1]
        api.runTrajectoryAnalysis(project_identifier)
        # api.createVideos(project_identifier)