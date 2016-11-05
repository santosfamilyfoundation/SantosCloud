
import Enum
class Status(Enum):
	UPLOADING = "Uploading video"
	TRACKING_FEATURES = "Tracking features"
	TRACKING_OBJEcTS = "Tracking objects"
	GENERATING_VIDEOS = "Generating short videos"
	COMBINING_VIDEOS = "Combining videos"
	SAFETY_ANALYSIS = "Running safety analysis"
	DONE = "Done"

class StatusHelper(object):
	def __init__(self):
		self.status_dict = {}

	def set_status(identifier, status):
		self.status_dict[identifier] = status

	def get_status(identifier):
		return self.status_dict[identifier]

sharedStatusHelper = StatusHelper()