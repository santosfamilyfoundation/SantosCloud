
from trafficcloud import api
import sys

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('Please pass the name of the folder in project_dir that you would like to run analysis on.')
    else:
        project = sys.argv[1]
        project_identifier = project.strip('/').split('/')[-1]
        api.runTrajectoryAnalysis(project_identifier)