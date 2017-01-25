
import os

from trafficcloud.app_config import AppConfig as ac
from trafficcloud.app_config import update_config_with_sections, get_config_section

class Status(object):
    class StatusType:
        UPLOAD_VIDEO = "upload_video"
        UPLOAD_HOMOGRAPHY = "upload_homography"
        CONFIGURATION_TEST = "configuration_test"
        FEATURE_TRACKING = "feature_tracking"
        OBJECT_TRACKING = "object_tracking"
        SAFETY_ANALYSIS = "safety_analysis"
        HIGHLIGHT_VIDEO = "highlight_video"

    class Status:
        INCOMPLETE = 0
        IN_PROGRESS = 1
        COMPLETE = 2

    def create_status_dict():
        return {
            self.Type.UPLOAD_VIDEO: 0,
            self.Type.UPLOAD_HOMOGRAPHY: 0,
            self.Type.CONFIGURATION_TEST: 0,
            self.Type.FEATURE_TRACKING: 0,
            self.Type.OBJECT_TRACKING: 0,
            self.Type.SAFETY_ANALYSIS: 0,
            self.Type.HIGHLIGHT_VIDEO: 0,
        }

class StatusHelper(object):
    @classmethod
    def get_config_path(cls, identifier):
        ac.load_application_config()
        return os.path.join(ac.PROJECT_DIR, identifier, "project_name.cfg")

    @classmethod
    def initalize_project(cls, identifier):
        d = cls.create_status_dict()
        config_path = self.get_config_path(identifier)
        for (status_type, status) in d.iteritems():
            update_config_with_sections(config_path, "status", status_type, status)

    @classmethod
    def set_status(cls, identifier, status_type, status):
        config_path = cls.get_config_path(identifier)
        update_config_with_sections(config_path, "status", status_type, status)

    @classmethod
    def get_status(cls, identifier):
        config_path = cls.get_config_path(identifier)
        (success, value) = get_config_section(config_path, "status")
        if success:
            return value
        else:
            return None


