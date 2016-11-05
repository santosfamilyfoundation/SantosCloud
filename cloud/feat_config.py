import os
import sys

def getConfig_features(self):
    """
    Gets the features configuration file and returns the data as a dictionary.
    """
    path = os.path.join(ac.CURRENT_PROJECT_PATH, ".temp/test/test_feature/feature_tracking.cfg")

    f = open(path, "r")
    lines = f.readlines()
    f.close()

    final_dict = {}
    for line in lines:
        line = line.strip()

        # If it's a comment, ignore it
        if len(line) > 0 and line[0] == '#':
            continue

        arr = line.split(' = ')

        # Protect against things that aren't in "this = that" format
        if len(arr) != 2:
            continue

        final_dict[arr[0]] = arr[1]

    return final_dict