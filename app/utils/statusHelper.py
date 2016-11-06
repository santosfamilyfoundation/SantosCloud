
class Status(object):
    UPLOADING = "Uploading video"
    TRACKING_FEATURES = "Tracking features"
    TRACKING_OBJEcTS = "Tracking objects"
    GENERATING_VIDEOS = "Generating short videos"
    COMBINING_VIDEOS = "Combining videos"
    SAFETY_ANALYSIS = "Running safety analysis"
    DONE = "Done"
    UNKNOWN = "Unknown"

class StatusHelper(object):
    def __init__(self):
        self.status_dict = {}

    def set_status(self, identifier, status):
        self.status_dict[identifier] = status

    def get_status(self, identifier):
        if identifier not in self.status_dict:
            return Status.UNKNOWN
        return self.status_dict[identifier]

sharedStatusHelper = StatusHelper()